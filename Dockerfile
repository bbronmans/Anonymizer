# Base image of tensorflow 1.15 as installing tensorflow using pip lacks required dependencies from CUDA/CUDNN
FROM tensorflow/tensorflow:1.15.0-gpu-py3


# Update GPG keys from nvidia
# RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub

# Some essentials to install other packages
RUN apt-get update
RUN apt-get install -y build-essential

# TODO: Kijken of dit werkt
RUN git clone https://github.com/bbronmans/Anonymizer.git/

# Install required packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy contents of source folder into container
COPY . .

# Run the anonymizer
CMD ["python","-u", "anonymizer//bin//anonymize.py"]