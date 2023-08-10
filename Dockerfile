# This Dockerfile creates an image based on pyspark-notebook to include mysqlclient, plotly, and natural language toolkit
# To create image, input the following in a terminal pointing to this directory:
# docker build -t dev:01 .
FROM python:3.11.4-slim

WORKDIR /usr/src/app

WORKDIR /app

# Install git for cloning the repo
# RUN apt-get update && apt-get install -y \
#     build-essential \
#     curl \
#     software-properties-common \
#     git \
#     && rm -rf /var/lib/apt/lists/*
# RUN git clone https://github.com/streamlit/streamlit-example.git .

# COPY all from location of this Dockerfile into /app 
COPY /requirements.txt .

# Tell package manager to install items in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Tells Docker that the container listens on the specified network ports at runtime.
EXPOSE 8501

# Tells Docker to test a container and check that is it still working
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Configures container to run as an executable
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]