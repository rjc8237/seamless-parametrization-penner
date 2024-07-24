#! /bin/bash
SCRIPT=$(realpath "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
BINDIR=${SCRIPTPATH}/../build/bin/
data_dir=${SCRIPTPATH}/../data/closed-Myles
m=cup
output_dir=${SCRIPTPATH}/../output/figures/stress_test

mkdir -p ${output_dir}
${BINDIR}/animate_holonomy_rotation \
	--mesh ${data_dir}/${m}.obj \
	--cones ${data_dir}/${m}_Th_hat \
	--field ${data_dir}/${m}_kappa_hat \
	--loop 0 \
	--frames 5 \
	--output ${output_dir}

# Rename output files
file_list=($(ls ${output_dir}))
mkdir -p ${output_dir}/${m}_output
for file in ${file_list[@]}
do
  if [[ "$file" = "frame_"* ]]; then
    suffix="${file##frame_}"
		mv ${output_dir}/frame_${suffix} ${output_dir}/${m}_output/${m}_${suffix}
	fi
done

# Render output
cp ${SCRIPTPATH}/pipelines/stress_test.json ${output_dir}/_pipeline.json
python3 ${SCRIPTPATH}/../scripts/holonomy_pipeline.py ${output_dir}/_pipeline.json
