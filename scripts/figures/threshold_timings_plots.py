import os
import argparse
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt

if __name__ == "__main__":
  # Parse arguments for the script
  parser = argparse.ArgumentParser("Get information about meshes")
  args = parser.parse_args()
  
  input_dir='output/figures/performance/projection_comparison.csv'
  output_dir='output/figures/performance'

  os.makedirs(output_dir, exist_ok=True)

  # Load data frame of mesh info
  threshold_df = pd.read_csv(input_dir)

  # Stretch factors for all data sets
  colors = ["#2bac4a"]
  #sns.set_theme()
  sns.set_style("whitegrid")
  sns.set_palette(sns.color_palette(colors))
  matplotlib.rcParams['figure.figsize'] = (7, 7)
  fontsize=45

  # Plot newton and projection solve counts
  X = threshold_df['newton_solves'].to_numpy()
  Y = threshold_df['projection_solves'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  scatter = sns.scatterplot(x=X, y=Y, alpha=0.5, ax=ax, s=45)

  diag = np.linspace(0, 100, 100)
  ax.plot(diag, diag, color="#b90f29", alpha=0.5)

  scatter.set_xlim(0,100)
  scatter.set_ylim(0,100)
  scatter.set_xlabel('newton', fontsize=fontsize)
  scatter.set_ylabel('projection', fontsize=fontsize)

  scatter.tick_params(labelsize=fontsize)
  scatter.set_xticks([30, 60, 90])
  scatter.set_yticks([0, 30, 60, 90])

  output_path = os.path.join(output_dir, "threshold_solves.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot newton and projection solve time 
  X = threshold_df['newton_solve_time'].to_numpy()
  Y = threshold_df['projection_solve_time'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  scatter = sns.scatterplot(x=X, y=Y, alpha=0.5, ax=ax, s=45)

  diag = np.linspace(0, 1, 100)
  ax.plot(diag, diag, color="#b90f29", alpha=0.5)

  scatter.set_xlabel('newton', fontsize=fontsize)
  scatter.set_ylabel('projection', fontsize=fontsize)
  scatter.set_xlim(0, 1)
  scatter.set_ylim(0, 1)

  scatter.tick_params(labelsize=fontsize)
  scatter.set_xticks([0.3, 0.6, 0.9])
  scatter.set_yticks([0, 0.3, 0.6, 0.9])

  output_path = os.path.join(output_dir, "threshold_solve_time.png")
  fig.savefig(output_path, bbox_inches='tight')

  # Plot newton and projection energy
  X = threshold_df['newton_energy'].to_numpy()
  Y = threshold_df['projection_final_energy'].to_numpy()
  fig, ax = plt.subplots(1)
  binrange=None
  scatter = sns.scatterplot(x=X, y=Y, alpha=0.5, ax=ax, s=45)

  diag = np.linspace(0, 1e5, 100)
  ax.plot(diag, diag, color="#b90f29", alpha=0.5)

  scatter.set_xlabel('newton', fontsize=fontsize)
  scatter.set_ylabel('projection', fontsize=fontsize)
  scatter.set_xlim(0, 15000)
  scatter.set_ylim(0, 15000)

  scatter.tick_params(labelsize=fontsize)
  scatter.set_xticks([5000, 10000])
  scatter.set_yticks([5000, 10000])

  output_path = os.path.join(output_dir, "final_energy.png")
  fig.savefig(output_path, bbox_inches='tight')
