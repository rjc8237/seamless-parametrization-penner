import os
import pymeshlab as pml
import numpy as np
import multiprocessing

def process_file(file_id, input_dir, output_dir, suffix):
    mesh_path = os.path.join(input_dir, str(file_id) + suffix)
    try:
        ms = pml.MeshSet()
        ms.load_new_mesh(mesh_path)
    except:
        print("Could not read mesh", file_id, flush=True)
        return

    if not ms.get_topological_measures()['is_mesh_two_manifold']:
        print("Skipping nonmanifold mesh", file_id, flush=True)
        return

    if ms.get_topological_measures()['boundary_edges'] != 0:
        print("Skipping open mesh", file_id, flush=True)
        return

    if ms.get_topological_measures()['connected_components_number'] != 1:
        print("Skipping multiple component mesh", file_id, flush=True)
        return

    print("Saving closed mesh", file_id, flush=True)
    output_path = os.path.join(output_dir, str(file_id) + ".obj")
    ms.save_current_mesh(output_path)

def main():
    input_dir = os.path.join("data", "thingi10k")
    output_dir = os.path.join("data", "thingi10k-connected-all")
    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)

    models = [f[:-len(".obj")] for f in files if f.endswith(".obj")]
    pool_args = [(m, input_dir, output_dir, '.obj') for m in models]
    with multiprocessing.Pool(processes=42) as pool:
        pool.starmap(process_file, pool_args, chunksize=1)
    print("Done with obj")

    models = [f[:-len(".stl")] for f in files if f.endswith(".stl")]
    models = [m for m in models if m not in ['49911', '286163']]
    pool_args = [(m, input_dir, output_dir, '.stl') for m in models]
    with multiprocessing.Pool(processes=42) as pool:
        pool.starmap(process_file, pool_args, chunksize=1)
    print("Done with stl")

if __name__ == "__main__":
    main()
