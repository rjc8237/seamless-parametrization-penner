# Script to list meshes below a given size

import os
import igl
import numpy as np
import argparse

if __name__ == "__main__":
    # Parse arguments for the script
    parser = argparse.ArgumentParser("Generate a list of small meshes")
    parser.add_argument("--mesh_dir",           help="directory with meshes",
                                                     type=str)
    parser.add_argument("--output_dir",           help="directory to write output",
                                                     type=str, default="./")
    parser.add_argument("--max_size",           help="list meshes below this size",
                                                     type=int, default=25000)
    args = parser.parse_args()

    files = os.listdir(args.mesh_dir)
    meshes = [f[:-len(".obj")] for f in files if f.endswith(".obj")]

    small_meshes= []
    for mi, m in enumerate(meshes):
        if (mi % 1000) == 0:
            print("{} meshes processed".format(mi))

        # check number of faces
        v3d_orig, f_orig = igl.read_triangle_mesh(os.path.join(args.mesh_dir, m+'.obj'))
        if (len(f_orig) > args.max_size):
            small_meshes.append(m)
        
    np.savetxt(os.path.join(args.output_dir, 'large_meshes.txt'), np.array(small_meshes), fmt='%s')
    