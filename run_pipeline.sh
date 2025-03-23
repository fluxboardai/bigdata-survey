#!/bin/bash

# Display a message
echo "Executing pipeline inside the container..."

# Change to the working directory
cd /home/doc-bd-a1

# Activate the Python virtual environment
source .venv/bin/activate

echo "Python virtual environment activated."
echo "Running data analysis pipeline..."

# Each python script can invoke the next script in the pipeline
# but for better readability, I've written a separate script for each step
# and added a check to ensure the previous step was successful
# if we want to run the pipeline step by step, we can add os.system() to the end of each script

# Step 1: Load the data
echo "Step 1: Loading data..."
python load.py /home/doc-bd-a1/dataset.csv

# Check if load was successful
if [ ! -f "input_data.csv" ]; then
    echo "Error: Data loading failed. Exiting pipeline."
    exit 1
fi

# Step 2: Preprocess the data
echo "Step 2: Preprocessing data..."
python dpre.py /home/doc-bd-a1/input_data.csv

# Check if preprocessing was successful
if [ ! -f "res_dpre.csv" ]; then
    echo "Error: Data preprocessing failed. Exiting pipeline."
    exit 1
fi

# Step 3: Perform exploratory data analysis
echo "Step 3: Performing exploratory data analysis..."
python eda.py /home/doc-bd-a1/res_dpre.csv

# Check if EDA output files were created
if [ ! -f "eda-in-1.txt" ] || [ ! -f "eda-in-2.txt" ] || [ ! -f "eda-in-3.txt" ]; then
    echo "Warning: Some EDA files are missing, but continuing pipeline."
fi

# Step 4: Create visualization
echo "Step 4: Creating visualization..."
python vis.py /home/doc-bd-a1/res_dpre.csv

# Check if visualization was created
if [ ! -f "vis.png" ]; then
    echo "Warning: Visualization file is missing, but continuing pipeline."
fi

# Step 5: Run K-means clustering
echo "Step 5: Running K-means clustering..."
python model.py /home/doc-bd-a1/res_dpre.csv

# Check if clustering results were created
if [ ! -f "k.txt" ]; then
    echo "Warning: K-means result file is missing, but continuing pipeline."
fi

echo "Pipeline completed successfully."

# Deactivate the Python virtual environment
deactivate
