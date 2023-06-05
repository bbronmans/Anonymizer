# Base image of tensorflow 1.15 as installing tensorflow using pip lacks required dependencies from CUDA/CUDNN
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

# Some essentials to install other packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y build-essential

# Install Python 3.11 and git
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.11 \
    python3-pip \
    git \
    && \
    apt-get clean && \
    rm -rf \var\lib\apt\lists\*

# Get the anonymizer code
RUN mkdir -p anon
RUN git clone https://github.com/bbronmans/Anonymizer.git/ ./anon/
RUN mv ./anon/* .
RUN mv -f ./anon/.[!.]* .

# Install required packages
RUN pip3 install --upgrade pip
RUN python3 -m pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Create symlink between python3 and python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Run the anonymizer
CMD ["python","-u", "anonymizer//bin//anonymize.py"]