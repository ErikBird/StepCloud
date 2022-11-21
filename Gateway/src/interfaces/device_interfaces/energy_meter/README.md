# Energy Meter

## Shelly Plug S

### Setup

1. Press button on device for 10 seconds to reset

2. Connect to Wifi

3. Open IP Address ` http://192.168.33.1/ `

## Usage

### Docker

You can test the project with docker. This makes the installation process easy and
the engine available not only on unix operating systems.

1. Build the image:

   `
   sudo docker build -t engine .
   `

2. Build the container and run it as daemon

   `
   sudo docker run -d --name my-engine engine
   `

3. Access the shell of the docker container

   `
   sudo docker exec -it my-engine /bin/sh