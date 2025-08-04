#! /bin/bash

module load gpu cuda/12.6.2 cudnn/9.5.1.17-12 anaconda3

scripts=$(dirname "$0")
base=$scripts/..

venvs=$base/venvs
tools=$base/tools

# perhaps not necessary anymore
# export TMPDIR="/var/tmp"

mkdir -p $tools

source activate $venvs/huggingface

# install multimodalhugs

git clone https://github.com/GerrySant/multimodalhugs.git $tools/multimodalhugs

(cd $tools/multimodalhugs && pip install .)

# install SL datasets

pip install git+https://github.com/sign-language-processing/datasets.git
