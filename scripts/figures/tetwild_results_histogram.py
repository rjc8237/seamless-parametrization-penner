import os, sys
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, '..', 'py')
sys.path.append(module_dir)
import numpy as np
import argparse
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt


if __name__ == "__main__":
  # Parse arguments for the script
  parser = argparse.ArgumentParser("Consolidate data from iteration data logs")
  parser.add_argument("-i", "--input",           help="mesh info csv file",
                                                    type=str)
  parser.add_argument("-o", "--output_dir",           help="figure output directory",
                                                    type=str)
  args = parser.parse_args()
  input = args.input
  output_dir = args.output_dir
  # TODO Move to bash script
  input = "output/figures/tetwild_results/final_data.csv"
  output_dir = "output/figures/tetwild_results"
  os.makedirs(output_dir, exist_ok=True)

  # Load data frame of mesh info
  mesh_info_df = pd.read_csv(input)

  # Stretch factors for all data sets
  sns.set_theme()
  sns.set_style("whitegrid")
  matplotlib.rcParams['figure.figsize'] = (7, 7)

  ymax=70
  fontsize=45
  colors = ["#4c95c1"]
  sns.set_palette(sns.color_palette(colors))
  axisfont=45


  # Plot rmsre
  xmax=0.5
  X = mesh_info_df['rmsre'].to_numpy()
  num_outlier = len(np.where(X >= xmax)[0])
  print ("{} RMSE above threshold".format(len(np.where(X >= xmax)[0])))
  X = np.concatenate((X[np.where(X < xmax)], np.full(num_outlier, xmax)))
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_xlabel('RMSRE', fontsize=axisfont)
  hist.set_xlim(0,xmax)
  hist.set_ylim(0,35)

  hist.tick_params(labelsize=fontsize)
  hist.set_xticks([0.2, 0.4])
  hist.set_yticks([0, 10, 20, 30])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "rmsre.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot number of iterations 
  xmax=50
  X = mesh_info_df['num_iter'].to_numpy()
  X = X[np.where(X < xmax)]
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', binrange=binrange, ax=ax)

  hist.set_ylim(0,ymax)
  hist.set_ylim(0,ymax)
  hist.set_ylabel('')
  hist.set_xlabel('iterations', fontsize=fontsize)

  hist.tick_params(labelsize=fontsize)
  hist.set_xticks([15, 30, 45])
  hist.set_yticks([0, 20, 40, 60])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "iter.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot solve time per iteration
  xmax=0.125
  X = mesh_info_df['solve_time'].to_numpy()
  num_outlier = len(np.where(X >= xmax)[0])
  print ("{} times above threshold".format(len(np.where(X >= xmax)[0])))
  X = np.concatenate((X[np.where(X < xmax)], np.full(num_outlier, xmax)))
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', binrange=binrange, ax=ax)

  hist.tick_params(labelsize=fontsize)
  hist.set_xticks([0.05, 0.1])
  hist.set_yticks([0, 20, 40, 60])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  hist.set_xlim(0,xmax)
  hist.set_ylim(0,ymax)
  hist.set_ylabel('')
  hist.set_xlabel('solve time (s)', fontsize=fontsize)

  output_path = os.path.join(output_dir, "solve_time.png")
  fig.savefig(output_path, bbox_inches='tight')
