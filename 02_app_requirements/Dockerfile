# This Dockerfile creates an image based on pyspark-notebook to include mysqlclient, plotly, and natural language toolkit
# To create image, input the following in a terminal pointing to this directory:
# docker build -t dev:01 .
FROM python:3.11.4-slim

WORKDIR /app

# COPY requirements txt to /app 
COPY /requirements.txt .

# Tell package manager to install items in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Tells Docker that the container listens on the specified network ports at runtime.
EXPOSE 8501

# Tells Docker to test a container and check that is it still working
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Configures container to run as an executable
ENTRYPOINT ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]