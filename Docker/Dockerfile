############################################################
# Dockerfile to build Python / Django / Mysql small container images
# Based on Linux Alpine
############################################################

# Set the base image
FROM yobasystems/alpine-mariadb

# Work dir
WORKDIR /usr/src/app
COPY . .

# File Author / Maintainer
LABEL Janis Romsko

# Update the repository sources list
RUN apk update

################## BEGIN INSTALLATION ######################
# Add the packages
RUN apk add python3
RUN apk add --update py-pip
RUN pip install mariadb
# You can skip this step if your Django project has the correct version specified on requirements.txt
RUN pip install fastapi pydantic uvicorn


# Clean up disk space
RUN rm -Rf ~/.cache
##################### INSTALLATION END #####################

# Expose the default port
EXPOSE 8000

# Set default container command
CMD ["python", "./app.py"]

### Reduce the image size
##  Run : docker export <CONTAINER ID> | docker import - some-image-name:latest