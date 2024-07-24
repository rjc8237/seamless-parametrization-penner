import os
import argparse, multiprocessing
import pandas as pd
import numpy as np

def compute_data_at_rmse_threshold(newton_dir, projection_dir, m):
  threshold_data = {}
  try:
    newton_iteration_data_dir = os.path.join(newton_dir, m+'_output', 'iteration_data_log.csv')
    newton_iteration_data = pd.read_csv(newton_iteration_data_dir)

    projection_iteration_data_dir = os.path.join(projection_dir, m+'_output', 'iteration_data_log.csv')
    projection_iteration_data = pd.read_csv(projection_iteration_data_dir)
    conformal_solve_times = pd.read_csv(os.path.join(projection_dir, m+'_output', 'conformal_iteration_times.csv'))[' solve_time'].to_numpy()
    projection_solve_times = pd.read_csv(os.path.join(projection_dir, m+'_output', 'projection_solve_times.csv'))['solve_time'].to_numpy()

    threshold_data['name'] = m
    newton_rmse = float(newton_iteration_data['rmse'].tail(1))

    threshold_data['newton_rmse'] = newton_rmse
    threshold_data['newton_solves'] = int(newton_iteration_data['num_iter'].tail(1))
    threshold_data['newton_time'] = float(newton_iteration_data['time'].tail(1))
    threshold_data['newton_solve_time'] = np.average(newton_iteration_data['solve_time'].to_numpy())
    threshold_data['newton_energy'] = np.average(newton_iteration_data['l2_energy'].to_numpy())

    def get_threshold_value(key):
      return projection_iteration_data[(projection_iteration_data['rmse'] < newton_rmse)][key].head(1)

    threshold_data['projection_rmse'] = float(get_threshold_value('rmse'))
    threshold_data['projection_solves'] = float(get_threshold_value('num_linear_solves'))
    threshold_data['projection_time'] = float(get_threshold_value('time'))
    threshold_data['projection_solve_time'] = np.average(np.concatenate((conformal_solve_times, projection_solve_times)))
    threshold_data['projection_final_energy'] = float(projection_iteration_data['energy'].tail(1))
    return threshold_data
  except:
    return {
      'name': m,
    }

if __name__ == "__main__":
  # Parse arguments for the script
  parser = argparse.ArgumentParser("Get information about meshes")
  args = parser.parse_args()

  newton_dir='output/figures/performance'
  projection_dir='output/figures/optimization'
  output_dir='output/figures/performance'
  os.makedirs(output_dir, exist_ok=True)

  files = os.listdir(newton_dir)
  models = [f[:-len("_output")] for f in files if f.endswith("_output")]
  pool_args = [(newton_dir, projection_dir, m) for m in models]
  with multiprocessing.Pool(processes=8) as pool:
      all_mesh_info = pool.starmap(compute_data_at_rmse_threshold, pool_args)

  mesh_info_df = pd.DataFrame(all_mesh_info)
  mesh_info_df.to_csv(os.path.join(output_dir, "projection_comparison.csv"))

