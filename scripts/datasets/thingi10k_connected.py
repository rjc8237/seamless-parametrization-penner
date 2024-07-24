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
    input_dir = os.path.join("data", "thingi10k-connected-all")
    output_dir = os.path.join("data", "thingi10k-connected-extra")
    os.makedirs(output_dir, exist_ok=True)

    files = os.listdir(input_dir)
    models = [f for f in files if f.endswith(".obj")]
    models = ['270395', '131971', '252653', '60845', '97597', '136405', '76539', '100031', '91588', '1716286', '236171', '112965', '94900', '91140', '99910', '162340', '55956', '51142', '41732', '994786', '83003', '376253', '372112', '66678', '99912', '994785', '44064', '51141', '43859', '67564', '44739', '71761', '77021', '81262', '117011', '56103', '118656', '921798', '128914', '1176423', '133994', '60843', '99911', '97431', '372090', '91589', '131438', '917937', '298321', '71566', '60844', '80441']
    models = [f + '.obj' for f in models]

    pool_args = [(m, input_dir, output_dir) for m in models]
    with multiprocessing.Pool(processes=48) as pool:
        pool.starmap(process_file, pool_args, chunksize=1)

if __name__ == "__main__":
    main()
