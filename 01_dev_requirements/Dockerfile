# Dockerhub link to image: https://hub.docker.com/layers/jupyter/minimal-notebook/2023-06-26/images/sha256-bbe7bbfed402b19ded0778a2e334d1638910320e40f169d59ccb8cfeb07e5bcf?context=explore
FROM jupyter/pyspark-notebook:2023-06-26
COPY /requirements.txt .

USER root
RUN chmod 755 requirements.txt

USER jovyan
RUN pip install --upgrade pip \
&& pip install --no-cache-dir -r requirements.txt \
&& rm requirements.txt