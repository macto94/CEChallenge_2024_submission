# Pull an image that already had all the basic setup completed, including torch
FROM macto94/ce_challenge_2024:latest


RUN apt-get update && apt-get install -y wget git vim
RUN pip3 install transformers datasets accelerate

# build custom kernels
WORKDIR /workspace
COPY script ./script
#COPY kernels ./kernels
#RUN cd kernels && python3 setup.py install

WORKDIR /workspace/script
