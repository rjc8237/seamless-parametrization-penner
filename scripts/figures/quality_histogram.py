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
from invalid_meshes import *


if __name__ == "__main__":
  # Parse arguments for the script
  parser = argparse.ArgumentParser("Consolidate data from iteration data logs")
  parser.add_argument("-i", "--input",           help="mesh info csv file",
                                                    type=str)
  parser.add_argument("-o", "--output_dir",           help="directory to write output",
                                                    type=str)
  args = parser.parse_args()
  input = "output/figures/quality/sym_dir_energy.csv"
  output_dir = "output/figures/quality"
  os.makedirs(output_dir, exist_ok=True)

  # Load data frame of mesh info
  mesh_info_df = pd.read_csv(input)

  # Stretch factors for all data sets
  sns.set_theme()
  sns.set_style("whitegrid")
  matplotlib.rcParams['figure.figsize'] = (7, 7)
  ylim=52.5
  xlim=1e7
  axisfont=45
  labelfont=45

  colors = ["#7851a9"]
  sns.set_palette(sns.color_palette(colors))

  # Plot newton quality
  X = mesh_info_df['newton'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', log_scale=True, binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_ylim(0,ylim)
  hist.set_xlim(0,xlim)
  hist.set_xlabel('avg sym. Dir', fontsize=axisfont)

  hist.tick_params(labelsize=45)
  hist.set_xticks([1, 1e2, 1e4, 1e6])
  hist.set_yticks([0, 15, 30, 45])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "newton.png")
  fig.savefig(output_path, bbox_inches='tight') # Plot newton quality

  colors = ["#7851a9"]
  sns.set_palette(sns.color_palette(colors))

  # Plot optimized quality
  X = mesh_info_df['optimized'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X, bins = 20, stat='percent', log_scale=True, binrange=binrange, ax=ax)

  hist.set_ylabel("")
  hist.set_ylim(0,ylim)
  hist.set_xlim(0,xlim)
  hist.set_xlabel('avg sym. Dir', fontsize=axisfont)

  hist.tick_params(labelsize=45)
  hist.set_xticks([1, 1e2, 1e4, 1e6])
  hist.set_yticks([0, 15, 30, 45])
  hist.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=0))

  output_path = os.path.join(output_dir, "optimized.png")
  fig.savefig(output_path, bbox_inches='tight')

  exit()

  # Plot genus
  xmax = 20
  X = mesh_info_df['genus'].to_numpy()
  print ("{} genus above threshold".format(len(np.where(X >= xmax)[0])))
  X = X[np.where(X < xmax)]
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
  print ("{} cones about threshold".format(len(np.where(X >= xmax)[0])))
  X = X[np.where(X< 500)]

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
  
  exit()

  # Plot number of edges
  X_num_edges = mesh_info_df['num_edges'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X_num_edges, bins = 20, stat='percent', log_scale=True, binrange=binrange, ax=ax)
  set_default(hist)
  hist.set_ylim(0,ylim)
  hist.set_xlabel('edge count', fontsize=axisfont)
  hist.tick_params(labelsize=labelfont)
  hist.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(15))
  output_path = os.path.join(output_dir, "num_edges.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot number of vertices
  X_num_vertices = mesh_info_df['num_vertices'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.histplot(X_num_vertices, bins = 20, stat='percent', log_scale=True, binrange=binrange, ax=ax)
  set_default(hist)
  hist.set_ylim(0,ylim)
  hist.set_xlabel('vertex count', fontsize=axisfont)
  hist.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(15))
  hist.tick_params(labelsize=labelfont)
  output_path = os.path.join(output_dir, "num_vertices.png")
  fig.savefig(output_path, bbox_inches='tight')


  # Plot genus over number edges
  X_num_edges = mesh_info_df['num_edges'].to_numpy()
  X_genus = mesh_info_df['genus'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.scatterplot(x=X_num_edges, y=X_genus, alpha=0.5, ax=ax)
  set_default(hist)
  hist.set_xscale('log')
  hist.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(15))
  #hist.set_yscale('log')
  hist.set_xlabel('edges', fontsize=axisfont)
  hist.set_ylabel('genus', fontsize=axisfont)
  hist.tick_params(labelsize=labelfont)
  output_path = os.path.join(output_dir, "genus_over_edge.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot genus over number edges
  X_num_vertices = mesh_info_df['num_vertices'].to_numpy()
  X_num_cones = mesh_info_df['num_cones'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  hist = sns.scatterplot(x=X_num_vertices, y=X_num_cones, alpha=0.5, ax=ax)
  set_default(hist)
  hist.set_xscale('log')
  #hist.set_yscale('log')
  hist.set_xlabel('vertices', fontsize=axisfont)
  hist.set_ylabel('cones', fontsize=axisfont)
  hist.tick_params(labelsize=labelfont)
  output_path = os.path.join(output_dir, "cones_over_vertices.png")
  fig.savefig(output_path, bbox_inches='tight')