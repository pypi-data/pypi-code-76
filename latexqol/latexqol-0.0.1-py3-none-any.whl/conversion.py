import pyperclip

def copy_table(headers, *args):
    '''
    Creates a formated table based on headers and collumns
    :param headers : array
        names of each collumn
    :param *args : arrays
        collumns with data
    '''

    num_cols = 'c' * len(headers)
    collumns = args
    row_range = range(len(headers))
    col_range = range(len(collumns[0]))

    # Rearange 2D array of collumns
    collumns = [[collumns[row][item] for row in row_range] for item in col_range]
    print(collumns)

    # Initialize table
    table = "\\begin{table}[!htbp]\n"
    table += "\t\centering\n"
    table += "\t\\begin{tabular}{" + f"{num_cols}" + "}\n"

    # Add headers
    table += "\t\t\hline\n"
    table += "\t\t" + ' & '.join(headers) + ' \\\\\n'
    table += "\t\t\hline\n"

    # Add collumns
    for col in col_range:
        table += f"\t\t{collumns[0][col]} "
        for row in range(1, len(collumns[0])):
            table += f"& {collumns[row][col]} "
        table += "\\\\\n"
    table += "\t\t\hline\n"

    # End table
    table += "\t\end{tabular}\n"
    table += "\t\caption{Caption here}\n"
    table += "\t\label{tab:label}\n"
    table += "\end{table}"

    print(table)
    pyperclip.copy(table)