#! /bin/bash

#params_dir="data/mpz14_data/miq_bommes"
#output_dir="data/miq_bommes"

params_dir="data/mpz14_data/miq_yaron"
output_dir="data/miq_yaron"

model_list=($(ls ${params_dir}))

for file in ${model_list[@]}
do
  if [[ "$file" = *".obj" ]]; then
    m=${file%_miq_nonlin.obj}
    mkdir -p ${output_dir}/${m}_output
    cp ${params_dir}/${file} ${output_dir}/${m}_output/${file}
  fi
done