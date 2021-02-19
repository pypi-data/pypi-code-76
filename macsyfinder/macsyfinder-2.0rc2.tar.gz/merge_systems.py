import pandas as pd


def merge_systems_pd(files):
    df = pd.read_csv(files[0], comment="#", sep="\t")
    for file in files[1:]:
        new_df = pd.read_csv(file, comment="#", sep="\t")
        df = df.concat(new_df)
    return df


def merge_systems(files, out):
    with open(out, 'w') as f_out:
        first = True
        for file in files:
            with open(file) as fh_in:
                for line in fh_in:
                    if first and line.startswith('#'):
                        pass
                    elif first and line.startswith('replicon'):
                        first = False
                    elif line.startswith('#'):
                        continue
                    elif line.startswith('replicon'):
                        continue

                    f_out.write(line)


def merge_best_solutions(files):
    df = pd.read_csv(files[0], comment="#", sep="\t")
    for file in files[1:]:
        last_sol_id = df.iloc[-1]['sol_id']
        new_df = pd.read_csv(file, comment="#", sep="\t")
        new_df['sol_id'] = new_df['sol_id'] + last_sol_id
        df = pd.concat([df, new_df])

    return df


def merge_all_best_solutions(files, out):
    with open(out, 'w') as f_out:
        last_sol_id = 0
        first = True
        for file in files:
            with open(file) as fh_in:
                for line in fh_in:
                    if first and line.startswith('sol_id'):
                        first = False
                        new_line = line
                    elif line.startswith('sol_id'):
                        continue
                    elif first and line.startswith('#'):
                        new_line = line
                    elif line.startswith('#'):
                        continue
                    elif line.startswith('\n'):
                        new_line = line
                    elif line:
                        fields = line.split('\t')
                        try:
                            new_sol_id = int(fields[0]) + last_sol_id
                        except ValueError as err:
                            print(f"new_sol_id = int({fields[0]}) + {last_sol_id}")
                            raise err
                        fields[0] = str(new_sol_id)
                        new_line = '\t'.join(fields)
                    f_out.write(new_line)
            last_sol_id = new_sol_id


# df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'],
#                     'B': ['B0', 'B1', 'B2', 'B3'],
#                     'C': ['C0', 'C1', 'C2', 'C3'],
#                     'D': ['D0', 'D1', 'D2', 'D3']},
#                     index=[0, 1, 2, 3])
#

if __name__ == '__main__':
    import os
    results_dir = ['macsyfinder-20201209_17-54-53', 'macsyfinder-20201209_17-47-41', 'macsyfinder-20201202_15-17-58']
    all_best_solutions_files = [os.path.join(d, 'all_best_solutions.tsv') for d in results_dir]
    best_solution_files = [os.path.join(d, 'best_solution.tsv') for d in results_dir]
    all_systems_files = [os.path.join(d, 'all_systems.tsv') for d in results_dir]
    merge_all_best_solutions(all_best_solutions_files, "merged_all_best_sol.tsv")
    merge_systems(best_solution_files, "merged_best_sol.tsv")
    merge_systems(all_systems_files, "merged_all_systems.tsv")