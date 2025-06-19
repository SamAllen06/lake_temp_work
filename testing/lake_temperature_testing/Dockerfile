FROM nvcr.io/nvidia/nvhpc:23.5-devel-cuda_multi-ubuntu22.04

RUN apt-get update -y && \
    apt-get install -y \
    python3 \
    python3-pip \
    vim && \
    apt-get clean all

RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN apt-get install -y locales && \
    echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen && \
    locale-gen

ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US.UTF-8

RUN locale -a

WORKDIR /app

COPY docker/ /app/
COPY src/ /app/src/

#RUN pip3 install wheel numpy scipy netCDF4 h5py configparser cftime
#RUN CFLAGS=-noswitcherror pip install mpi4py
