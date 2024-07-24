import os, sys
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, '..', 'py')
sys.path.append(module_dir)
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


if __name__ == "__main__":

  output_dir = "output/figures/intrinsic"
  os.makedirs(output_dir, exist_ok=True)

  models = os.listdir('data/thingi10k-connected')
  models = [f[:-len('.obj')] for f in models if f.endswith('.obj')]
  print(len(models), "models")

  # file labels and corresponding angles for tests
  first_input_dir = "output/plot_regularization_v2/final_data"
  #second_input_dir = "output/figures/plots/final_data"
  second_input_dir = "output/figures/plots_diff/final_data"
  file_nums = ["0", "0_003", "0_03", "0_3", "3", "30", "60"]
  label_nums = ["0", "0.003", "0.03", "0.3", "3", "30", "60"]


  # lambda to add a data entry
  def combine_data(first_df, second_df, models):
    first_df = first_df.loc[first_df["Unnamed: 0"].isin(models)]
    first_df.set_index('Unnamed: 0', inplace=True)
    print('first', first_df)

    int_models = [int(m) for m in models]
    second_df = second_df.loc[second_df["Unnamed: 0"].isin(int_models)]
    second_df.set_index('Unnamed: 0', inplace=True)
    print('second', second_df)

    combined_df = pd.concat((first_df, second_df), axis=0).reset_index()
    combined_df.drop_duplicates(subset=['Unnamed: 0',])

    return combined_df

  # gather data from file
  for i, n in enumerate(file_nums):
    # Add regularization data
    first_df = pd.read_csv(os.path.join(first_input_dir, 'regularization_' + n + ".csv"))
    second_df = pd.read_csv(os.path.join(second_input_dir, 'regularization_' + n + ".csv"))
    combined_df = combine_data(first_df, second_df, models)
    combined_df.to_csv(os.path.join(output_dir, 'regularization_' + n + '.csv'))

  exit()

  for i, n in enumerate(file_nums):
    # Add refinement data
    first_df = pd.read_csv(os.path.join(first_input_dir, 'refinement_' + n + ".csv"))
    second_df = pd.read_csv(os.path.join(second_input_dir, 'refinement_' + n + ".csv"))
    combined_df = combine_data(first_df, second_df, models)
    combined_df.to_csv(os.path.join(output_dir, 'refinement_' + n + '.csv'))

