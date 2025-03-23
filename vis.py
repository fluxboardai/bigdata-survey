import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualization():
    """
    Create visualization from the preprocessed data.
    """
    try:
        # Check if preprocessed data exists
        if not os.path.exists('res_dpre.csv'):
            print("Error: res_dpre.csv not found. Please run dpre.py first.")
            return
        
        # Load the preprocessed data
        df = pd.read_csv('res_dpre.csv')
        
        print("Starting visualization...")
        
        # Set the style for the plots
        sns.set_style('whitegrid')
        plt.figure(figsize=(12, 8))
        
        # Create a visualization that shows survival rates by passenger class and gender
        if all(col in df.columns for col in ['Pclass', 'Sex_male', 'Survived']):
            # Create a new column for gender (for readability)
            df['Gender'] = df['Sex_male'].map({1: 'Male', 0: 'Female'})
            
            # Create a grouped bar chart
            ax = sns.barplot(x='Pclass', y='Survived', hue='Gender', data=df, errorbar=None)
            
            # Add title and labels
            plt.title('Survival Rate by Passenger Class and Gender', fontsize=16)
            plt.xlabel('Passenger Class', fontsize=12)
            plt.ylabel('Survival Rate', fontsize=12)
            
            # Add annotations
            for container in ax.containers:
                ax.bar_label(container, fmt='%.2f')
            
            # Add a note
            plt.figtext(0.5, 0.01, 'Note: Survival Rate represents the proportion of passengers who survived.', 
                        ha='center', fontsize=10, style='italic')
            
            # Save the figure
            plt.tight_layout()
            plt.savefig('vis.png')
            plt.close()
            
            print("Visualization created and saved as vis.png")
        else:
            print("Required columns for visualization not found in the dataset.")
        
    except Exception as e:
        print(f"Error in creating visualization: {e}")

if __name__ == "__main__":
    create_visualization() 