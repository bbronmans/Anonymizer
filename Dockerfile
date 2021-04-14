# Base image of tensorflow 1.15 as installing tensorflow using pip lacks required dependencies from CUDA/CUDNN
FROM tensorflow/tensorflow:1.15.0-gpu-py3

# Some essentials
RUN apt-get update
RUN apt-get install -y build-essential

# Install required packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy contents of source folder into container
COPY . .

# Run the anonymizer
# ENTRYPOINT ["python","anonymizer/bin/anonymize.py"]