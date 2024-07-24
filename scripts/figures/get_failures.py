import os, sys
import numpy as np
import pandas as pd
import argparse


if __name__ == "__main__":
  parser = argparse.ArgumentParser("Consolidate data from iteration data logs")
  parser.add_argument("--input_dir",           help="directory with data",
                                                    type=str)
  parser.add_argument("--output_dir",           help="directory to write data",
                                                    type=str, default="")
  args = parser.parse_args()
  output_dir = args.output_dir
  if output_dir == "":
      output_dir = args.input_dir
  os.makedirs(output_dir, exist_ok=True)

  def get_failures(final_data_df):
      above_thres = (final_data_df['max_error'] > 1e-12)
      invalid_output = (final_data_df['max_error'] < 0)
      return final_data_df.loc[np.logical_or(above_thres, invalid_output)]['Unnamed: 0'].to_numpy(dtype=str)

  # get failure list
  input_path = os.path.join(args.input_dir, 'final_data.csv')
  final_data_df = pd.read_csv(input_path)
  total_failures = get_failures(final_data_df)
  total_failures = np.array(['\"' + m + ".obj\"," for m in total_failures])

  # write failure list
  output_path = os.path.join(output_dir, 'failure_cases.txt')
  np.savetxt(output_path, total_failures, fmt='%s')