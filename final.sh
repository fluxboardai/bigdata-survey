#!/bin/bash

# Display a message
echo "Executing final.sh script..."
echo "This script will connect to the Docker container, run the pipeline, and copy the results."

# Name of the Docker container and image
CONTAINER_NAME="titanic-container"
IMAGE_NAME="titanic-analysis"

# Ensure service-result directory exists locally
mkdir -p service-result

# Check if the Docker image exists
if ! docker images -q "$IMAGE_NAME" | grep -q .; then
    echo "Docker image '$IMAGE_NAME' not found. Building it now..."
    docker build -t "$IMAGE_NAME" .
fi

# Check if the container is running
if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
    echo "Container '$CONTAINER_NAME' is running."
else
    # Check if the container exists but is stopped
    if docker ps -aq -f name=$CONTAINER_NAME | grep -q .; then
        echo "Starting existing container '$CONTAINER_NAME'..."
        docker start "$CONTAINER_NAME"
    else
        echo "Creating and starting new container '$CONTAINER_NAME'..."
        docker run -d --name "$CONTAINER_NAME" -v "$(pwd)/service-result:/bd-a1/service-result" titanic-analysis
    fi
fi

# Execute the pipeline script inside the container
echo "Executing the pipeline script inside the container..."
docker exec $CONTAINER_NAME /home/doc-bd-a1/run_pipeline.sh

# Check if the pipeline execution was successful
if [ $? -ne 0 ]; then
    echo "Error: Pipeline execution failed."
    exit 1
fi

# Copy results from the container to the local service-result directory
echo "Copying output files from container to local service-result directory..."

# Copy output files from container to local machine
docker exec $CONTAINER_NAME bash -c 'mkdir -p /bd-a1/service-result && cp /home/doc-bd-a1/res_dpre.csv /home/doc-bd-a1/eda-in-*.txt /home/doc-bd-a1/vis.png /home/doc-bd-a1/k.txt /bd-a1/service-result/'

echo "Files should now be available in your local bd-a1/service-result/ directory."

# Stop the container
echo "Stopping Docker container '$CONTAINER_NAME'..."
docker stop $CONTAINER_NAME
echo "Container stopped."

echo "final.sh script execution completed." 