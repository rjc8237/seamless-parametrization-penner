#! /bin/bash
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
PIPELINE_DIR=${SCRIPTPATH}/../ext/penner-optimization/scripts
pipeline=$1

output_dir=${SCRIPTPATH}/../output/figures/${pipeline}
mkdir -p ${output_dir}
cp ${SCRIPTPATH}/pipelines/${pipeline}.json ${output_dir}/_pipeline.json
python ${PIPELINE_DIR}/holonomy_pipeline.py ${output_dir}/_pipeline.json
