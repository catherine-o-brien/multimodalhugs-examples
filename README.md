# multimodalhugs-examples

Download the code:

    git clone https://github.com/bricksdont/multimodalhugs-examples
    cd multimodalhugs-examples

## Basic setup

Create a venv:

    ./scripts/environment/create_env.sh

Then install required software:

    ./scripts/environment/install.sh

## Run experiments

### Single experiment

The one change you definitely need to make is edit the 
variable `base` at the top of a run script such as `scripts/running/run_basic.sh`.

It is also a good idea
to use `dry_run="true"` the first time you are running code, which creates all files, executes all
the code but uses only a fraction of the training data, trains for very few steps only, etc - as a
general sanity check. If you want to launch a real run after a dry run you will need to manually
delete folders that the dry run created (e.g. a sub-folder of `models`), otherwise the steps
will not be repeated.

Then to train a basic model:

    ./scripts/running/run_basic.sh

This will first download and prepare the PHOENIX training data,
and then train a basic MultimodalHugs model. All steps are submitted
as SLURM jobs.

If the process is fully reproducible, this should result in a test set BLEU score of `10.691`. This
value is inside the file `evaluations/phoenix/test_score.bleu`.

### Hyperparams exploration

The following script will train approximately 50 models to search for good hyperparameters
(each run will finish in roughly 2 hours):

    ./scripts/running/run_hyperparam_search.sh

Currently the models with label smooothing enabled will fail.
