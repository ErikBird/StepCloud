FROM python:3.10

# Set some working directory where you want to run your code inside docker
WORKDIR /opt/app/

# copy all files to the working directory
COPY . /opt/app/

ENV PYTHONPATH=/opt/app/
# install dependencies
RUN pip install -r requirements.txt
