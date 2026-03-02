import pandas as pd

def remove_duplicates_from_excel(input_file, output_file):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(input_file)
    
    # Initialize a set to keep track of unique addresses
    unique_addresses = set()
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        address = row['address']
        names = str(row['name']).split(',') if pd.notna(row['name']) else []
        
        # Convert names to set to remove duplicates
        unique_names = list(set(names))
        
        # Convert back to string with comma separation
        df.at[index, 'name'] = ', '.join(unique_names)
        
        # Check if address is unique, keep the first occurrence
        if address in unique_addresses:
            df.at[index, 'address'] = None  # Mark for removal
        else:
            unique_addresses.add(address)
    
    # Drop rows with Address marked as None
    df = df.dropna(subset=['address'])
    
    # Write the cleaned DataFrame back to a new Excel file
    print(f'Writing')
    df.to_excel(output_file, index=False)

# Example usage:
input_file = 'Before.xlsx'
output_file = 'After.xlsx'

remove_duplicates_from_excel(input_file, output_file)
