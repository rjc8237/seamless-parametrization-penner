# Script to conformally project a similarity metric to holonomy constraints

import os, sys
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, '..', '..', 'py')
sys.path.append(module_dir)
import numpy as np
import argparse
import pandas as pd

if __name__ == "__main__":
    # Parse arguments for the script
    parser = argparse.ArgumentParser("Consolidate data from iteration data logs")
    parser.add_argument("--data_dir",           help="directory with output data",
                                                     type=str)
    parser.add_argument("--output_dir",           help="directory to write data",
                                                     type=str, default="")
    args = parser.parse_args()
    output_dir = args.output_dir
    if output_dir == "":
        output_dir = args.data_dir

    files = os.listdir(args.data_dir)
    models = [f[:-len("_output")] for f in files if f.endswith("_output")]

    keys = ['num_iter', 'max_error', 'rmse', 'rrmse', 'rmsre', 'time']
    energies = {key:[] for key in keys}
    energies['solve_time'] = []
    for m in models:
        for key in keys:
            try:
                iteration_data_dir = os.path.join(args.data_dir, m+'_output', 'iteration_data_log.csv')
                iteration_data = pd.read_csv(iteration_data_dir)
                energies[key].append(float(iteration_data[key].tail(1)))
            except:
                energies[key].append(-1)
        try:
            iteration_data_dir = os.path.join(args.data_dir, m+'_output', 'iteration_data_log.csv')
            iteration_data = pd.read_csv(iteration_data_dir)
            energies['solve_time'].append(np.average(iteration_data['solve_time'].to_numpy()))
        except:
            energies['solve_time'].append(-1)


    energies_df = pd.DataFrame(energies, index=models)
    energies_df.to_csv(os.path.join(output_dir, 'final_data.csv'))
