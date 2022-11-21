# set base image (host OS)
FROM cdrx/pyinstaller-windows:python3

# Set some working directory where you want to run your code inside docker
WORKDIR /opt/app/

# copy all files to the working directory
COPY . /opt/app/

# install dependencies
RUN pip install -r requirements.txt
RUN apt-get -y install gettext-base
# command to run on container start
#CMD [ "python", "./main.py", "engine", "start"]
#"--help"]
#"debug-engine", "start" ]
#ENTRYPOINT []
