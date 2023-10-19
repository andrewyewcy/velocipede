# VELOCIPEDE

Author: Andrew Yew<br>
Contact: [LinkedIn](https://www.linkedin.com/in/andrewyewcy/) [Website](https://andrewyewcy.com/)

## Brief Introduction
As an avid cyclist, how are bicycle rental (bikeshare) networks performing and what are possible ways to improve the bikeshare systems further. In this study, 40 million [Bixi](https://bixi.com/en/) bicycle trips across 2014 and 2022 in the city of Montreal were analyzed to build a regressor that predicts the number of trips for each station. The geographical coordinates of each bicycle rental station were converted to similarity measures to cluster centres using KMeans and RBF Kernel. These similarity measures were then used to train a Random Forest regressor that was able to predict the percentage of annual trips for each station with a RMSE of 0.05608% with a 95% confidence interval of 0.04770% and 0.06336%. Practically, the model requires further tuning for stations with annual trips less than 33% percentile of annual trips, but, is able to accurately predict the annual number of trips for all stations as a whole with less than 5% difference to actuals.

![030_regression_modelling_002.png](/22_assets/images/030_regression_modelling_002.png)

## Access to dashboard webapp
Interactive dashboard hosted on an AWS EC2 instance: [Link](http://3.96.175.190:8501/)
This dashboard visualizes the Bixi bicycle trips in the city of Montreal between 2014 and 2022.
![velocipede_dashboard_.png](/22_assets/images/velocipede_dashboard_.png)

## Open Data Sources
Format: Company (City, Country Code)<br>
1. Bixi (Montreal, CA) : [open_data](https://bixi.com/en/open-data)

## Environments and Setup
The dashboard is packaged as a Docker container and hosted on an AWS EC2 instance while all other notebooks also use Docker containers.

**Setup instructions**<br>
1. Installed GIT, Docker and Docker-compose on local machine. 
2. Clone the git repository
3. In terminal, go to directory of repository, then run:
   - `app_setup.yaml` for setup of production environment (Streamlit app)
   - `dev_setup.yaml` for setup of development environment, which includes Streamlit app, Jupyter Hub, phpMyAdmin, and MySQL server

- For the dashboard hosted on AWS
   - `02_app_requirements`: contains Dockerfile and requirements.txt to recreate the dashboard
   - `app_setup.yaml`: a Docker-compose file that pulls images based on files in `02_app_requirements`
   - `streamlit_app.py`: Python script containing dashboard
- For notebooks:
   - `01_dev_requirements`: contains Dockerfile and requirements.txt to run notebooks for data processing and machine learning
   - `dev_setup.yaml`: a Docker-compose file that pulls images based on files in `01_dev_requirements`
      - Instructions on how to access Jupyter will appear in the terminal
         - Container 1 `sql`: contains MySQL for storing the data
         - Container 2 `php`: contains phpMyAdmin for administering MySQL
         - Container 3 `dev`: contains Pyspark notebook with most machine learning packages installed 
         - Container 4 `app`: contains Streamlit app for testing in development

## Tools involved
- Docker
- Python
- MySQL
- phpMyAdmin
- Streamlit

## Repository Table of Contents
- `01_dev_requirements`
`Dockerfile` for docker-compose to build Docker container and `requirements.txt` listing python packages required to recreate the develop environment

- `02_app_requirements`
`Dockerfile` for docker-compose to build Docker container and `requirements.txt` listing python packages required to recreate the production environment

- `11_raw_data`*not available on GitHub*
This folder contains all raw data before cleaning and storage in MySQL

- `12_processed_data`
Comma Separated Value (CSV) files containing the smaller(<100MB) ETL products from the raw data. These files are used to create visualizations and analysis.

- `13_models`
Contains the trained machine learning models used throughout development and production

- `21_notebooks`
Jupyter notebooks created while developing the dashboard. Each notebook represents one process and is roughly 1 blog post in the author's [blog](andrewyewcy.com). Examples of processes are: web-scraping, data ingestion, data visualization.

- `22_assets`
Contains the output from the notebooks, such as images, PowerPoint, Excel, and other files.

- `23_logs`
Contains log files from data ingestion or ETL processes for troubleshooting.

- `24_testing`
Contains all notebooks and code in development.

- `30_automation` *in construction*
Contains Python files and Makefile for automation processes

- `streamlit_app.py`
Python app that contains the interactive dashboard.