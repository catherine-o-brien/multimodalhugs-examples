# multimodalhugs-examples

## Basic setup

Create a venv:

    ./scripts/create_venv.sh

Then install required software:

    ./scripts/install.sh

## Run experiments

    ./scripts/run.sh

This will first download and prepare the training data,
and then train a MultimodalHugs model. All steps are submitted
as SLURM jobs.
