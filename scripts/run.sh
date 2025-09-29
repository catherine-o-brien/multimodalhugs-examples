#! /bin/bash

base="/shares/sigma.ebling.cl.uzh/mathmu/multimodalhugs-examples"

dry_run="false"

################################

module load anaconda3

# explicit unloading of GPU modules at this point to use CPU nodes

module unload gpu cuda/12.6.2 cudnn/9.5.1.17-12

scripts=$base/scripts
logs=$base/logs

# logging

mkdir -p $logs

SLURM_DEFAULT_FILE_PATTERN="slurm-%j.out"
SLURM_LOG_ARGS="-o $logs/$SLURM_DEFAULT_FILE_PATTERN -e $logs/$SLURM_DEFAULT_FILE_PATTERN"

echo "##############################################" | tee -a $logs/MAIN
date | tee -a $logs/MAIN
echo "##############################################" | tee -a $logs/MAIN
echo "DRY RUN: $dry_run" | tee -a $logs/MAIN

# SLURM job args

DRY_RUN_SLURM_ARGS="--cpus-per-task=2 --time=01:00:00 --mem=8G"

SLURM_ARGS_GENERIC="--cpus-per-task=8 --time=24:00:00 --mem=16G"
SLURM_ARGS_TRAIN="--time=36:00:00 --gres=gpu:V100:1 --constraint=GPUMEM32GB --cpus-per-task 8 --mem 16g"
SLURM_ARGS_TRANSLATE="--time=12:00:00 --gres=gpu:V100:1 --constraint=GPUMEM32GB --cpus-per-task 8 --mem 16g"
SLURM_ARGS_EVALUATE="--time=01:00:00 --gres=gpu:V100:1 --constraint=GPUMEM32GB --cpus-per-task 8 --mem 16g"

# if dry run, then all args use generic instances

if [[ $dry_run == "true" ]]; then
  SLURM_ARGS_GENERIC=$DRY_RUN_SLURM_ARGS
  SLURM_ARGS_TRAIN=$DRY_RUN_SLURM_ARGS
  SLURM_ARGS_TRANSLATE=$DRY_RUN_SLURM_ARGS
  SLURM_ARGS_EVALUATE=$DRY_RUN_SLURM_ARGS
fi

# preprocess data

id_preprocess=$(
    $scripts/sbatch_bare.sh \
    $SLURM_ARGS_GENERIC \
    $SLURM_LOG_ARGS \
    $scripts/phoenix_dataset_preprocessing.sh \
    $base $dry_run
)

echo "  id_preprocess: $id_preprocess | $logs/slurm-$id_preprocess.out" | tee -a $logs/MAIN

# load GPU modules at this point

module load gpu cuda/12.6.2 cudnn/9.5.1.17-12

# HF train (depends on preprocess)

id_train=$(
    $scripts/sbatch_bare.sh \
    $SLURM_ARGS_TRAIN \
    --dependency=afterok:$id_preprocess \
    $SLURM_LOG_ARGS \
    $scripts/train_phoenix.sh \
    $base $dry_run
)

echo "  id_train: $id_train | $logs/slurm-$id_train.out"  | tee -a $logs/MAIN

# HF translate + evaluate (depends on train)

id_translate=$(
    $scripts/sbatch_bare.sh \
    $SLURM_ARGS_TRANSLATE \
    --dependency=afterok:$id_train \
    $SLURM_LOG_ARGS \
    $scripts/translate_phoenix.sh \
    $base $dry_run
)

echo "  id_translate: $id_translate | $logs/slurm-$id_translate.out"  | tee -a $logs/MAIN

# evaluate (depends on translate)

id_evaluate=$(
    $scripts/sbatch_bare.sh \
    $SLURM_ARGS_EVALUATE \
    --dependency=afterok:$id_translate \
    $SLURM_LOG_ARGS \
    $scripts/evaluate.sh \
    $base $dry_run
)

echo "  id_evaluate: $id_evaluate | $logs/slurm-$id_evaluate.out"  | tee -a $logs/MAIN
