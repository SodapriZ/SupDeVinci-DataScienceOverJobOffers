import json
import pandas as pd
import numpy as np
import re
import nltk
from datetime import datetime
import pyarrow.parquet as pq
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse.linalg import svds
import spacy

# Constants
JSON_FILE_PATH = "./results/we_love_dev-parsed_data.json"
OUTPUT_PARQUET_FILE_PATH = "./results/we_love_dev-cleaned_data.parquet"
OUTPUT_CSV_FILE_PATH = "./results/we_love_dev-cleaned_data.csv"

# Load French stopwords for text normalization
stop_words = nltk.corpus.stopwords.words('french')


def convert_timestamp(timestamp_ms: int) -> str:
    """
    Convert timestamp in milliseconds to human-readable format.
    
    Args:
        timestamp_ms (int): Timestamp in milliseconds.
        
    Returns:
        str: Human-readable timestamp.
    """
    try:
        if timestamp_ms:
            return datetime.fromtimestamp(int(timestamp_ms) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        pass
    return None


def normalize_text(text: str) -> str:
    """
    Normalize text by removing special characters, whitespaces, and stopwords.
    
    Args:
        text (str): Input text.
        
    Returns:
        str: Normalized text.
    """
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I | re.A).lower().strip()
    tokens = nltk.word_tokenize(text)
    filtered_tokens = [token for token in tokens if token not in stop_words]
    return ' '.join(filtered_tokens)


def create_vocab_matrix(normalized_sentences: list) -> np.ndarray:
    """
    Create a TF-IDF vocabulary matrix from a list of normalized sentences.
    
    Args:
        normalized_sentences (list): List of normalized sentences.
        
    Returns:
        np.ndarray: TF-IDF vocabulary matrix.
    """
    tv = TfidfVectorizer(min_df=0., max_df=1., use_idf=True)
    dt_matrix = tv.fit_transform(normalized_sentences)
    dt_matrix = dt_matrix.toarray()
    td_matrix = dt_matrix.T
    return td_matrix


def low_rank_svd(matrix: np.ndarray, singular_count: int = 2) -> tuple:
    """
    Perform low-rank SVD on a matrix.
    
    Args:
        matrix (np.ndarray): Input matrix.
        singular_count (int): Number of singular values to retain.
        
    Returns:
        tuple: Tuple containing U, S, and V^T matrices.
    """
    u, s, vt = svds(matrix, k=singular_count)
    return u, s, vt


def summarize_text(text: str) -> str:
    """
    Summarize text by extracting top salient sentences using TF-IDF and SVD.
    
    Args:
        text (str): Input text.
        
    Returns:
        str: Summarized text.
    """
    if text:
        apply_normalization = np.vectorize(normalize_text)
        sentences = nltk.sent_tokenize(text)

        if len(sentences) > 2:
            normalized_sentences = apply_normalization(sentences)
            td_matrix = create_vocab_matrix(normalized_sentences)
            num_sentences = 2
            num_topics = 2
            u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)
            salience_scores = np.sqrt(np.dot(np.square(s), np.square(vt)))
            top_sentence_indices = (-salience_scores).argsort()[:num_sentences]
            top_sentence_indices.sort()
            return '\n'.join(np.array(sentences)[top_sentence_indices])
        else:
            return None
    else:
        return None


def parse_skill_list(skill_list: list) -> str:
    """
    Parse and format skill list into a string.
    
    Args:
        skill_list (list): List of skill dictionaries.
        
    Returns:
        str: Formatted skill string.
    """
    if skill_list:
        sorted_skills = sorted(skill_list, key=lambda x: x['value'], reverse=True)
        skill_names = [skill['name'] for skill in sorted_skills]
        return '/'.join(skill_names)
    return None


def parse_location(location: list) -> dict:
    """
    Parse location information into a dictionary.
    
    Args:
        location (list): Location information.
        
    Returns:
        dict: Dictionary containing city and country information.
    """
    if location:
        city, country = location[0].split(", ")
        return {"city": city, "country": country}
    return {"city": None, "country": None}


def categorize_experience(experience: int) -> str:
    """
    Categorize years of experience into predefined categories.
    
    Args:
        experience (int): Years of experience.
        
    Returns:
        str: Experience category.
    """
    if experience <= 3:
        return '[0-3]'
    elif experience <= 7:
        return '[3-7]'
    else:
        return '[+7]'


def clean_data(parsed_data_list: list) -> list:
    """
    Clean parsed data and format it into a list of dictionaries.
    
    Args:
        parsed_data_list (list): List of parsed data dictionaries.
        
    Returns:
        list: List of cleaned data dictionaries.
    """
    cleaned_data_list = []
    for parsed_data in parsed_data_list:
        location_data = parse_location(parsed_data.get("location"))

        cleaned_data = {
            "company_name": parsed_data.get("company_name"),
            "job_offer_title": parsed_data.get("job_offer_title"),
            "profession_title": parsed_data.get("profession_title"),
            "description": parsed_data.get("description"),
            "description_summarized": summarize_text(parsed_data.get("description")),
            "salary_max": parsed_data["salary_info"].get("max"),
            "salary_avg": ((parsed_data["salary_info"].get("max", 0) + parsed_data["salary_info"].get("min", 0)) / 2),
            "salary_min": parsed_data["salary_info"].get("min"),
            "remote_quantity": parsed_data["remote_policy"].get("daysPerWeek"),
            "job_format": parsed_data["remote_policy"].get("frequency"),
            "required_experience": int(parsed_data.get("required_experience")),
            "required_experience_category": categorize_experience(int(parsed_data.get("required_experience"))),
            "team_management_description": parsed_data["team_description"].get("management"),
            "team_management_description_summarized": summarize_text(
                parsed_data["team_description"].get("management")),
            "team_technical_description": parsed_data["team_description"].get("technical"),
            "team_technical_description_summarized": summarize_text(
                parsed_data["team_description"].get("technical")),
            **location_data,
            "created_timestamp": convert_timestamp(parsed_data.get("created_timestamp")),
            "skills": parse_skill_list(parsed_data.get("skill_list")),
            "cdi": parsed_data["contract_type"].get("permanent")
        }

        cleaned_data_list.append(cleaned_data)

    return cleaned_data_list


# Read JSON data from file
with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
    json_data = file.read()

# Parse JSON data
parsed_data_list = json.loads(json_data)

# Clean the parsed data
cleaned_data_list = clean_data(parsed_data_list)

# Convert cleaned data to DataFrame
df = pd.DataFrame(cleaned_data_list)

# Filter DataFrame to select rows where profession_title is not an empty dictionary
filtered_df = df[df['profession_title'] != {}]

# Print some columns for validation
print('Description : ', filtered_df.iloc[1]['description'])
print('Description summarized : ', filtered_df.iloc[1]['description_summarized'])

# Write DataFrame to Parquet and CSV files
filtered_df.to_parquet(OUTPUT_PARQUET_FILE_PATH, engine='pyarrow', index=False)
filtered_df.to_csv(OUTPUT_CSV_FILE_PATH, index=False)