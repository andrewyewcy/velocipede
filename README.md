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
## 01_dev_requirements


## notebook_functions
Contains custom functions that are commonly used across different notebooks.

## terminal_functions
Contains functions that are called through Terminal (shell), usually for touching up notebooks.

## notebooks 01X
Notebooks that detail data ingestiong and preprocessing.

## notebooks 02X
Notebooks that detail data exploration and visualization.

## TESTX
Test notebooks for specific functions, to be removed at project completion.