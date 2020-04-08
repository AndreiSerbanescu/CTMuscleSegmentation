FROM python:3.8-rc-buster


WORKDIR /app

RUN apt-get update
RUN pip3 install --upgrade pip

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

COPY ./src/ /app/src
RUN mv /app/src/* /app/ && rm -rf /app/src