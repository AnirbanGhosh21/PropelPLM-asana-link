import pandas as pd

# Function to load and filter data from CSVs
def compare_eco_states(sf_csv_path, asana_csv_path):
    # Load data from CSVs
    sf_df = pd.read_csv(sf_csv_path)
    asana_df = pd.read_csv(asana_csv_path)

    # Filter rows where state is 'released' on Salesforce and 'implemented' on Asana
    filtered_ecos = pd.merge(sf_df[sf_df['State'] == 'Released'], asana_df[asana_df['State'] == 'Implemented'], on='ECO Number', how='inner')

    return filtered_ecos

# Paths to the CSV files
sf_csv_path = 'mock data generator/Propel_ECOs.csv'
asana_csv_path = 'mock data generator/asana_ECOs.csv'

# Compare ECO states between CSVs
filtered_ecos = compare_eco_states(sf_csv_path, asana_csv_path)

# Print the filtered ECOs
print("Filtered ECOs:")
print(filtered_ecos)
filtered_ecos.to_csv('Compared_ECOs.csv', index=False)