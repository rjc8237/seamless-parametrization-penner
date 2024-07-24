#! /bin/bash

input_dir=$1
file_list=($(ls ${input_dir}))
output_dir=$2
output_file=${output_dir}/mesh_list.txt
[ -e ${output_file} ] && rm ${output_file}

for file in ${file_list[@]}
do
  if [[ "$file" = *".obj" ]]; then
    echo \"${file}\", >> ${output_file}
  fi
done
