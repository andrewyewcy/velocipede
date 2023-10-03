##########<br>
VELOCIPEDE<br>
##########<br>

Author: Andrew Yew<br>
Date initiated: 2023-06-01<br>

# Description <br> 
As an avid cyclist, how are bikeshare networks performing across cities and what are possible ways to improve the bikeshare systems further. The first city for analysis is Montreal, where Bixi is the main bikeshare provider.This repository contains development notebooks detailing the process of developing dashboards and machine learning model using open source data on Bicycle rides.<br>

# Interactive Dashboard<br>
An interactive dashboard is hosted on an AWS EC2 instance, accessible [here](http://3.96.175.190:8501/)

# Open Data Sources<br>
Format: Company (City, Country Code)<br>
1. Bixi (Montreal, CA) : [open_data](https://bixi.com/en/open-data)

# SETUP <br>
## Requirements<br>
1. GIT
2. [Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/)

## Procedure<br>
1. Clone the git repository
2. In terminal, go to directory of repository, then run:
   - `app_setup.yaml` for setup of production environment (Streamlit app)
   - `dev_setup.yaml` for setup of development environment, which includes Streamlit app, Jupyter Hub, phpMyAdmin, and MySQL server

## Details<br>
Details for all environments can be found within the `app_setp.yaml` and `dev_setup.yaml` files, with exact requirements listed in `01_dev_requirements` and `02_app_requirements` folders.

# Table of Contents:<br>
### 01_dev_requirements
`Dockerfile` for docker-compose to build Docker container and `requirements.txt` listing python packages required to recreate the develop environment

### 02_app_requirements
`Dockerfile` for docker-compose to build Docker container and `requirements.txt` listing python packages required to recreate the production environment

### 12_processed_data
Comma Separated Value (CSV) files containing the smaller(<100MB) ETL products from the raw data. These files are used to create visualizations and analysis.

### 21_notebooks
Jupyter notebooks created while developing the dashboard. Each notebook represents one process and is roughly 1 blog post in the author's [blog](andrewyewcy.com). Examples of processes are: web-scraping, data ingestion, data visualization.

### 22_assets
Contains the output from the notebooks, such as images, PowerPoint, Excel, and other files.

### 23_logs
Contains log files from data ingestion or ETL processes for troubleshooting.

### 24_testing
Jupyter notebooks that were used in development and pending organization into 21_notebooks or deletion

### streamlit_app.py
Streamlit app that contains the interactive dashboard.