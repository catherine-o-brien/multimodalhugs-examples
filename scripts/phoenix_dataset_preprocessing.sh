#! /bin/bash

# calling script needs to set:
# $base

base=$1

scripts=$base/scripts
data=$base/data
venvs=$base/venvs

poses=$data/poses
preprocessed=$data/preprocessed

mkdir -p $data
mkdir -p $poses $preprocessed

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

################################

python $scripts/phoenix_dataset_preprocessing.py \
    --pose-dir $poses \
    --output-dir $preprocessed \
    --tfds-data-dir $data/tensorflow_datasets

# sizes
echo "Sizes of preprocessed TSV files:"

wc -l $preprocessed/*

echo "time taken:"
echo "$SECONDS seconds"
