#! /bin/bash

mesh_dir="data/closed-Myles"
field_dir="data/mpz14_data/inputmodels"
Th_hat_dir="data/closed-Myles"
output_dir="data/rotation-forms/closed-Myles"
build_dir="build"
model_list=($(ls ${mesh_dir}))

rm -rf ${output_dir}
mkdir -p ${output_dir}

for file in ${model_list[@]}
do
  if [[ "$file" = *".obj" ]]; then
    m=${file%.*}
    ${build_dir}/src/analysis/compute_rotation_form ${mesh_dir}/${m}.obj ${field_dir}/${m}.ffield ${Th_hat_dir}/${m}_Th_hat ${output_dir}/${m}_kappa_hat
  fi
done