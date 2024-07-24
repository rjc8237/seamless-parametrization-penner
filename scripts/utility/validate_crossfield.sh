#! /bin/bash

mesh_dir="data/mpz14_data/inputmodels"
Th_hat_dir="data/closed-Myles"
rotation_form_dir="data/rotation-forms/closed-Myles"

params_dir="data/mpz14_data"
output_dir="output/valdiate_crossfield"

build_dir="build"
model_list=($(ls ${mesh_dir}))

for file in ${model_list[@]}
do
  if [[ "$file" = *".obj" ]]; then
    m=${file%.obj}
    mkdir -p ${output_dir}/${m}
    ${build_dir}/src/analysis/compute_holonomy_from_uv \
      ${m} \
      ${mesh_dir}/${m}.obj \
      ${Th_hat_dir}/${m}_Th_hat \
      ${rotation_form_dir}/${m}_kappa_hat \
      ${params_dir} \
      ${output_dir}
  fi
done