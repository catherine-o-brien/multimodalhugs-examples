#! /bin/bash

# taken from:
# https://hpc.nih.gov/docs/job_dependencies.html

sbr="$(/cluster/24-05-1-1/slurm-24-05-1-1/bin/sbatch "$@")"

if [[ "$sbr" =~ Submitted\ batch\ job\ ([0-9]+) ]]; then
    echo "${BASH_REMATCH[1]}"
    exit 0
else
    echo "sbatch failed"
    exit 1
fi
