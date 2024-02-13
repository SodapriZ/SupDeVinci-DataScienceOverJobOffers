import json
import pandas as pd
import os

# Specify the folder containing the JSON files
folder_path = "./result"
file_name = "we_love_dev-output_from_bs4.json"
# Iterate through each JSON file in the folder
file_path = os.path.join(folder_path, file_name)

# Read JSON data from file
with open(file_path, 'r', encoding='utf-8') as file:
    json_data = file.read()

# Load JSON data
data = json.loads(json_data)

# Create a list to store extracted data from all files
all_data = []
# Extracting relevant information from all hits in the file
for hit in data['hits']:

    output_data = {
        'job_title':hit.get('seoAlias',''),
        'company_name':hit.get('smallCompany', {}).get('companyName', ''),
        'job_offer_title':hit.get('title',''),
        'profession_title':hit.get('profession', {}).get('langContent', {}).get('en',{}).get('displayName',{}),
        'description':hit.get('mdDescription',''),
        'salary_info':hit.get('details').get('salary', {}),
        'remote_policy':hit.get('details').get('remotePolicy',{}),
        'required_experience':hit.get('details').get('requiredExperience', []),
        'team_description':hit.get('team', {}),
        'location':hit.get('formattedPlaces', []),
        'created_timestamp':hit.get('createdAt', ''),
        'skill_list': hit.get('skillsList', []),
        'contract_type': hit.get('details', {}).get('contracts', {})
    }
    
    all_data.append(output_data)

# Save all data to a JSON file
output_json_file = './result/we_love_dev-parsed_data.json'
with open(output_json_file, 'w+', encoding='utf-8') as output_file:
    json.dump(all_data, output_file, ensure_ascii=False, indent=4)