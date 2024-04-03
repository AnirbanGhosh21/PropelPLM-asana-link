import pandas as pd
import random
from getpass import getpass

def propel_login():
    # Mock propel login
    username = getpass("Enter your Salesforce username: ")
    password = getpass("Enter your Salesforce password: ")
    api_key = getpass("Enter your Asana API key: ")
    if api_key == 'test' and username == 'anirban' and password == 'password':
        print("Logged in to Salesforce.")
    else:
        print("Login failed.")
    
# Function to generate mock ECO data
def generate_mock_eco_data(num_ecos):
    eco_data = []
    for i in range(num_ecos):
        eco_number = f'ECO_{i+1}'
        eco_title = f'Mechanical Engineering ECO {i+1}'
        eco_state = random.choice(['Define Change', 'Update Items', 'CCB', 'Released', 'Implemented'])
        eco_data.append({'ID': i+1, 'ECO Number': eco_number, 'Title': eco_title, 'State': eco_state})
    return eco_data

# Generate mock ECO data
propel_login()
num_ecos = 2063
mock_eco_data = generate_mock_eco_data(num_ecos)

# Create DataFrame
mock_eco_df = pd.DataFrame(mock_eco_data)

# Save DataFrame to CSV
mock_eco_df.to_csv('Propel_ECOs.csv', index=False)
print(f"Mock ECOs CSV file generated with {num_ecos} entries.")