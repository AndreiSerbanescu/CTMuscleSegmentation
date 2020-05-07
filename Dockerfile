FROM nvidia/cuda:latest

WORKDIR /app

# Installing Python3 and Pip3
RUN apt-get update
RUN apt-get update && apt-get install -y  python3-pip virtualenv libssl-dev libpq-dev git build-essential libfontconfig1 libfontconfig1-dev
RUN pip3 install setuptools pip --upgrade --force-reinstall

# Installing dependencies
RUN pip install nibabel
RUN pip3 install torch
RUN pip3 install simpleitk
RUN pip3 install numpy
RUN pip3 install pprint
RUN pip3 install argparse
RUN pip3 install pandas
RUN pip3 install torchvision
RUN pip3 install scipy

# Installing tools for debugging
RUN apt-get install vim -y

RUN mkdir /app/data_share
ENV DATA_SHARE_PATH /app/data_share

COPY files/interface /app/
COPY files/source /app