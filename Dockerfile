# Base image of tensorflow 1.11 as installing tensorflow using pip lacks required dependencies from CUDA/CUDNN
FROM tensorflow/tensorflow:1.11.0-devel-gpu-py3

# Some essentials
RUN apt-get update
RUN apt-get install -y build-essential make

# Install required packages
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Some weird steps to fix a bug and ensure the GPU can be used/tensorflow doesn't crash
RUN ln -s /usr/local/cuda/lib64/stubs/libcuda.so /usr/local/cuda/lib64/stubs/libcuda.so.1
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/cuda/lib64/stubs:/usr/local/cuda-9.0/lib64:/usr/local/cuda-9.0/lib64/stubs:/usr/local/cuda/extras/CUPTI/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64

# Copy contents of source folder into container
COPY . .

# Run the anonymizer
#RUN python anonymizer/bin/anonymize.py --input ./images --image-output ./output --weights ./weights --plate-threshold 0.1
#CMD ["python", "anonymizer/bin/anonymize.py", "--input ./images --image-output ./output --weights ./weights --plate-threshold 0.1"]
ENTRYPOINT ["python","anonymizer/bin/anonymize.py"]