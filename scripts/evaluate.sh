#! /bin/bash

# calling process needs to set:
# base

base=$1

scripts=$base/scripts
venvs=$base/venvs

translations=$base/translations
translations_sub=$translations/phoenix

evaluations=$base/evaluations
evaluations_sub=$evaluations/phoenix

mkdir -p $evaluations $evaluations_sub

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

hyp=$translations_sub/generated_predictions.txt
ref=$translations_sub/predictions_labels.txt

output=$evaluations_sub/test_score.bleu

. $scripts/evaluate_bleu_generic.sh

exit 0

# todo remove once implemented

output=$evaluations_sub/test_score.bleurt

. $scripts/evaluate_bleurt_generic.sh

