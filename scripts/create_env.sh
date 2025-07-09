#! /bin/bash

module load gpu cuda/12.6.2 cudnn/9.5.1.17-12 anaconda3

scripts=$(dirname "$0")
base=$scripts/..

venvs=$base/venvs

# perhaps not necessary anymore
# export TMPDIR="/var/tmp"

mkdir -p $venvs

# venv for HF

conda create -y --prefix $venvs/huggingface python=3.9.6
