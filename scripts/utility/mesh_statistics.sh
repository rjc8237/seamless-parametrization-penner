#! /bin/bash

data_dir=$1
file_list=($(ls ${data_dir}))
build_dir=./build

for file in ${file_list[@]}
do
  if [[ "$file" = *".obj" ]]; then
    m=${file%.obj}
    ${build_dir}/src/app/mesh_statistics \
      --mesh ${data_dir}/${m}.obj \
      --cones ${data_dir}/${m}_Th_hat \
      --field ${data_dir}/${m}_kappa_hat
  fi
done
