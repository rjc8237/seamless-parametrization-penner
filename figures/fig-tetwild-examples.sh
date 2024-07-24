#! /bin/bash
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
output_dir=${SCRIPTPATH}/../output/figures

bash ${SCRIPTPATH}/pipeline.sh tetwild_examples &

wait

cp -r ${output_dir}/tetwild_examples ${output_dir}/tetwild_examples_zoom
cp ${SCRIPTPATH}/pipelines/tetwild_examples_zoom.json ${output_dir}/tetwild_examples_zoom/_pipeline.json
python3 ${SCRIPTPATH}/../scripts/holonomy_pipeline.py ${output_dir}/tetwild_examples_zoom/_pipeline.json

exit

