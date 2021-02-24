#!/usr/bin/python3
import sys, getopt
from .tools import edge_3_labelling,powerset
from .problem import Problem
from .file_help import store
from .problem_set import Problem_set
import time
from tqdm import tqdm

def generate(white_degree, black_degree):
    white_configurations, black_configurations = edge_3_labelling(white_degree),edge_3_labelling(black_degree)
    white_constraints, black_constraints = powerset(white_configurations),powerset(black_configurations)
    problems_tuple = set([(frozenset(a),frozenset(b)) for a in white_constraints for b in black_constraints])
    problems = set([Problem(a,b,white_degree,black_degree) for (a,b) in problems_tuple if Problem(a,b,white_degree,black_degree).is_characteristic_problem()])
    number_of_problems = len(problems)
    problems_list = list(problems)

    print("Computing relaxations and restrictions ...")

    def process_problem(elem):
        relaxations,restrictions = set(),set()
        equivalent_set = elem.equivalent_problems_instance()
        for other in problems:
            for x in equivalent_set:
                if elem != other :
                    if x.is_restriction(other):
                        relaxations.add(other)
                    if x.is_relaxation(other):
                        restrictions.add(other)
        return (relaxations,restrictions)

    t0= time.time()

    relaxations_dict, restrictions_dict = dict(),dict()

    for problem in tqdm(problems):
        a,b = process_problem(problem)
        relaxations_dict[problem] = a
        restrictions_dict[problem] = b

    print(time.time()-t0)

    return (set(problems),relaxations_dict,restrictions_dict)
