# Script to conformally project a similarity metric to holonomy constraints

import os
import numpy as np
import argparse

if __name__ == "__main__":
    # Parse arguments for the script
    parser = argparse.ArgumentParser("Consolidate data from iteration data logs")
    parser.add_argument("--mesh_dir",           help="directory with meshes",
                                                     type=str)
    parser.add_argument("--output_dir",           help="directory to write output",
                                                     type=str, default="./")
    parser.add_argument("--min_cone",           help="minimum allowed cone",
                                                     type=int, default=0)
    parser.add_argument("--only_cones",           help="only look for cones",
                                                     action="store_true")
    args = parser.parse_args()

    files = os.listdir(args.mesh_dir)
    models = [f[:-len(".obj")] for f in files if f.endswith(".obj")]

    invalid_models = []
    for m in models:
        Th_hat = np.loadtxt(os.path.join(args.mesh_dir, m + "_Th_hat"), dtype=float)

        # General invalid cases
        if (np.min(Th_hat) < (args.min_cone * np.pi / 2.) + 1e-3):
            print("{} has a {} cone".format(m, np.min(Th_hat)))
            invalid_models.append('"'+m+'.obj",')

        if args.only_cones:
            continue
        
        # Torus invalid cases
        num_3_cones = np.count_nonzero(np.abs(Th_hat < (2.0 * np.pi - 1e-3)))
        num_5_cones = np.count_nonzero(np.abs(Th_hat > (2.0 * np.pi + 1e-3)))
        genus = int(1.0 + np.sum(Th_hat - 2 * np.pi) / (4.0 * np.pi))
        if ((num_3_cones == 1) and (num_5_cones == 1) and (genus == 1)):
            print("{} is a torus with a cone pair".format(m))
            invalid_models.append('"'+m+'.obj",')
        if ((num_3_cones == 0) and (num_5_cones == 0) and (genus == 1)):
            print("{} is a torus with no cones".format(m))
            invalid_models.append('"'+m+'.obj",')

    np.savetxt(os.path.join(args.output_dir, 'invalid_cones.txt'), np.array(invalid_models), fmt='%s')

