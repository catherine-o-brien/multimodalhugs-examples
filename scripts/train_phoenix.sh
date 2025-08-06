#! /bin/bash

# calling script needs to set:
# $base
# $dry_run

base=$1
dry_run=$2

venvs=$base/venvs
configs=$base/configs

models=$base/models

mkdir -p $models

# measure time

SECONDS=0

################################

echo "Python before activating:"
which python

echo "activate path:"
which activate

# perhaps not necessary anymore
# eval "$(conda shell.bash hook)"

echo "Executing: source activate $venvs/huggingface"

source activate $venvs/huggingface

echo "Python after activating:"
which python

# necessary?
# export CUDA_VISIBLE_DEVICES=0

################################

# setup

multimodalhugs-setup --modality "pose2text" --config_path $CONFIG_PATH

# training

config_path=$configs/config_phoenix.yaml

multimodalhugs-train \
    --task "translation" \
    --config_path $config_path \
    --output_dir $models

echo "time taken:"
echo "$SECONDS seconds"