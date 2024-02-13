import json
import pandas as pd
import os

# Specify the folder containing the JSON files
folder_path = "../result"

# Create a list to store extracted data from all files
all_data = []

# Iterate through each JSON file in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.json'):
        file_path = os.path.join(folder_path, file_name)

        # Read JSON data from file
        with open(file_path, 'r', encoding='utf-8') as file:
            json_data = file.read()

        # Load JSON data
        data = json.loads(json_data)

        # Extracting relevant information from all hits in the file
        for hit in data['hits']:
            job_title = hit['seoAlias']
            company_name = hit['smallCompany']['companyName']  # Modify with the correct key for company name
            title=hit.get('title','')
            profession=hit.get('profession', {}).get('langContent', {}).get('en',{}).get('displayName',{})
            salary_info = hit['details'].get('salary', {})
            remote_policy=hit['details'].get('remotePolicy',{})
            required_experience=hit['details'].get('requiredExperience', [])
            team= hit.get('team', {})
            location= hit.get('formattedPlaces', [])
            #skill_list = hit['skillsList']
            #contract_type = hit['contractTypes']  
            createdTimestamp=hit.get('createdAt', '')

            # Extract salary information with default values if the key is missing
         

            skill_list = hit.get('skillsList', [])
            contract_type = hit.get('details', {}).get('contracts', {})
            
            # Create a dictionary with extracted data for the current hit
            output_data = {
                'job title': job_title,
                'company name': company_name,
                'title': title,
                'profession': profession,
                'salary_info':salary_info,
                'remote':remote_policy,
                'required_experience':required_experience,
                'team':team,
                'location':location,
                'createdTimestamp':createdTimestamp,
                'skill List': skill_list,
                'contract Type': contract_type
            }

            # Append the extracted data to the list
            all_data.append(output_data)

# Save all data to a JSON file
output_json_file = 'all_output_data.json'
with open(output_json_file, 'w', encoding='utf-8') as output_file:
    json.dump(all_data, output_file, ensure_ascii=False, indent=4)

# Display the extracted data
for data in all_data:
    print(data)
