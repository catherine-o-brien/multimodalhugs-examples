#! /bin/bash

# calling script needs to set

# $scripts
# $hyp
# $ref
# $output

for unused in pseudo_loop; do

    if [[ -s $output ]]; then
      continue
    fi

    python  evaluate_bleurt_generic.py --references $ref --predictions $hyp > $output

    echo "$output"
    cat $output

done
