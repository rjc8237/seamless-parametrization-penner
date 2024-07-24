#! /bin/bash

# Make result table and histograms
mkdir -p output/figures/tetwild_results
python3 scripts/figures/consolidate_iteration_data.py \
	--data_dir output/figures/tetwild_dataset \
	--output_dir output/figures/tetwild_results
python3 scripts/figures/tetwild_results_histogram.py \
	--input output/figures/tetwild_results/final_data.csv \
	--output_dir output/figures/tetwild_results
