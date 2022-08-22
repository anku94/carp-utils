#!/bin/bash

function execute_parallel() {
  part_dir=$1
  base_dir=$(dirname $(readlink -e $0))
  script="python $base_dir/gen_compressed_traces.py"
  echo $script
  host=0
  for ts in $(ls $part_dir); do
    echo $host, $ts
    rm h$host
    ssh h$host "$script $part_dir/$ts" &> h$host &
    host=$(( host + 1 ))
  done
}

execute_parallel $1
