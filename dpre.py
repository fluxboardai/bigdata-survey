import pandas as pd
import numpy as np
import os
import sys

def clean_data(df):
    """
    Clean the dataset by handling missing values.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    # Make a copy to avoid warning
    df_clean = df.copy()
    
    # Handle missing values
    # Fill missing age with median
    df_clean['Age'] = df_clean['Age'].fillna(df_clean['Age'].median())
    
    # Fill missing embarked with most common value
    df_clean['Embarked'] = df_clean['Embarked'].fillna(df_clean['Embarked'].mode()[0])
    
    # Drop Cabin column as it has too many missing values
    df_clean = df_clean.drop('Cabin', axis=1)
    
    print("Data cleaning completed")
    return df_clean

def transform_data(df):
    """
    Transform the dataset by creating new features and encoding categorical variables.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Transformed dataframe
    """
    # Make a copy
    df_transform = df.copy()
    
    # Create new features
    
    # Family size
    df_transform['FamilySize'] = df_transform['SibSp'] + df_transform['Parch'] + 1
    
    # Is alone
    df_transform['IsAlone'] = (df_transform['FamilySize'] == 1).astype(int)
    
    # Extract title from name
    df_transform['Title'] = df_transform['Name'].str.extract(' ([A-Za-z]+)\.', expand=False)
    
    # Map titles to smaller categories
    title_mapping = {
        'Mr': 'Mr',
        'Miss': 'Miss',
        'Mrs': 'Mrs',
        'Master': 'Master',
        'Dr': 'Rare',
        'Rev': 'Rare',
        'Col': 'Rare',
        'Major': 'Rare',
        'Mlle': 'Miss',
        'Countess': 'Rare',
        'Ms': 'Miss',
        'Lady': 'Rare',
        'Jonkheer': 'Rare',
        'Don': 'Rare',
        'Dona': 'Rare',
        'Mme': 'Mrs',
        'Capt': 'Rare',
        'Sir': 'Rare'
    }
    
    df_transform['Title'] = df_transform['Title'].map(lambda x: title_mapping.get(x, 'Rare'))
    
    # One-hot encoding for categorical variables
    df_transform = pd.get_dummies(df_transform, columns=['Sex', 'Embarked', 'Title'], drop_first=True)
    
    # Drop unnecessary columns
    df_transform = df_transform.drop(['Name', 'Ticket', 'PassengerId'], axis=1)
    
    print("Data transformation completed")
    return df_transform

def reduce_data(df):
    """
    Reduce the dataset by selecting important features.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Reduced dataframe
    """
    # For simplicity, we'll just select a subset of columns
    # In a real-world scenario, you would use dimensionality reduction techniques like PCA
    
    # Keep only the most relevant features
    important_features = [
        'Survived', 'Pclass', 'Age', 'Fare', 'FamilySize', 'IsAlone',
        'Sex_male', 'Embarked_Q', 'Embarked_S', 'Title_Miss', 'Title_Mr', 'Title_Mrs', 'Title_Rare'
    ]
    
    # Select columns that exist in the dataframe
    selected_features = [col for col in important_features if col in df.columns]
    
    df_reduced = df[selected_features]
    
    print("Data reduction completed")
    return df_reduced

def discretize_data(df):
    """
    Discretize continuous variables in the dataset.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Discretized dataframe
    """
    # Make a copy
    df_discrete = df.copy()
    
    # Discretize Age
    df_discrete['AgeGroup'] = pd.cut(
        df_discrete['Age'],
        bins=[0, 12, 18, 35, 60, 100],
        labels=['Child', 'Teenager', 'Young Adult', 'Adult', 'Senior']
    )
    
    # Discretize Fare
    df_discrete['FareCategory'] = pd.qcut(
        df_discrete['Fare'],
        q=4,
        labels=['Low', 'Medium-Low', 'Medium-High', 'High']
    )
    
    # Discretize FamilySize
    df_discrete['FamilySizeCategory'] = pd.cut(
        df_discrete['FamilySize'],
        bins=[0, 1, 3, 10],
        labels=['Alone', 'Small', 'Large']
    )
    
    # Drop the original continuous columns if needed for certain analyses
    # For now we'll keep them
    
    print("Data discretization completed")
    return df_discrete

def data_preprocessing(file_path):
    """
    Main function to perform data preprocessing.
    """
    try:
        # Load the dataset
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
        else:
            print(f"Error: {file_path} not found. Please run load.py first.")
            return
        
        print("Starting data preprocessing...")
        
        # Data Cleaning
        df_cleaned = clean_data(df)
        
        # Data Transformation
        df_transformed = transform_data(df_cleaned)
        
        # Data Reduction
        df_reduced = reduce_data(df_transformed)
        
        # Data Discretization
        df_final = discretize_data(df_reduced)
        
        # Save the preprocessed data
        df_final.to_csv('res_dpre.csv', index=False)
        
        print("Data preprocessing completed. Results saved to res_dpre.csv")
        
    except Exception as e:
        print(f"Error in data preprocessing: {e}")

if __name__ == "__main__":
    # Check if file path is provided
    if len(sys.argv) != 2:
        print("Usage: python3 dpre.py <dataset-path>")
        sys.exit(1)
    
    # Get the file path from command line arguments
    data_preprocessing(sys.argv[1]) 