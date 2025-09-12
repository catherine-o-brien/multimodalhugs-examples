# multimodalhugs-examples

Download the code:

    git clone https://github.com/bricksdont/multimodalhugs-examples

## Basic setup

Create a venv:

    ./scripts/create_env.sh

Then install required software:

    ./scripts/install.sh

## Run experiments

The one change you definitely need to make is edit the 
variable `base` at the top of `scripts/run.sh.` Then:

    ./scripts/run.sh

This will first download and prepare the training data,
and then train a MultimodalHugs model. All steps are submitted
as SLURM jobs.
