import sys
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os

def implement_kmeans(file_path):
    """
    Implement K-means clustering on the preprocessed data.
    """
    try:
        # Check if preprocessed data exists
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found. Please run dpre.py first.")
            return
        
        # Load the preprocessed data
        df = pd.read_csv(file_path)
        
        print("Starting K-means clustering...")
        
        # Select numerical features for clustering
        # Exclude target variable (Survived) and categorical variables
        numerical_cols = [col for col in df.columns if df[col].dtype in ['int64', 'float64']]
        
        # Exclude any categorical columns that were encoded as numbers but shouldn't be used for distance calculation
        exclude_cols = ['Survived']
        features = [col for col in numerical_cols if col not in exclude_cols and '_' not in col]
        
        # Make sure we have features to work with
        if not features:
            print("Error: No suitable numerical features found for clustering.")
            return
            
        # Print the features being used
        print(f"Using the following features for clustering: {features}")
        
        # Extract features for clustering
        X = df[features].copy()
        
        # Handle missing values if any
        X.fillna(X.mean(), inplace=True)
        
        # Standardize the features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Apply K-means clustering with k=3
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['cluster'] = kmeans.fit_predict(X_scaled)
        
        # Count records in each cluster
        cluster_counts = df['cluster'].value_counts().sort_index()
        
        # Save cluster counts to k.txt
        with open('k.txt', 'w') as f:
            f.write("K-means Clustering Results (k=3)\n\n")
            for cluster_id, count in cluster_counts.items():
                f.write(f"Cluster {cluster_id}: {count} records\n")
            
            # Add some characteristics about each cluster
            f.write("\nCluster Characteristics:\n")
            
            # Calculate mean values for each feature in each cluster
            cluster_means = df.groupby('cluster')[features].mean()
            
            for cluster_id in range(3):
                f.write(f"\nCluster {cluster_id} mean values:\n")
                for feature in features:
                    f.write(f"  {feature}: {cluster_means.loc[cluster_id, feature]:.2f}\n")
            
            # Calculate survival rate for each cluster if 'Survived' is in the dataframe
            if 'Survived' in df.columns:
                survival_rates = df.groupby('cluster')['Survived'].mean()
                f.write("\nSurvival rates by cluster:\n")
                for cluster_id in range(3):
                    f.write(f"  Cluster {cluster_id}: {survival_rates.loc[cluster_id]:.2%}\n")
        
        print("K-means clustering completed. Results saved to k.txt")
        
    except Exception as e:
        print(f"Error in K-means clustering: {e}")

if __name__ == "__main__":
    # Check if file path is provided
    if len(sys.argv) != 2:
        print("Usage: python3 model.py <dataset-path>")
        sys.exit(1)
    
    # Get the file path from command line arguments
    file_path = sys.argv[1]
    implement_kmeans(file_path) 