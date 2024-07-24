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
  parser.add_argument("-o", "--output_dir",           help="directory to write output",
                                                    type=str)
  args = parser.parse_args()
  # TODO Move to bash script
  input = "output/figures/tetwild_input/mesh_info.csv"
  output_dir = "output/figures/tetwild_input"
  os.makedirs(output_dir, exist_ok=True)

  # Load data frame of mesh info
  mesh_info_df = pd.read_csv(input)

  # Stretch factors for all data sets
  sns.set_theme()
  sns.set_style("whitegrid")
  matplotlib.rcParams['figure.figsize'] = (7, 7)
  ylim=30
  axisfont=45
  labelfont=45

  colors = ["#4c95c1"]
  sns.set_palette(sns.color_palette(colors))

  # Plot number of faces
  X = mesh_info_df['num_faces'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', log_scale=True, binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_ylim(0,ylim)
  hist.set_xlabel('face count', fontsize=axisfont)

  hist.tick_params(labelsize=45)
  hist.set_xticks([1e2, 1e4, 1e6])
  hist.set_yticks([0, 10, 20, 30])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "num_faces.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot genus
  xmax = 20
  X = mesh_info_df['genus'].to_numpy()
  num_outlier = len(np.where(X >= xmax)[0])
  print ("{} cones about threshold".format(len(np.where(X >= xmax)[0])))
  print ("{} genus above threshold".format(num_outlier))
  X = np.concatenate((X[np.where(X < xmax)], np.full(num_outlier, xmax)))
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_xlabel('genus', fontsize=axisfont)
  hist.set_ylim(0,60)

  hist.tick_params(labelsize=labelfont)
  hist.set_xticks([5, 10, 15])
  hist.set_yticks([0, 20, 40, 60])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "genus.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot cone count
  xmax=500
  X = mesh_info_df['num_cones'].to_numpy()
  num_outlier = len(np.where(X >= xmax)[0])
  print ("{} cones about threshold".format(len(np.where(X >= xmax)[0])))
  X = np.concatenate((X[np.where(X < xmax)], np.full(num_outlier, xmax)))

  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_ylim(0,ylim)
  hist.set_xlabel('cone count', fontsize=axisfont)

  hist.set_xticks([150, 300, 450])
  hist.set_yticks([0, 10, 20, 30])
  hist.tick_params(labelsize=labelfont)
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "num_cones.png")
  fig.savefig(output_path, bbox_inches='tight')
  