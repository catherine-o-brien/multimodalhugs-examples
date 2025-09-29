#! /bin/bash

# calling script needs to set

# $scripts
# $hyp
# $ref
# $output
# $bleurt_checkpoint

for unused in pseudo_loop; do

    if [[ -s $output ]]; then
      continue
    fi

    # avoid TF JIT compiler error

    export XLA_FLAGS=--xla_gpu_cuda_data_dir=$(dirname $(dirname $(which nvcc)))

    python $scripts/evaluate_bleurt.py \
        --references $ref \
        --predictions $hyp \
        --checkpoint $bleurt_checkpoint \
        > $output

    echo "$output"
    cat $output

done
