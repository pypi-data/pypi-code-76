import pandas as pd
import sys


class System:
    """ A tiny version of the System class only to find the algo for the best solution... """

    def __init__(self, df, name):
        self.name = name
        self.df = df

        self.score = df.loc[df.index[1], 'sys_score']
        #self.wholeness = df.loc[df.index[1], 'sys_wholeness'] # not used here...
        self.elements = df["hit_pos"].to_list()

    def __str__(self):
        return f'Sys_ID={self.name}, hit={self.elements[0]} - {self.elements[-1]} Score={self.score}'

    def get_score(self):
        return self.score


class Solution:
    """ A class that holds systems that are part of a solution,
    and keeps track of its validity (no overlaps between systems) and score """
    # The score of a solution is defined as the sum of the scores of the systems it is made of

    def __init__(self, systems = []):
        self.score = 0
        # Lists components from all systems part of an instance
        self.components = []

        if systems != None:
            self.systems = systems
            for s in systems:
                for el in s.elements:
                    "el = hit_pos"
                    self.components.append(el)
                self.score += s.get_score()
        else:
            self.systems = []


    def __add__(self, system):
         new_systems = self.systems + [system]
         return Solution(new_systems)

    def __str__(self):
        out = 'Score of the solution = {0}\n'.format(self.score)
        for s in self.systems:
            out += '{0}\n'.format(s)

        return out

    def is_compatible(self, system):
        """ Defines whether or not system, an instance of System() is compatible, that is, does not share components with the sytems that are part of the solution. """

        for el1 in self.components:
            for el2 in system.elements:
                if el1 == el2:
                    return False
        return True

    def get_score(self):
        return self.score


def compute_max_bound(systems):
    """ Computes a grand estimation of the maximal score to be found using the set of System() systems as ground for a solution """
    # This grand estimation is the sum of the scores of the systems.
    bound = 0
    for s in systems:
        bound += s.get_score()
    return bound


def find_best_sol_bba(sorted_systems, best_sol, cur_sol):
    """ Function to perform a branch-and-bound type of search for the best solution """
    # A solution is a combination of systems with non-overlapping components, that is, compatible systems
    # The best solution is the one with the best score.

    # Ways to speed up the search:
    # - start to enumerate and evaluate the solutions, starting from the best systems by decreasing score order:
    # - find at once the max_bound of the systems left to explore, and compare to the current max score. if max_bound <= max_score => don't explore the list of systems anymore.
    # - remove/don't explore solutions with uncompatible systems (that is, systems that share components already part of systems in the current solution)
    #print("##################### find_best_sol_bba ###################")
    if len(sorted_systems) == 0:
        return best_sol

    max_bound = compute_max_bound(sorted_systems)
    #print("### max_bound", max_bound)
    if (max_bound + cur_sol.get_score()) < best_sol.get_score():
        # Not worth to explore the rest, impossible to find a better solution than the current best one.
        return best_sol
    #print(f"### cur_sol.is_compatible({sorted_systems[0].name}): ", cur_sol.is_compatible(sorted_systems[0]))
    if cur_sol.is_compatible(sorted_systems[0]):
        # We include the current best system that is compatible and continue the exploration of a solution with this system
        cur_sol += sorted_systems[0]
        if cur_sol.get_score() > best_sol.get_score():
            #print("-- BEST SOLUTION SO FAR --")
            best_sol = cur_sol
            # PB! is here? deepcopying does not change a thing... should this be overloaded in System() class?
            #best_sol = copy.deepcopy(cur_sol)
            #print(best_sol)
        return find_best_sol_bba(sorted_systems[1:], best_sol, cur_sol)

    # We now attempt a solution without the current best system to explore other combinations of systems
    return find_best_sol_bba(sorted_systems[1:], best_sol, cur_sol)


def main_find_sol_bba():
    """ Computes the best solution as the combination of systems which scores' sum is maximized """
    # For implementation purpose, this works for now from a file of the type "all_systems.tsv" which contains all possible valid systems
    input = sys.argv[1]

    # The file containing systems from which to build the solution is read, and extracted as a table
    df = pd.read_csv(input, comment='#', sep='\t')

    # A solution has to be computed for each replicon.
    # Group values by replicon
    grouped = df.groupby('replicon')
    for replicon, df_replic in grouped:
        print("----------REPLICON {0} ----------".format(replicon))

        # Group values by system ID
        # PB! the following issues a warning...
        df_replic.sort_values(by=["sys_score","sys_id"], ascending = False, inplace = True)
        grouped_sysid = df_replic.groupby('sys_id', sort = False)

        # List the systems to work with. It must be sorted by score to speed up the search of the best solution.
        systems = []
        for name, group in grouped_sysid:
            sysobj = System(group, name)
            # Print all sorted systems
            #print(sysobj)
            systems.append(sysobj)

        # Initialization
        best_solution = Solution()
        cur_solution = Solution()

        # Branch-and-bound search:
        #print([(s.name, s.get_score()) for s in systems])
        best_solution = find_best_sol_bba(systems, best_solution, cur_solution)

        print("------ Best Solution ------")
        # PB! this does not work... best_solution is not properly saved when passed as a parameter to the above search function
        print(best_solution)


main_find_sol_bba()
