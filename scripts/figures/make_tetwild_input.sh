#! /bin/bash

# Make input table and histograms
mkdir -p output/figures/tetwild_input
python3 scripts/figures/mesh_info.py \
	--mesh_dir data/tetwild_all \
	--output_dir output/figures/tetwild_input
python3 scripts/figures/tetwild_input_histogram.py \
	--input output/figures/tetwild_input/mesh_info.csv \
	--output_dir output/figures/tetwild_input

