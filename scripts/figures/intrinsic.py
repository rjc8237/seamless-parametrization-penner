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
  input_dir = "output/figures/intrinsic/"
  output_dir = "output/figures/intrinsic"
  os.makedirs(output_dir, exist_ok=True)

  # set style for all data sets
  sns.set_theme()
  sns.set_style("whitegrid")
  matplotlib.rcParams['figure.figsize'] = (7, 7)
  ymax=70
  fontsize=15
  colors = ["#7c7ebc", "#c3a9d1"]
  sns.set_palette(sns.color_palette(colors))
  axisfont=15

  # file labels and corresponding angles for tests
  file_nums = ["0", "0_003", "0_03", "0_3", "3", "30",]
  label_nums = ["0", "0.003", "0.03", "0.3", "3", "30",]

  # lambda to add a data entry
  def add_data(data, X, method, angle, digits):
    thres = pow(10, -digits)
    num_models = len(X)
    converged = len(np.where(X <= thres)[0])
    failures = num_models - converged
    if len(X) > 0:
        converged_percent = converged * (100 / len(X))
        failures_percent = failures * (100 / len(X))
    else:
        converged_percent = 0
        failures_percent = 0

    data.append(
      {
        "method": method,
        "min angle": angle,
        "digits": digits,
        "converged": converged,
        "not converged": failures,
        "converged (%)": converged_percent,
        "not converged (%)": failures_percent
      }
    )

  def get_failures(final_data_df):
      above_thres = (final_data_df['max_error'] > 1e-12)
      invalid_output = (final_data_df['max_error'] < 0)
      return final_data_df.loc[np.logical_or(above_thres, invalid_output)]['Unnamed: 0'].to_numpy(dtype=str)
    

  # initialize total failure list
  n = file_nums[0]
  input_path = os.path.join(input_dir, 'regularization_' + n + ".csv")
  final_data_df = pd.read_csv(input_path)
  total_failures = get_failures(final_data_df)

  # gather data from file
  data = []
  for i, n in enumerate(file_nums):
    # Add refinement data
    input_path = os.path.join(input_dir, 'refinement_' + n + ".csv")
    final_data_df = pd.read_csv(input_path)
    X = final_data_df['max_error'].to_numpy()
    failures = get_failures(final_data_df)
    total_failures = np.intersect1d(total_failures, failures)
    for digits in [3, 6, 9, 12]:
      add_data(data, X, "refinement", label_nums[i], digits)

    # Add regularization data
    input_path = os.path.join(input_dir, 'regularization_' + n + ".csv")
    final_data_df = pd.read_csv(input_path)
    X = final_data_df['max_error'].to_numpy()
    failures = get_failures(final_data_df)
    total_failures = np.intersect1d(total_failures, failures)
    for digits in [3, 6, 9, 12]:
      add_data(data, X, "interpolation", label_nums[i], digits)
  


  # Add regularization data for 60
  input_path = os.path.join(input_dir, 'regularization_60.csv')
  final_data_df = pd.read_csv(input_path)
  X = final_data_df['max_error'].to_numpy()
  failures = get_failures(final_data_df)
  total_failures = np.intersect1d(total_failures, failures)
  for digits in [3, 6, 9, 12]:
    add_data(data, X, "interpolation", "60", digits)

  # build dataframe from data
  intrinsic_df = pd.DataFrame(data)
  print(intrinsic_df)

  # check for total failures
  print("Failures:", total_failures)

  # generate refinement plot
  fig, ax = plt.subplots(1)
  bar = sns.barplot(
    intrinsic_df.loc[intrinsic_df['digits'] == 12],
    x="min angle",
    y="not converged (%)",
    hue="method",
    palette=colors,
    ax=ax
  )
  bar.set_xlabel("min angle", fontsize=axisfont)
  bar.set_ylabel("not converged (%)", fontsize=axisfont)
  plt.setp(ax.get_legend().get_texts(), fontsize=fontsize)
  plt.setp(ax.get_legend().get_title(), fontsize=fontsize)
  #bar.set_xfont("min angle", fontsize=axisfont)
  #bar.set_ylabel('num. converged', fontsize=axisfont)
  #bar.set_yscale('log')
  #bar.set_yticks([10, 5, 2.5, 1, 0.5, 0.4, 0.3])
  bar.tick_params(labelsize=fontsize)
  #bar.set_yticks([15, 13, 11, 9, 7, 5, 3, 2, 1, 0.3])
  bar.set_yticks([25, 20, 15, 10, 7.5, 5, 2.5, 1.5, 0.5,])
  bar.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(decimals=1))

  output_path = os.path.join(output_dir, "intrinsic.png")
  fig.savefig(output_path, bbox_inches='tight')

