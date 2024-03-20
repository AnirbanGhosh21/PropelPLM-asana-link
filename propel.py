import asana
from simple_salesforce import Salesforce
import pandas as pd

def authenticate_salesforce(username, password, security_token):
    # Salesforce authentication
    sf = Salesforce(username=username, password=password, security_token=security_token)
    if sf.authenticated():
        return sf
    else:
        print("Failed to authenticate with Salesforce.")
        return None

def authenticate_asana(api_key):
    # Authenticating with Asana
    client = asana.Client.access_token(api_key)
    return client

def fetch_ecos_from_salesforce(sf):
    # SOQL query to fetch ECOs
    query = "SELECT Id, PDLM__Name, PDLM__Title, PDLM__State__c FROM PDLM__ECO__c"
    result = sf.query_all(query)
    return result['records']

def fetch_tasks_from_asana(client, project_id):
    # Fetching tasks from Asana project
    tasks = client.tasks.find_by_project(project_id, opt_fields=["name", "notes"])
    return tasks

def create_eco_dataframe(ecos):
    if not ecos:
        return None

    # Extract relevant information from fetched data and create a DataFrame
    eco_data = []
    for eco in ecos:
        eco_id = eco['Id']
        eco_number = eco['PDLM__Name']
        eco_title = eco['PDLM__Title']
        eco_state = eco['PDLM__State__c'] if 'PDLM__State__c' in eco else None

        eco_data.append({'ID': eco_id, 'Number': eco_number, 'Title': eco_title, 'State': eco_state})

    eco_df = pd.DataFrame(eco_data)
    return eco_df

def create_task_dataframe(tasks):
    # Create DataFrame from fetched tasks with ECO details
    task_data = []
    for task in tasks:
        eco_number, state, description = get_task_eco_details(task)
        task_data.append({'Task Name': task['name'], 'ECO Number': eco_number, 'State': state, 'Description': description})
    task_df = pd.DataFrame(task_data)
    return task_df

def get_task_eco_details(task):
    # Extracting ECO number, state, and description from task notes
    eco_number = None
    state = None
    description = None
    
    if 'notes' in task:
        notes = task['notes']
        # Parse notes to extract ECO number, state, and description (if available)
        # You need to implement your parsing logic here based on how your ECO information is structured in task notes

    return eco_number, state, description

def compare_eco_states(salesforce_df, asana_df):
    # Compare ECO states between Salesforce and Asana DataFrames
    conflicting_states = pd.merge(salesforce_df, asana_df, on='ECO Number', suffixes=('_sf', '_asana'), how='inner')
    conflicting_states = conflicting_states[conflicting_states['State_sf'] != conflicting_states['State_asana']]
    return conflicting_states

def main():
    # User input for Salesforce and Asana credentials
    username = input("Enter your Salesforce and Asana username: ")
    password = input("Enter your Salesforce and Asana password: ")
    security_token = input("Enter your Salesforce security token: ")
    asana_api_key = input("Enter your Asana API key: ")
    project_id = input("Enter Asana project ID: ")

    # Authenticate with Salesforce
    sf = authenticate_salesforce(username, password, security_token)
    client = authenticate_asana(asana_api_key)

    if sf and client:
        # Fetch ECOs from Salesforce
        ecos_salesforce = fetch_ecos_from_salesforce(sf)
        ecos_asana_tasks = fetch_tasks_from_asana(client, project_id)

        if ecos_salesforce and ecos_asana_tasks:
            # Create DataFrames from fetched ECOs
            salesforce_df = create_eco_dataframe(ecos_salesforce)
            asana_df = create_task_dataframe(ecos_asana_tasks)

            # Compare ECO states between Salesforce and Asana DataFrames
            conflicting_states = compare_eco_states(salesforce_df, asana_df)

            if not conflicting_states.empty:
                print("Conflicting ECO States:")
                print(conflicting_states)
                
                # Export comparison DataFrame to CSV
                conflicting_states.to_csv('conflicting_eco_states.csv', index=False)
                print("Comparison DataFrame exported to 'conflicting_eco_states.csv'.")
            else:
                print("No conflicting ECO states found.")
        else:
            print("Failed to fetch ECOs from Salesforce or tasks from Asana.")
    else:
        print("Authentication failed.")

if __name__ == "__main__":
    main()