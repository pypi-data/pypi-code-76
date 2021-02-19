def compute_max_bound(solution, systems):
    return sum([s.score for s in systems if solution.is_compatible(s)])


def solution_explorer():

    visited = set()

    def find_best_solution(sorted_systems, best_sol, cur_sol):
        if not sorted_systems:
            return best_sol

        # It's IMPORTANT to do a copy of sorted_systems
        # otherwise (for instance using pop to get the first element)
        # the side effect will empty the sorted_systems even outside the function :-(
        system_to_test = sorted_systems[0]
        remaining_syst = sorted_systems[1:]
        if not cur_sol.systems:
            if system_to_test in visited:
                return best_sol
            else:
                visited.add(system_to_test)
        max_bound = compute_max_bound(cur_sol, sorted_systems)
        if max_bound + cur_sol.score < best_sol.score:
            return best_sol

        if cur_sol.is_compatible(system_to_test):
            cur_sol += system_to_test
            if cur_sol.score > best_sol.score:
                best_sol = cur_sol
            return find_best_solution(remaining_syst, best_sol, cur_sol)
        else:
            is_the_best = find_best_solution(sorted_systems, best_sol, Solution([]))
            if is_the_best.score > best_sol.score:
                best_sol = is_the_best
            return find_best_solution(remaining_syst, best_sol, cur_sol)

    return find_best_solution


def find_best_solutions(systems):
    G = nx.Graph()
    # add nodes (vertices)
    G.add_nodes_from(systems)
    # let's create an edges between compatible nodes
    for sys_i, sys_j in itertools.combinations(systems, 2):
        if sys_i.is_compatible(sys_j):
            G.add_edge(sys_i, sys_j)

    cliques = nx.algorithms.clique.find_cliques(G)
    max_score = 0
    max_cliques = []
    for c in cliques:
        current_score = sum([s.score for s in c])
        if current_score > max_score:
            max_score = current_score
            max_cliques = [c]
        elif current_score == max_score:
            max_cliques.append(c)
    return max_cliques, max_score


def find_best_solution(systems):
    scores = [s.score for s in systems]
    ranks = range(len(systems))
    # create a new Model
    m = mip.Model("")
    if _log.getEffectiveLevel() > 10:
        m.verbose = 0
    # let's create variable which can take 0/1 for each system
    # and add them to the model
    x = [m.add_var(var_type=mip.BINARY) for i in ranks]

    # add constraints
    for i, j in itertools.combinations(ranks, 2):
        if not systems[i].is_compatible(systems[j]):
            m += x[i] + x[j] <= 1, f'{systems[i].id} and {systems[j].id} are not compatible'

    # We want to optimize the scores
    m.objective = mip.maximize(mip.xsum(x[i] * scores[i] for i in ranks))

    status = m.optimize()

    if status == mip.OptimizationStatus.OPTIMAL:
        _log.debug('optimal solution cost {} found'.format(m.objective_value))
        best_ranks = [i for i, v in enumerate(m.vars) if abs(v.x) > 1e-6]
        best_sol = [systems[i] for i in best_ranks]
    else:
        raise MacsypyError("No optimal solution")
    return best_sol, m.objective_value