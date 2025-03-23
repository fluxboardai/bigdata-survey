# Use Ubuntu 22.04 as the base image - more stable for our use case
FROM ubuntu:22.04

# Install necessary packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

# Create the directory inside the container
RUN mkdir -p /home/doc-bd-a1

# Copy the requirements file and dataset into the container
COPY requirements.txt /home/doc-bd-a1/
COPY dataset.csv /home/doc-bd-a1/
COPY run_pipeline.sh /home/doc-bd-a1/
COPY load.py /home/doc-bd-a1/
COPY dpre.py /home/doc-bd-a1/
COPY eda.py /home/doc-bd-a1/
COPY model.py /home/doc-bd-a1/
COPY vis.py /home/doc-bd-a1/

# Make the run_pipeline.sh script executable
RUN chmod +x /home/doc-bd-a1/run_pipeline.sh


# Set the working directory
WORKDIR /home/doc-bd-a1
# Create and activate a virtual environment
RUN python3 -m venv /home/doc-bd-a1/.venv
ENV PATH="/home/doc-bd-a1/.venv/bin:$PATH"

# Install required Python packages from requirements.txt in the virtual environment
RUN pip3 install -r requirements.txt

# Open bash upon startup
CMD ["/bin/bash"] 