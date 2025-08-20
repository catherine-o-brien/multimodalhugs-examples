#! /bin/bash

# calling script needs to set:
# $base
# $dry_run

base=$1
dry_run=$2

data=$base/data
scripts=$base/scripts
venvs=$base/venvs
configs=$base/configs
configs_sub=$configs/phoenix

models=$base/models
models_sub=$models/phoenix

translations=$base/translations
translations_sub=$translations/phoenix

mkdir -p $translations
mkdir -p $translations_sub

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

# if in doubt, check with:
# echo "CUDA is available:"
# python -c 'import torch; print(torch.cuda.is_available())'

################################

# for now need to manually find latest checkpoint
# taken from: https://github.com/GerrySant/multimodalhugs/blob/master/tests/e2e_overfitting/e2e_overfitting.sh#L26C1-L28C50

model_name_or_path=$(find $models_sub/phoenix -maxdepth 1 -type d -name 'checkpoint-*' | \
  sed 's/.*checkpoint-//' | sort -n | tail -1 | \
  xargs -I{} echo "${models_sub/phoenix}/checkpoint-{}")

multimodalhugs-generate --task "translation" \
    --config_path $configs_sub/config_phoenix.yaml \
    --metric_name "sacrebleu" \
    --output_dir $translations_sub \
    --data_dir $models_sub/phoenix/datasets/pose2text \
    --model_name_or_path $model_name_or_path \
    --processor_name_or_path $models_sub/phoenix/pose2text_processor
