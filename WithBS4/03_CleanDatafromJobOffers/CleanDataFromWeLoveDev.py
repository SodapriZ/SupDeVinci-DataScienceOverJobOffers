import json
import pandas as pd
from datetime import datetime
import pyarrow.parquet as pq

def convert_timestamp(timestamp_ms):
    if timestamp_ms:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    return None

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
            "required_experience": parsed_data.get("required_experience"),
            "team_management_description": parsed_data["team_description"].get("management"),
            "team_technical_description": parsed_data["team_description"].get("technical"),
            **location_data,
            "created_timestamp": convert_timestamp(parsed_data.get("created_timestamp")),
            "skills": parse_skill_list(parsed_data.get("skill_list")),
            "cdi": parsed_data["contract_type"].get("permanent")
        }

        cleaned_data_list.append(cleaned_data)
    
    return cleaned_data_list

# Read JSON data from file
file_path = "./result/we_love_dev-parsed_data.json"
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = file.read()

# Parse JSON data
parsed_data_list = json.loads(json_data)

# Clean the parsed data
cleaned_data_list = clean_data(parsed_data_list)

# Convert cleaned data to DataFrame
df = pd.DataFrame(cleaned_data_list)

# Filter DataFrame to select rows where profession_title is not an empty dictionary
filtered_df = df[df['profession_title'].apply(lambda x: isinstance(x, dict) and bool(x))]


# Write DataFrame to Parquet file
output_file_path = "./result/we_love_dev-cleaned_data.parquet"
filtered_df.to_parquet(output_file_path, engine='pyarrow', index=False)