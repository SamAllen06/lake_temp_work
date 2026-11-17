#!/bin/bash
#SBATCH -J lake_temp_test #set the jobname in slurm
#SBATCH -o %x.o%j #set the file name that stdout and stderror are captured in %x jobname, %j jobnumber
#SBATCH -t 00:00:20 #set the time for the job to run in HH:MM:SS
#SBATCH --container-image=./lake_temp.sqsh #where to find container image
#SBATCH --container-writable #set container writable
#SBATCH --container-mounts=./lake_temp_logs:/app/logs,./lake_temp_output:/app/testing_output #mount external filesystems
cd model; for item in [1 2 3 4 5 6 7]; do time ./elmtest 1; done #run commands in the container (different from most sbatch instances that run on the host machine)
#whatever you change in the container will also change in the repository