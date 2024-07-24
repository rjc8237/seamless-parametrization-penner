import os, sys
script_dir = os.path.dirname(__file__)
module_dir = os.path.join(script_dir, '..', '..', 'py')
sys.path.append(module_dir)
import numpy as np
import optimize_impl.energies as energies
import optimize_impl.analysis as analysis
import seaborn as sns
import igl
import argparse, multiprocessing

def symmetric_dirichlet_histogram(uv_dir, output_dir, m):
    # Get mesh and test name
    suffix=""
    if (suffix == ""):
        name = m
    else:
        name = m + '_' + suffix

    # Load uv information
    try:
        v3d, uv, _, f, fuv, _ = igl.read_obj(os.path.join(uv_dir, name + ".obj"))
    except:
        print("Could not load mesh")
        return

    # Get bin range (or None if no range values provided)
    #binrange = (args['bin_min'], args['bin_max'])
    binrange = (0, 5)

    # Get histogram color
    color_dict = {
        'red': "#b90f29",
        'blue': "#3c4ac8"
    }
    color = color_dict['blue']
    colors = ["#7851a9",]

    # Set palette
    sns.set_palette(colors)

    # Get symmetric Dirichlet energy per face
    print("Generating energy")
    uv_embed = np.zeros((len(uv), 3))
    uv_embed[:,:2] = uv[:,:2]
    X = energies.sym_dirichlet_vf(v3d, f, uv_embed, fuv) - 4

    os.makedirs(os.path.join(output_dir, 'colormap_histograms'), exist_ok=True)

    print("Generating histogram")
    label = 'sym dir'
    output_path = os.path.join(
        output_dir,
        'colormap_histograms',
        name+"_sym_dir.png"
    )
    ylim = 65
    analysis.generate_histogram(X, label, binrange, output_path, ylim=ylim,)

if __name__ == "__main__":
  # Parse arguments for the script
  parser = argparse.ArgumentParser("Get information about meshes")
  parser.add_argument("--mesh_dir",           help="directory with meshes",
                                                    type=str)
  parser.add_argument("--output_dir",           help="directory for output",
                                                    type=str)
  parser.add_argument("--suffix",           help="suffix of output",
                                                    type=str, default="")
  args = parser.parse_args()

  files = os.listdir(args.mesh_dir)
  models = [f[:-len("_output")] for f in files if f.endswith("_output")]
  pool_args = [(os.path.join(args.mesh_dir, m + "_output"), args.output_dir, m + '_' + args.suffix) for m in models]

  with multiprocessing.Pool(processes=8) as pool:
      all_mesh_info = pool.starmap(symmetric_dirichlet_histogram, pool_args)


