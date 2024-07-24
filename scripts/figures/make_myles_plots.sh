#! /bin/bash

# Make input table and histograms
mkdir -p output/figures/myles_input
python3 scripts/figures/mesh_info.py \
	--mesh_dir data/closed-Myles \
	--output_dir output/figures/myles_input
python3 scripts/figures/myles_input_histogram.py \
	--input output/figures/myles_input/mesh_info.csv \
	--output_dir output/figures/myles_input

# Make result table and histograms
mkdir -p output/figures/myles_results
python3 scripts/figures/consolidate_iteration_data.py \
	--data_dir output/figures/myles_dataset \
	--output_dir output/figures/myles_results
python3 scripts/figures/myles_results_histogram.py \
	--input output/figures/myles_results/final_data.csv \
	--output_dir output/figures/myles_results
