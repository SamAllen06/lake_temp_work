# Working with Docker

## What is a container?
A container is an isolated environment, similar (though not the same as) a
virtual machine. Both isolate the application from the host system (your 
computer) by virtualizing the filesystem, network, process IDs, and user IDs,
however, a virtual machine also virtualizes the operating system, whereas docker
does not. For example, docker images for windows require that Windows be
installed, and images for linux use the host's linux kernel (or Windows
Subsystem for Linux when run on Windows).

## What is an image?
An image is essentially a blueprint for a container. It contains everything the
container needs to run, including any dependancies or other files. This image
can then be shared with others, usually through Docker Hub.

## What is a Dockerfile
A Dockerfile specifies how to build an image. It is the highest level of
abstraction in the docker workflow. You can think of a Dockerfile similar to the
source code of a program, an image as similar to a compiled binary from that
source code, and a container as similar to that program while it is running.

## How do we write a Dockerfile?
Docker has a [reference for this on their website](https://docs.docker.com/reference/dockerfile/).

Let's take a look at how this is applied in the Dockerfile for this project.

```
FROM nvcr.io/nvidia/nvhpc:23.5-devel-cuda_multi-ubuntu22.04
```

"FROM" indicates that we want this image to extend another image. In other
words, we want this image to have the contents of the
nvhpc:23.5-devel-cuda_multi-ubuntu22.04 image, plus some additional things we
specify in the Dockerfile.

```
RUN apt-get update -y && \
    apt-get install -y \
    python3 \
    vim && \
    apt-get clean all
```

"RUN" tells docker that we want to run a command inside the image. apt is the
package manager used by Ubuntu, and this command is telling it to install
python3 (Python 3.X), and vim, a text editor.

(There are a number of RUN lines after this, but I'm not going to cover them
here as the point is to explain the syntax of the Dockerfile.)

```
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8
```

"ENV" sets an environment variable. You can access and modify environment
variables in linux using `echo $VAR` and `export VAR=value`. In this case, we
are setting the locale we want Ubuntu to use (UTF-8).

```
WORKDIR /app
```

"WORKDIR" sets the working directory. In this case, we've set it to /app/. This
means that any commands we run with the docker file will run from this location.
Additionally, when we run the docker image interactively, we will start in the
/app/ directory.

```
COPY ./elmtest/ /app/elmtest/
COPY ./scripts/ /app/scripts/
COPY ./config/elmtest_mapper.conf /app/config/mapper.conf
COPY ./elmtest_mapping_orders/ /app/mapping_orders/
```

"COPY" copies directories from the host into the image. In this case, I'm
copying the scripts/, elmtest/, and elmtest_mapping_orders/ directories, along
with the mapping script's elmtest-specific configuration file into the image.
Note that the second two lines are renaming the files they copy as well.

## Docker commands
```
docker buildx build .
```
Builds an image from the Dockerfile located in the current directory. I would 
recommend using the -t "name_here" flag to tag your image so you can recognize
it.

```
docker images
```
Lists the images currently on your machine, as well as their ID. You must use an
image's name (under "Repository") or ID to interact with it.

```
docker ps
```
Lists the currently running containers on your machine, along with their IDs.

```
docker run -it [image_name or image_id]
```
Runs a container interactively, meaning you can type commands inside it, and
recieve output from it directly on your terminal. This is how you should run
the image from the Dockerfile in this repository.

```
docker rm [container_id]
```
Removes a container. If you need to remove a stopped container, such as an
interactive one that you have run `exit` inside, you can list all containers,
regardless of running status, using `docker container ls`.

```
docker rmi [image_name or image_id]
```
Removes an image.

Please note that container_ids and image_ids are **not** the same.
