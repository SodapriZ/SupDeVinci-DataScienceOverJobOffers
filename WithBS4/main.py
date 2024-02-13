import os

# Define the directory names
directories = ['01_GetDataFromJobOffersWithBS4', '02_ParseDataFromJobOffers', '03_CleanDataFromJobOffers']

# Loop through each directory
for directory in directories:
    # Get the list of Python files in the directory
    files = [f for f in os.listdir(directory) if f.endswith('.py')]
    
    # Loop through each Python file and execute it
    for file in files:
        file_path = os.path.join(directory, file)
        print(f"Executing {file_path}...")
        os.system(f"python {file_path}")
