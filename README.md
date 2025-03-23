# Big Data Assignment 1: Titanic Dataset Analysis

This project implements a data analysis pipeline for the Titanic dataset using Docker. The pipeline includes data loading, preprocessing, exploratory data analysis, visualization, and K-means clustering.

## Project Structure

```
bd-a1/
├── Dockerfile          # Dockerfile to build the container
├── requirements.txt    # Python package requirements
├── dataset.csv         # The Titanic dataset
├── README.md           # This README file
├── final.sh            # Script to run pipeline from host machine
├── run_pipeline.sh     # Script to run pipeline inside the container
└── service-result/     # Directory where results will be stored
```

Inside the container, the following Python scripts will be created:
- `load.py`: Loads the dataset from a user-provided path
- `dpre.py`: Performs data preprocessing (cleaning, transformation, reduction, discretization)
- `eda.py`: Performs exploratory data analysis
- `vis.py`: Creates visualizations
- `model.py`: Implements K-means clustering

For demonstration purposes, the files are created and copied to the container.

## Setup and Execution Instructions

### 1. The Dockerfile

- Uses Ubuntu 22.04 as the base image
- Installs Python3, pip, and virtual environment support
- Creates a Python virtual environment to avoid "externally managed environment" issues
- Copies requirements.txt and the dataset into the container
- Installs required Python packages from requirements.txt in the virtual environment
- Creates the necessary directory structure
- Sets the working directory to /home/doc-bd-a1

### 2. Execute the Pipeline

To execute the complete pipeline, simply run the final.sh script:

```bash
./final.sh
```

The final.sh script will:
1. Build the Docker image if it doesn't exist
2. Create and run the Docker container with appropriate volume mounts
3. Copy all necessary files to the container
4. Execute the pipeline inside the container
5. Verify the pipeline execution completed successfully
6. Stop and remove the container when done

All results will be available in the `bd-a1/service-result/` directory on your host machine.

### 5. Check Results

After the pipeline completes, you can check the results in the `bd-a1/service-result/` directory on your host machine, which should contain:
- `res_dpre.csv`: Preprocessed dataset
- `eda-in-1.txt`, `eda-in-2.txt`, `eda-in-3.txt`: Exploratory data analysis insights
- `vis.png`: Visualization
- `k.txt`: K-means clustering results

### 6. Stop the Container

If the container is still running, you can stop it manually:

```bash
docker stop titanic-container
```

To remove the container when you're done:

```bash
docker rm titanic-container
```

## Notes

- The Docker container must be built with access to the internet to install required packages.
- If you need to modify any files after starting the pipeline, you can access the container with:
  ```bash
  docker exec -it titanic-container bash
  ```
- All Python files in this pipeline are independent modules that perform specific tasks in the data analysis process.
- The final.sh script runs on your local machine and coordinates the execution of the pipeline inside the container.
- The run_pipeline.sh script runs inside the container and executes all Python scripts in sequence.
- The requirements.txt file specifies exact versions of the Python packages to ensure reproducibility.
- A Python virtual environment is created inside the container to avoid "externally managed environment" issues in newer Ubuntu versions. 