#! /bin/bash
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
output_dir=${SCRIPTPATH}/../output/figures

# constrain angles
bash ${SCRIPTPATH}/pipeline.sh quality_initial &
wait

# optimize with symmetric dirichlet
bash ${SCRIPTPATH}/../scripts/symmetric_dirichlet.sh \
    ${output_dir}/quality_initial \
    ${output_dir}/quality_final
wait

# render optimized output
cp ${SCRIPTPATH}/pipelines/quality_final.json ${output_dir}/quality_final/_pipeline.json
python3 ${SCRIPTPATH}/../scripts/holonomy_pipeline.py ${output_dir}/quality_final/_pipeline.json

wait

# generate colormap histograms
python3 scripts/figures/symmetric_dirichlet_histogram.py \
    --mesh_dir ${output_dir}/quality_initial \
    --output_dir ${output_dir}/quality_initial \
    --suffix refined_with_uv

python3 scripts/figures/symmetric_dirichlet_histogram.py \
    --mesh_dir ${output_dir}/quality_final \
    --output_dir ${output_dir}/quality_final \
    --suffix optimized_uv
