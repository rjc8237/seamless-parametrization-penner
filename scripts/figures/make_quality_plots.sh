#! /bin/bash

output_dir=output/figures/sym_dir_quality
mkdir -p ${output_dir}
python3 scripts/figures/symmetric_dirichlet_histogram.py \
	--mesh_dir output_sonic/metric_newton_sym_dir \
	--output_dir ${output_dir}

output_dir=output/figures/newton_quality
mkdir -p ${output_dir}
python3 scripts/figures/symmetric_dirichlet_histogram.py \
	--mesh_dir output_sonic/newton_timings \
	--output_dir ${output_dir}
