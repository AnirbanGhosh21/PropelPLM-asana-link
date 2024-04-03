import pandas as pd
import random
from getpass import getpass

def asana_login():
    # Mock Asana login
    api_key = getpass("Enter your Asana API key: ")
    if api_key == 'test':
        print("Logged in to Asana.")
    else:
        print("Login failed.")

# Function to generate mock ECO data for Asana board
def generate_mock_asana_eco_data(num_ecos):
    eco_data = []
    for i in range(num_ecos):
        eco_number = f'ECO_{i+1}'
        eco_title = f'Mechanical Engineering ECO {i+1}'
        eco_state = random.choice(['Implemented', 'Released'])
        eco_data.append({'Task Name': f'Task {i+1}', 'ECO Number': eco_number, 'State': eco_state})
    return eco_data

# Generate mock ECO data for Asana board
asana_login()
num_ecos = 423
mock_asana_eco_data = generate_mock_asana_eco_data(num_ecos)

# Create DataFrame
mock_asana_eco_df = pd.DataFrame(mock_asana_eco_data)

# Save DataFrame to CSV
mock_asana_eco_df.to_csv('asana_ECOs.csv', index=False)
print(f"Mock ECOs CSV file generated for Asana board with {num_ecos} entries.")
