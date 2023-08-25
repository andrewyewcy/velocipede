# This Dockerfile creates an image based on pyspark-notebook to include mysqlclient, plotly, and natural language toolkit
# To create image, input the following in a terminal pointing to this directory:
# docker build -t dev:01 .
FROM jupyter/pyspark-notebook:2023-06-26

COPY /. .

#RUN sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
RUN conda install -c conda-forge mysqlclient
RUN pip3 install -r requirements.txt