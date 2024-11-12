import pandas as pd
from datetime import datetime

def load_and_convert(file_path,output_path):
    """
    Loads data from a CSV file, converts date strings in 'YYYY/MM' format to datetime objects.

    Parameters:
    - file_path (str): Path to the file containing the data.

    Returns:
    - DataFrame: Pandas DataFrame with converted date column.
    """
    # Load data from file
    df = pd.read_csv(file_path)

    # Convert 'month' column to datetime format
    df['month'] = pd.to_datetime(df['month'] + '/01', format='%Y/%m/%d')

    df.to_csv(output_path, index=False)
    print(f"Transformed data saved to {output_path}")

# File path
file_path = '/home/anas-nouri/Documents/meteroloqique/result_monthfes.csv'
output_path = "data.csv"
# Load and process the file
df = load_and_convert(file_path , output_path)

