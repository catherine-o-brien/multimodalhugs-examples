#! /bin/bash

base="/shares/sigma.ebling.cl.uzh/mathmu/multimodalhugs-examples"

venvs=$base/venvs
scripts=$base/scripts
evaluations=$base/evaluations

summaries=$base/summaries

mkdir -p $summaries

# python3 $scripts/summaries/summarize.py --eval-folder $evaluations > $summaries/summary.tsv

grep "\"score\"" $evaluations/*/test_score.bleu | awk -F'"score": ' '{print $2 "\t" $0}' | sort -k1,1nr | cut -f2- \
    > $summaries/summary.txt

cat $summaries/summary.txt
