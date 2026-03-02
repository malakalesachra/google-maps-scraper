import os
import pandas as pd

def compile_excel_files(input_folder='output', output_file='compiled_google_maps_data.xlsx'):
    # Create a list to hold all the dataframes
    all_data = []

    # Get a list of all Excel files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(input_folder, file_name)
            # Read the Excel file into a dataframe
            df = pd.read_excel(file_path)
            # Append the dataframe to the list
            all_data.append(df)

    # Concatenate all the dataframes in the list into a single dataframe
    combined_df = pd.concat(all_data, ignore_index=True)

    # Check for duplicate rows based on 'address' column
    duplicate_rows = combined_df[combined_df.duplicated(subset=['address'], keep=False)]
    num_duplicates = len(duplicate_rows)

    # Save the combined dataframe to a new Excel file
    combined_df.to_excel(output_file, index=False)
    print(f"Compiled data has been saved to {output_file}")

    # Print number of duplicate rows based on 'address'
    print(f"Number of duplicate rows based on 'address': {num_duplicates}")

if __name__ == "__main__":
    compile_excel_files()