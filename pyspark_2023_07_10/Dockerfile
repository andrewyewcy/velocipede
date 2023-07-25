# This Dockerfile creates an image based on pyspark-notebook to include mysqlclient, plotly, and natural language toolkit
# To create image, input the following in a terminal pointing to this directory:
# docker build -t dev:01 .
FROM jupyter/pyspark-notebook:2023-06-26

# Run below line to clone the requirements file from github
# RUN git clone https://github.com/streamlit/streamlit-example.git .

#RUN sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

COPY requirements.txt ./requirements.txt
COPY .aws ./.aws/

COPY mysql-connector-j-8.0.33.jar ./mysql-connector-j-8.0.33.jar

RUN conda install -c conda-forge mysqlclient
RUN pip3 install -r requirements.txt