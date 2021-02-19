
import os
import subprocess
import time
import re


def run_macsyfinder(algo, bench_home, macsy_home, run=10):
    cwd = os.getcwd()
    if not os.path.exists(bench_home):
        os.mkdir(bench_home)
    os.chdir(bench_home)

    for algo in algos:
        subprocess.run(f"git co feat_{algo}", shell=True, check=True, stdout=subprocess.PIPE, text=True)
        for essai in range(run):
            command = f"macsyfinder " \
                      f"--sequence-db {os.path.join(macsy_home, 'data', 'base', 'subset_gembase_alphbetgammzetacidi_6thNov2018.fasta')} " \
                      f"--models TFF-SF all " \
                      f"--models-dir {os.path.join(macsy_home, 'data', 'models')} " \
                      f"--db-type gembase -w 4 " \
                      f"--out-dir {algo}_{essai}"
            subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, text=True)
            time.sleep(1)
    os.chdir(cwd)


def parse_time(log):
    pattern = "It took (\d+.\d+)sec to find best solution .*?for replicon (.+)"
    df = pd.DataFrame(columns=['replicon', 'algo', 'time'])
    match = re.match("^(.+)_(\d+)$", os.path.dirname(log))
    algo, attempt = match.groups()
    algo = os.path.split(algo)[1]
    with open(log) as log_file:
        line = log_file.readline()
        while not line.startswith('###################### Computing best solutions'):
            line = log_file.readline()
        for line in log_file:
            match = re.search(pattern, line)
            if match:
                elapse_time, replicon = match.groups()
                df = df.append({'replicon': replicon, 'algo': algo, 'time': elapse_time}, ignore_index=True)
    return df


def collate_results(log_files):
    times = pd.DataFrame(columns=['replicon', 'algo', 'time'])
    for log in log_files:
        res = parse_time(log)
        times = pd.concat([times, res], ignore_index=True)
    return times


if __name__ == '__main__':
    import glob
    import sys
    algos = ('bnb', 'bnb_max_bound', 'bnb_max_bound_all_solution', 'bnb_iter', 'mip', 'nx')
    macsy_home = os.path.abspath(os.path.dirname(__file__))
    bench_home = 'benchmark'

    if len(sys.argv) > 3:
        raise RuntimeError()
    elif len(sys.argv) == 1:
        sys.argv.append('run')
        sys.argv.append('parse')

    if 'run' in sys.argv:
        run_macsyfinder(algos, bench_home, macsy_home, run=2)

    if 'parse' in sys.argv:
        import pandas as pd
        log_files = []
        log_files = sorted(glob.glob(f'{bench_home}/*_*/macsyfinder.log'))
        executions = collate_results(log_files)
        executions.to_csv('execution.tsv', sep='\t', float_format='.2')




# ###################### Computing best solutions ######################
# Computing best solutions for GCF_000005845 (nb of systems 30)
# It took 0.02sec to find best solution (16.75) for replicon GCF_000005845
# Computing best solutions for GCF_000006725 (nb of systems 153)
# It took 0.67sec to find best solution (15.25) for replicon GCF_000006725
# Computing best solutions for GCF_000006745 (nb of systems 15)
# It took 0.01sec to find best solution (36.0) for replicon GCF_000006745
# Computing best solutions for GCF_000006765 (nb of systems 64)
# It took 0.36sec to find best solution (41.5) for replicon GCF_000006765
# Computing best solutions for GCF_000006845 (nb of systems 32)
# It took 0.03sec to find best solution (11.0) for replicon GCF_000006845
# Computing best solutions for GCF_000006905 (nb of systems 2)
# It took 0.00sec to find best solution (18.0) for replicon GCF_000006905
# Computing best solutions for GCF_000006925 (nb of systems 1)
# It took 0.00sec to find best solution (5.0) for replicon GCF_000006925
# Computing best solutions for GCF_000006945 (nb of systems 12)
# It took 0.00sec to find best solution (7.75) for replicon GCF_000006945
