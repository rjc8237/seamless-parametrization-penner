#! /bin/bash
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
output_dir=${SCRIPTPATH}/../output/figures

bash ${SCRIPTPATH}/pipeline.sh teaser &

wait

test_name=teaser_no_cones
cp -r ${output_dir}/teaser ${output_dir}/${test_name}
cp ${SCRIPTPATH}/pipelines/${test_name}.json ${output_dir}/${test_name}/_pipeline.json
python3 ${SCRIPTPATH}/../scripts/holonomy_pipeline.py ${output_dir}/${test_name}/_pipeline.json

wait

test_name=teaser_zoom
cp -r ${output_dir}/teaser ${output_dir}/${test_name}
cp ${SCRIPTPATH}/pipelines/${test_name}.json ${output_dir}/${test_name}/_pipeline.json
python3 ${SCRIPTPATH}/../scripts/holonomy_pipeline.py ${output_dir}/${test_name}/_pipeline.json

exit







