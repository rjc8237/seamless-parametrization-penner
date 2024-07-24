#! /bin/bash

data_dir="data/closed-Myles"
output_dir="../figures/compare_basis_loops/data"
build_dir="build"
model_list=($(ls ${data_dir}))

rm -rf ${output_dir}
mkdir -p ${output_dir}
mkdir -p ${output_dir}/minimal
mkdir -p ${output_dir}/maximal

for file in ${model_list[@]}
do
  if [[ "$file" = *".obj" ]]
  then
    m=${file%.*}

    if [[ "$m" = "camel" ]]
    then
      continue
    fi

    if [[ "$m" = "seahorse2_100K" ]]
    then
      continue
    fi

    if [[ "$m" = "gearbox" ]]
    then
      continue
    fi

    if [[ "$m" = "casting_refined" ]]
    then
      continue
    fi

    ${build_dir}/src/analysis/compare_basis_loops \
      --mesh ${data_dir}/${m}.obj \
      --cones ${data_dir}/${m}_Th_hat \
      --field ${data_dir}/${m}_kappa_hat \
      --output ${output_dir} \
      --mesh_name ${m}
  fi
done