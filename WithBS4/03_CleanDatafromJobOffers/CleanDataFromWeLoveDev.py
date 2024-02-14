import json
import pandas as pd
from datetime import datetime
import pyarrow.parquet as pq

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import ne_chunk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

import spacy


nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

# Load the English language model
nlp = spacy.load('fr_core_news_sm') 

def convert_timestamp(timestamp_ms):
    if timestamp_ms:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return None

def preprocess_text(text):
    if text :
        # Tokenize text
        tokens = word_tokenize(text)
        # Remove punctuation and lowercase
        tokens = [word.lower() for word in tokens if word.isalnum()]
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if not word in stop_words]
        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        return ' '.join(tokens)
    else :
        return ''

def extract_named_entities(text):
    if text:
        # Process the text with spaCy
        doc = nlp(text)
        # Extract named entities
        named_entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'DATE', 'GPE', 'EVENT', 'PERSON']]
        return named_entities
    else:
        return []

# Function to add named entities to DataFrame
def add_named_entities(text):
    named_entities = extract_named_entities(text)
    return ', '.join(named_entities)


def parse_skill_list(skill_list):
    if skill_list:
        # Sort the skill list by value in descending order
        sorted_skills = sorted(skill_list, key=lambda x: x['value'], reverse=True)
        
        # Extract skill names
        skill_names = [skill['name'] for skill in sorted_skills]
        
        # Construct the string by joining skill names
        skills_string = '/'.join(skill_names)
        
        return skills_string
    return None

def parse_location(location):
    if location:
        city, country = location[0].split(", ")
        return {"city": city, "country": country}
    return {"city": None, "country": None}

def categorize_experience(experience):
    if experience <= 3:
        return '[0-3]'
    elif experience <= 7:
        return '[3-7]'
    else:
        return '[+7]'

def clean_data(parsed_data_list):
    cleaned_data_list = []
    for parsed_data in parsed_data_list:
        location_data = parse_location(parsed_data.get("location"))

        cleaned_data = {
            "company_name": parsed_data.get("company_name"),
            "job_offer_title": parsed_data.get("job_offer_title"),
            "profession_title": parsed_data.get("profession_title"),
            "description": parsed_data.get("description"),
            "salary_max": parsed_data["salary_info"].get("max"),
            "salary_avg": (parsed_data["salary_info"].get("max", 0) + parsed_data["salary_info"].get("min", 0)) / 2,
            "salary_min": parsed_data["salary_info"].get("min"),
            "remote_quantity": parsed_data["remote_policy"].get("daysPerWeek"),
            "job_format": parsed_data["remote_policy"].get("frequency"),
            "required_experience": int(parsed_data.get("required_experience")),
            "required_experience_category":categorize_experience(int(parsed_data.get("required_experience"))),
            "team_management_description": parsed_data["team_description"].get("management"),
            "team_management_description_processed": preprocess_text(parsed_data["team_description"].get("management")),
            "team_management_description_entities": add_named_entities(preprocess_text(parsed_data["team_description"].get("management"))),
            "team_technical_description": parsed_data["team_description"].get("technical"),
            "team_technical_description_processed": preprocess_text(parsed_data["team_description"].get("technical")),
            "team_technical_description_entities": add_named_entities(preprocess_text(parsed_data["team_description"].get("technical"))),
            **location_data,
            "created_timestamp": convert_timestamp(parsed_data.get("created_timestamp")),
            "skills": parse_skill_list(parsed_data.get("skill_list")),
            "cdi": parsed_data["contract_type"].get("permanent")
        }

        cleaned_data_list.append(cleaned_data)
    
    return cleaned_data_list

# Read JSON data from file
file_path = "./results/we_love_dev-parsed_data.json"
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = file.read()

# Parse JSON data
parsed_data_list = json.loads(json_data)

# Clean the parsed data
cleaned_data_list = clean_data(parsed_data_list)

# Convert cleaned data to DataFrame
df = pd.DataFrame(cleaned_data_list)

# Filter DataFrame to select rows where profession_title is not an empty dictionary
filtered_df = df[df['profession_title'] != {}]

# print('Job Offers DataFrame : ',filtered_df.head(5))
print('Description Full : ',filtered_df.iloc[1]['team_management_description'])
print('Description Processed : ',filtered_df.iloc[1]['team_management_description_processed'])
print('Description Entity : ',filtered_df.iloc[1]['team_management_description_entities'])
# print('Job Offers DataFrame : ',filtered_df.iloc[1]['team_technical_description'])

# Write DataFrame to Parquet file
output_parquet_file_path = "./results/we_love_dev-cleaned_data.parquet"
output_csv_file_path = "./results/we_love_dev-cleaned_data.csv"
filtered_df.to_parquet(output_parquet_file_path, engine='pyarrow', index=False)
filtered_df.to_csv(output_csv_file_path, index=False)