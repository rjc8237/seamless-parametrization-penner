import os, sys
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, '..', '..', 'py')
sys.path.append(module_dir)
import numpy as np
import optimization_py as opt 
import holonomy_py as holonomy
import argparse, multiprocessing
import pandas as pd
import igl
import math

invalid_meshes = [
    "702414_sf_1.obj",
    "481225_sf.obj",
    "591243_sf.obj",
    "1582423_sf.obj",
    "1013015_sf.obj",
    "471985_sf.obj",
    "471984_sf.obj",
    "838512_sf.obj",
    "42041_sf_3.obj",
    "481225_sf.obj",
    "358257_sf.obj",
    "754638_sf.obj",
    "94019_sf.obj",
    "39893_sf.obj",
    "1083353_sf.obj",
    "44948_sf_3.obj",
    "96776_sf_2.obj",
    "39011_sf_2.obj",
    "929562_sf.obj",
    "370993_sf.obj",
    "44949_sf_3.obj",
    "838520_sf_1.obj",
    "108447_sf_2.obj",
    "199663_sf.obj",
    "1222709_sf.obj",
    "83676_sf_1.obj",
    "110372_sf_1.obj",
    "466802_sf.obj",
    "82536_sf_2.obj",
    "99468_sf_1.obj",
    "916909_sf_1.obj",
    "1368069_sf.obj",
    "103354_sf_1.obj",
    "1005586_sf_1.obj",
    "1688588_sf_1.obj"
] 


def get_mesh_info(data_dir, m):
  try:
    V, F = igl.read_triangle_mesh(os.path.join(data_dir, m + '.obj'))
    Th_hat = np.loadtxt(os.path.join(data_dir, m + "_Th_hat"), dtype=float)
    rotation_form = np.loadtxt(os.path.join(data_dir, m + "_kappa_hat"), dtype=float)
  except:
    return {}

  # Get cones
  is_bd = igl.is_border_vertex(V, F)
  _, vtx_reindex = opt.fv_to_double(V, F, V, F, Th_hat, [], False)
  cones = np.array([id for id in range(len(Th_hat)) if np.abs(Th_hat[id]-2*math.pi) > 1e-15 and not is_bd[id]], dtype=int)
  cones = [idx for idx in range(len(vtx_reindex)) if vtx_reindex[idx] in cones]

  # Generate initial similarity metric
  free_cones = []
  marked_metric_params = holonomy.MarkedMetricParameters()
  marked_metric, _ = holonomy.generate_marked_metric(V, F, V, F, Th_hat, rotation_form, free_cones, marked_metric_params)

  # Generate strings of holonomies
  holonomies = ""
  for kappa in marked_metric.kappa_hat:
    holonomies += str(kappa) + ";"

  # Generate strings of dual loop lengths
  basis_loop_lengths = ""
  #homology_basis_loops = marked_metric.get_homology_basis_loops()
  #for basis_loop in homology_basis_loops:
  #  basis_loop_lengths += str(len(basis_loop)) + ";"

  mesh_info = {}
  mesh_info['name'] = m
  mesh_info['num_vertices'] = marked_metric.n_vertices()
  mesh_info['num_edges'] = marked_metric.n_edges()
  mesh_info['num_faces'] = marked_metric.n_faces()
  mesh_info['genus'] = marked_metric.n_homology_basis_loops() / 2
  mesh_info['num_cones'] = len(cones)
  mesh_info['holonomies'] = holonomies
  #mesh_info['basis_loop_lengths'] = basis_loop_lengths

  return mesh_info

if __name__ == "__main__":
  # Parse arguments for the script
  parser = argparse.ArgumentParser("Get information about meshes")
  parser.add_argument("--mesh_dir",           help="directory with meshes",
                                                    type=str)
  parser.add_argument("--output_dir",           help="directory to output mesh info data",
                                                    type=str)
  args = parser.parse_args()

  files = os.listdir(args.mesh_dir)
  files = [f for f in files if f not in invalid_meshes]
  models = [f[:-len(".obj")] for f in files if f.endswith(".obj")]

  pool_args = [(args.mesh_dir, m) for m in models]
  with multiprocessing.Pool(processes=8) as pool:
      all_mesh_info = pool.starmap(get_mesh_info, pool_args)

  mesh_info_df = pd.DataFrame(all_mesh_info)
  mesh_info_df.to_csv(os.path.join(args.output_dir, "mesh_info.csv"))

