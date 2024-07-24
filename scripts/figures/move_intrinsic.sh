#! /bin/bash

cp output/figures/plots/final_data/*.csv output/figures/intrinsic/
cp output/figures/plot_refinement/final_data/*.csv output/figures/intrinsic/
cp output/figures/intrinsic/regularization_0.csv output/figures/intrinsic/refinement_0.csv

exit

cp output/figures/plot_closed_regularization/final_data/*.csv output/figures/intrinsic/
cp output/figures/plot_closed_refinement/final_data/*.csv output/figures/intrinsic/
cp output/figures/intrinsic/regularization_0.csv output/figures/intrinsic/refinement_0.csv
