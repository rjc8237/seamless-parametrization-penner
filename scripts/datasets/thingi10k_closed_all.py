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


    if ms.get_topological_measures()['connected_components_number'] == 1:
        print("Saving closed mesh", file_id, flush=True)
        output_path = os.path.join(output_dir, str(file_id) + ".obj")
        ms.save_current_mesh(output_path)
    else:
        print("Splitting and saving closed mesh", file_id, flush=True)
        ms.generate_splitting_by_connected_components(delete_source_mesh=True)
        for i in np.arange(ms.mesh_number()) + 1:
            if not ms.mesh_id_exists(i):
                print("Invalid components")
                continue
            output_path = os.path.join(output_dir, str(file_id) + "_" + str(i) + ".obj")
            ms.set_current_mesh(i)
            ms.save_current_mesh(output_path)

def main():
    input_dir = os.path.join("data", "thingi10k")
    output_dir = os.path.join("data", "thingi10k-closed-all")
    os.makedirs(output_dir, exist_ok=True)


    files = os.listdir(input_dir)

    models = [f[:-len(".obj")] for f in files if f.endswith(".obj")]

    pool_args = [(m, input_dir, output_dir, '.obj') for m in models]
    with multiprocessing.Pool(processes=52) as pool:
        pool.starmap(process_file, pool_args, chunksize=1)
    print("Done with obj")

    models = [f[:-len(".stl")] for f in files if f.endswith(".stl")]
    models = [m for m in models if m not in ['49911',]]

    #finished_files = os.listdir(output_dir)
    #finished_models = [f[:-len(".obj")] for f in finished_files if f.endswith(".obj")]
    #finished_models = [m.split('_')[0] for m in finished_models]
    #models = list(set(models) - set(finished_models))

    pool_args = [(m, input_dir, output_dir, '.stl') for m in models]
    with multiprocessing.Pool(processes=52) as pool:
        pool.starmap(process_file, pool_args, chunksize=1)
    print("Done with stl")

    return

    for m in models:
        process_file(m, input_dir, output_dir, '.stl')
    

    models = [f[:-len(".obj")] for f in files if f.endswith(".obj")]
    pool_args = [(m, input_dir, output_dir, '.obj') for m in models]
    with multiprocessing.Pool(processes=48) as pool:
        pool.starmap(process_file, pool_args, chunksize=1)

if __name__ == "__main__":
    main()
