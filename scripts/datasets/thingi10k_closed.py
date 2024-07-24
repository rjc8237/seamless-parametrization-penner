import os.path
from subprocess import check_call
import multiprocessing

def process_file(file, input_dir, output_dir):
    exec_path = os.path.join("./", "build", "bin", "generate_frame_field")
    command = exec_path + " -i " + input_dir + " --mesh " + file + " -o " + output_dir
    try:
        check_call(command.split())
    except:
        print("Could not process mesh")

def main():
    input_dir = os.path.join("data", "thingi10k-closed-all")
    output_dir = os.path.join("data", "thingi10k-closed")
    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)
    models = [f for f in files if f.endswith(".obj")]

    pool_args = [(m, input_dir, output_dir) for m in models]
    with multiprocessing.Pool(processes=48) as pool:
        pool.starmap(process_file, pool_args, chunksize=1)

if __name__ == "__main__":
    main()
