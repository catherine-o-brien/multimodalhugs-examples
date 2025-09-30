# multimodalhugs-examples

Download the code:

    git clone https://github.com/bricksdont/multimodalhugs-examples

## Basic setup

Create a venv:

    ./scripts/environment/create_venv.sh

Then install required software:

    ./scripts/environment/install.sh

## Run experiments

The one change you definitely need to make is edit the 
variable `base` at the top of a run script such as `scripts/running/run_basic.sh`. Then to train a basic model:

    ./scripts/running/run_basic.sh

This will first download and prepare the PHOENIX training data,
and then train a basic MultimodalHugs model. All steps are submitted
as SLURM jobs.
