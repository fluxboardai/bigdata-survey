import sys
import pandas as pd
import os

def load_data(file_path):
    """
    Load the dataset from the provided file path.
    
    Args:
        file_path (str): Path to the dataset file.
        
    Returns:
        pd.DataFrame: Loaded dataframe
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} does not exist.")
            sys.exit(1)
            
        # Load the data
        df = pd.read_csv(file_path)
        
        print(f"Dataset loaded successfully from {file_path}")
        print(f"Shape of the dataset: {df.shape}")
        print("First few rows of the dataset:")
        print(df.head())
        
        # Pass data to the next step in the pipeline
        df.to_csv('input_data.csv', index=False)
        
        print("Data saved to input_data.csv for further processing")
        
        return df
    
    except Exception as e:
        print(f"Error loading the dataset: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if file path is provided
    if len(sys.argv) != 2:
        print("Usage: python3 load.py <dataset-path>")
        sys.exit(1)
    
    # Get the file path from command line arguments
    file_path = sys.argv[1]
    
    # Load the data
    load_data(file_path) 