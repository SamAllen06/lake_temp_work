# Cluster 
## Purpose
A directory for running test_laketemperature.py using Ball State's cluster. 

## Details
To use this, you must have an account with Ball State's cluster. 
Once you have one, use ssh your-email@ccncluster.bsu.edu with your password to log in. 
To run test_laketemperature.py, include all of your desired instructions in the 
lake_temp.sbatch file and then run `sbatch lake_temp.sbatch`. Use mounts to get files in 
and out of the container but keep in mind that, unlike the Docker container, whatever
files you change in a mounted directory will also be changed in your repository. This is
why there is a dedicated [log directory](./lake_temp_logs) and [output directory](./lake_temp_output).

## Instructions for generating the .sqsh file
In the same directory as your Dockerfile run:
``` bash
#Build the image
$> podman buildx build . -t lake_temp
#Use enroot to create the squashfs file
$> enroot import -o lake_temp.sqsh podman://localhost/lake_temp:latest
#Clean up the containers/images from the podman cache
$> podman ps -a
$> podman container rm <container id>
$> podman image ls
$> podman image rm <image id>
```
