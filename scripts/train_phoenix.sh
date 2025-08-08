#! /bin/bash

# calling script needs to set:
# $base
# $dry_run

base=$1
dry_run=$2

data=$base/data
preprocessed=$data/preprocessed
scripts=$base/scripts
venvs=$base/venvs
configs=$base/configs
configs_sub=$configs/phoenix

models=$base/models
models_sub=$models/phoenix

mkdir -p $configs
mkdir -p $configs_sub
mkdir -p $models
mkdir -p $models_sub

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

# setup

if [[ $dry_run == "true" ]]; then
    dry_run_arg="--dry-run"
else
    dry_run_arg=""
fi

python $scripts/create_config.py \
    --run-name "phoenix" \
    --config-dir $configs_sub \
    --output-dir $models_sub \
    --logging-dir $models_sub \
    --train-metadata-file $preprocessed/rwth_phoenix2014_t.train.tsv \
    --validation-metadata-file $preprocessed/rwth_phoenix2014_t.validation.tsv \
    --test-metadata-file $preprocessed/rwth_phoenix2014_t.test.tsv \
    --new-vocabulary "__dgs__" \
    --reduce-holistic-poses $dry_run_arg

multimodalhugs-setup \
    --modality "pose2text" \
    --config_path $configs_sub/config_phoenix.yaml \
    --output_dir $models_sub

exit 0

# training

multimodalhugs-train \
    --task "translation" \
    --config_path $configs_sub/config_phoenix.yaml \
    --output_dir $models_sub

echo "time taken:"
echo "$SECONDS seconds"