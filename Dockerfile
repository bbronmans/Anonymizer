# Base image of tensorflow 1.15 as installing tensorflow using pip lacks required dependencies from CUDA/CUDNN
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

# Some essentials to install other packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y build-essential

# TODO: Kijken of dit werkt
# RUN git clone https://github.com/bbronmans/Anonymizer.git/

# Install Python 3.11
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    && \
    apt-get clean && \
    rm -rf \var\lib\apt\lists\*

# Install required packages
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN python3 -m pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Create symlink between python3 and python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copy contents of source folder into container
COPY . .

# Run the anonymizer
CMD ["python","-u", "anonymizer//bin//anonymize.py"]
