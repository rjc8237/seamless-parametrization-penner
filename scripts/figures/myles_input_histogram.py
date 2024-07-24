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
  input = "output/figures/myles_input/mesh_info.csv"
  output_dir = "output/figures/myles_input"
  os.makedirs(output_dir, exist_ok=True)

  # Load data frame of mesh info
  mesh_info_df = pd.read_csv(input)

  # Stretch factors for all data sets
  sns.set_theme()
  sns.set_style("whitegrid")
  matplotlib.rcParams['figure.figsize'] = (7, 7)
  ylim=50
  axisfont=45
  labelfont=45

  colors = ["#e0a96c"]
  sns.set_palette(sns.color_palette(colors))

  # Plot number of faces
  X_num_faces = mesh_info_df['num_faces'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X_num_faces, bins = 20, stat='percent', log_scale=True, binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_xlabel('face count', fontsize=axisfont)
  hist.set_ylim(0,ylim)

  hist.tick_params(labelsize=axisfont)
  hist.set_xticks([1e3, 1e4, 1e5])
  hist.set_yticks([0, 15, 30, 45])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))
  
  output_path = os.path.join(output_dir, "num_faces.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot genus
  X_genus = mesh_info_df['genus'].to_numpy()
  print ("{} genus above threshold".format(len(np.where(X_genus >= 25)[0])))
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X_genus, bins = 20, stat='percent', binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_xlabel('genus', fontsize=axisfont)
  hist.set_ylim(0,100)

  hist.tick_params(labelsize=labelfont)
  hist.set_xticks([25, 50, 75])
  hist.set_yticks([0, 30, 60, 90])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "genus.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot cone count
  X_num_cones = mesh_info_df['num_cones'].to_numpy()
  print ("{} cones about threshold".format(len(np.where(X_num_cones >= 500)[0])))
  X_num_cones = X_num_cones[np.where(X_num_cones < 500)]
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X_num_cones, bins = 20, stat='percent', binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_ylim(0,ylim)

  hist.tick_params(labelsize=labelfont)
  hist.set_xticks([150, 300, 450])
  hist.set_yticks([0, 15, 30, 45])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  hist.set_xlabel('cone count', fontsize=axisfont)

  output_path = os.path.join(output_dir, "num_cones.png")
  fig.savefig(output_path, bbox_inches='tight')
  