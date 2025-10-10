#! /bin/bash

base="/shares/sigma.ebling.cl.uzh/mathmu/multimodalhugs-examples"
scripts=$base/scripts

# set to "false" or "true":

dry_run="false"

for learning_rate in "5e-6" "1e-5" "2e-5"; do

    for warmup_steps in 0 500 1000; do

        for label_smoothing_factor in "0.0" "0.1"; do

            for gradient_accumulation_steps in 1 2 3; do

                model_name="phoenix+learning_rate.$learning_rate+warmup_steps.$warmup_steps+label_smoothing_factor.$label_smoothing_factor+gradient_accumulation_steps.$gradient_accumulation_steps"

                . $scripts/running/run_generic.sh

            done
        done
    done
done
