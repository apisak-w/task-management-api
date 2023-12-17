# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app/python

RUN apt-get --assume-yes update && \
    apt-get --assume-yes upgrade && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get -y install --no-install-recommends apt-utils dialog 2>&1 && \
    apt-get --assume-yes install freetds-dev freetds-bin 

# Copy the requirements file to the container
COPY requirements.txt .

RUN pip install --upgrade pip

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# To ensure proper functionality, install the marshmallow package separately; otherwise, the flasgger_marshmallow package will enforce the use of Marshmallow v2.
RUN pip install -U marshmallow

# Copy the project files to the container
COPY . .

# Set the default command to run when the container starts
CMD [ "flask", "run" ]