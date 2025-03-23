import sys
import pandas as pd
import numpy as np
import os

def exploratory_data_analysis(file_path):
    """
    Perform exploratory data analysis on the preprocessed data.
    """
    try:
        # Check if preprocessed data exists
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found. Please run dpre.py first.")
            return
        
        # Load the preprocessed data
        df = pd.read_csv(file_path)
        
        print("Starting exploratory data analysis...")
        
        # Insight 1: Survival rate by gender
        if 'Sex_male' in df.columns and 'Survived' in df.columns:
            # Calculate survival rates by gender
            # Sex_male=1 means male, Sex_male=0 means female
            survival_by_gender = df.groupby('Sex_male')['Survived'].mean()
            
            # Create insight file
            with open('eda-in-1.txt', 'w') as f:
                f.write("INSIGHT 1: Survival Rates by Gender\n\n")
                f.write(f"Female Survival Rate: {survival_by_gender.get(0, 'N/A'):.2%}\n")
                f.write(f"Male Survival Rate: {survival_by_gender.get(1, 'N/A'):.2%}\n\n")
                
                # Add more detailed analysis
                f.write("Analysis: \n")
                f.write("There is a significant difference in survival rates between genders. ")
                if 0 in survival_by_gender and 1 in survival_by_gender and survival_by_gender[0] > survival_by_gender[1]:
                    f.write("Females had a much higher chance of survival than males, ")
                    f.write(f"with females being {survival_by_gender[0]/survival_by_gender[1]:.1f} times more likely to survive. ")
                    f.write("This aligns with the 'women and children first' protocol followed during the Titanic disaster.")
            
            print("Insight 1 generated: Survival rates by gender")
        
        # Insight 2: Survival rate by passenger class
        if 'Pclass' in df.columns and 'Survived' in df.columns:
            # Calculate survival rates by class
            survival_by_class = df.groupby('Pclass')['Survived'].mean().sort_index()
            
            # Create insight file
            with open('eda-in-2.txt', 'w') as f:
                f.write("INSIGHT 2: Survival Rates by Passenger Class\n\n")
                for p_class, rate in survival_by_class.items():
                    f.write(f"Class {p_class} Survival Rate: {rate:.2%}\n")
                
                # Add more detailed analysis
                f.write("\nAnalysis: \n")
                f.write("There is a clear correlation between passenger class and survival rate. ")
                if len(survival_by_class) >= 3 and survival_by_class[1] > survival_by_class[3]:
                    f.write("First-class passengers had a significantly higher survival rate than third-class passengers, ")
                    f.write(f"approximately {survival_by_class[1]/survival_by_class[3]:.1f} times higher. ")
                    f.write("This suggests that socioeconomic status played a role in who survived the disaster, ")
                    f.write("possibly due to factors like cabin location, access to lifeboats, and priority given to higher-class passengers.")
            
            print("Insight 2 generated: Survival rates by passenger class")
        
        # Insight 3: Survival rate by age group
        if 'AgeGroup' in df.columns and 'Survived' in df.columns:
            # Calculate survival rates by age group
            survival_by_age = df.groupby('AgeGroup')['Survived'].mean()
            
            # Create insight file
            with open('eda-in-3.txt', 'w') as f:
                f.write("INSIGHT 3: Survival Rates by Age Group\n\n")
                for age_group, rate in survival_by_age.items():
                    f.write(f"{age_group} Survival Rate: {rate:.2%}\n")
                
                # Add more detailed analysis
                f.write("\nAnalysis: \n")
                f.write("Age appears to be a factor in survival rates. ")
                if 'Child' in survival_by_age and 'Adult' in survival_by_age:
                    if survival_by_age['Child'] > survival_by_age['Adult']:
                        f.write("Children had a higher survival rate than adults, ")
                        f.write(f"approximately {survival_by_age['Child']/survival_by_age['Adult']:.1f} times higher. ")
                        f.write("This aligns with the 'women and children first' protocol. ")
                    else:
                        f.write("Interestingly, children did not have higher survival rates than adults. ")
                        f.write("This could indicate that the 'women and children first' policy was not strictly followed, ")
                        f.write("or that other factors like class or location on the ship played a more significant role.")
            
            print("Insight 3 generated: Survival rates by age group")
        
        print("Exploratory data analysis completed.")
    
    except Exception as e:
        print(f"Error in exploratory data analysis: {e}")

if __name__ == "__main__":
    # Check if file path is provided
    if len(sys.argv) != 2:
        print("Usage: python3 eda.py <dataset-path>")
        sys.exit(1)
    
    # Get the file path from command line arguments
    file_path = sys.argv[1]
    
    exploratory_data_analysis(file_path) 