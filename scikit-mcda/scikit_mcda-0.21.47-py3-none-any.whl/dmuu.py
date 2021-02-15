'''
#########################################################
# SCI-KIT-MCDA Library                                  #
# Author: Antonio Horta                                 #
# https://gitlab.com/cybercrafter/scikit-mcda           #
# Cybercrafter ® 2021                                   #
#########################################################
'''

import pandas as pd
import copy
from tabulate import tabulate

class DMUU:
    """
    Class: DMUU: Decision making under uncertainty
    """
    def __init__(self):
        self.df_original = 0
        self.df_calc = 0
        self.decision = []

    def dataframe(self, alt_data, alt_labels=None, state_labels=None):

        # define state labels if not exists
        if state_labels is None:
            state_labels = []
            for s in range(1, len(alt_data[0])+1):
                state_labels.append("S" + str(s))

        # define alternative labels if not exists
        if alt_labels is None:
            alt_labels = []
            for a in range(1, len(alt_data)+1):
                alt_labels.append("A" + str(a))

        df_data = pd.DataFrame(data=alt_data, columns=state_labels)
        df_data.insert(loc=0,
                    column='alternatives',
                    value=alt_labels)
        dfo = df_data

        self.df_original = copy.copy(dfo)
        self.df_calc = copy.copy(dfo)
        self.decision = []

    def minimax_regret(self):
        self.__calc("minimax-regret")
        self.decision_making("minimax-regret")
        return "minimax-regret"

    def maximax(self):
        self.__calc("maximax")
        self.decision_making("maximax")
        return "maximax"

    def maximin(self):
        self.__calc("maximin")
        self.decision_making("maximin")
        return "maximin"

    def laplace(self):
        self.__calc("laplace")
        self.decision_making("laplace")
        return "laplace"

    def hurwicz(self, hurwicz_coeficient=-1):
        self.__calc("hurwicz", hurwicz_coeficient)
        self.decision_making("hurwicz")
        return "hurwicz"

    def calc_clean(self):
        self.df_calc = copy.copy(self.df_original)
        return True

    '''
    FUNCTION:
    decision_making(dmuu_df, dmuu_criteria_list=[], hurwicz_coeficient=0.5):

    DESCRIPTION:
    Function that returns solutions DMUU from dmuu_dataframe or dmcu_dataframe_calculated of criteria listed in dmuu_criteria_list

    PARAMS:
    dmuu_df: dataframe with alteratives and states
    dmuu_criteria_list: list of criteria ["maximax", "maximin", "laplace", "minimax-regret", "hurwicz"]

    OUTPUT:
            list of dict         {"alternative": ,
                                "index": ,
                                "value": ,
                                "criteria":,
                                "result": [{"alternative": value}],
                                "type_dm": "DMUU",
                                'hurwicz_coeficient':
                                }
    '''

    def decision_making(self, dmuu_criteria_list=[]):

        # check dmuu_criteria_list
        dmuu_criteria_list = self.__check_dmuu_criteria_list(dmuu_criteria_list)

        result = []

        # make result
        for l in dmuu_criteria_list:
            cols = list(self.df_calc[l])
            for c in cols:
                if c[1] == 1:
                    hc = ""
                    if l in "hurwicz":
                        hc = c[2]
                    result.append({"alternative": self.df_calc.iloc[cols.index(c), 0],
                                "index": cols.index(c),
                                "value": c[0],
                                "criteria": l,
                                "result": dict(zip(self.df_calc["alternatives"], [i[0] for i in cols])),
                                "type_dm": "DMUU",
                                "hurwicz_coeficient": hc
                                })
        
        self.decision = result


    def __calc(self, dmuu_criteria_list=[], hurwicz_coeficient=-1):

        df = self.df_calc

        if "minimax-regret" in dmuu_criteria_list:
            list_minimax_regret_max = self.df_original.iloc[:, 1:].max(axis=0)
            df_minimax_regret_temp = self.df_original.iloc[:, 1:] - list_minimax_regret_max
            # now apply maximin
            df_maximin_r = df_minimax_regret_temp.min(axis=1)
            result_maximin_r = df_maximin_r.max(axis=0)
            column_maximin_r = []
            for x in df_maximin_r.values:
                if x == result_maximin_r:
                    column_maximin_r.append((x * -1, 1))
                else:
                    column_maximin_r.append((x * -1, 0))
            df['minimax-regret'] = column_maximin_r

        if "maximax" in dmuu_criteria_list:
            df_maximax = self.df_original.iloc[:, 1:].max(axis=1)
            result_maximax = df_maximax.max(axis=0)
            column_maximax = []
            for x in df_maximax.values:
                if x == result_maximax:
                    column_maximax.append((x, 1))
                else:
                    column_maximax.append((x, 0))
            df['maximax'] = column_maximax

        if "maximin" in dmuu_criteria_list:
            df_maximin = self.df_original.iloc[:, 1:].min(axis=1)
            result_maximin = df_maximin.max(axis=0)
            column_maximin = []
            for x in df_maximin.values:
                if x == result_maximin:
                    column_maximin.append((x, 1))
                else:
                    column_maximin.append((x, 0))
            df['maximin'] = column_maximin

        if "laplace" in dmuu_criteria_list:
            df_laplace = self.df_original.iloc[:, 1:].mean(axis=1)
            result_laplace = df_laplace.max(axis=0)
            column_laplace = []
            for x in df_laplace.values:
                if x == result_laplace:
                    column_laplace.append((x, 1))
                else:
                    column_laplace.append((x, 0))
            df['laplace'] = column_laplace

        if "hurwicz" in dmuu_criteria_list:

            # check hurwicz_coeficient is ok. if not default is 0.5
            if self.__check_hurwicz_coeficient(hurwicz_coeficient) is False:
                hurwicz_coeficient = 0.5

            df_hurwicz = self.df_original.iloc[:, 1:].max(axis=1) * hurwicz_coeficient + self.df_original.iloc[:, 1:].min(axis=1) * (1 - hurwicz_coeficient)
            result_hurwicz = df_hurwicz.max(axis=0)
            column_hurwicz = []
            for x in df_hurwicz.values:
                if x == result_hurwicz:
                    column_hurwicz.append((x, 1, hurwicz_coeficient))
                else:
                    column_hurwicz.append((x, 0, hurwicz_coeficient))
            df['hurwicz'] = column_hurwicz

        self.df_calc = df


    '''
    FUNCTION:
    check_hurwicz_coeficient(hurwicz_coeficient):

    DESCRIPTION:
    Check if hurwicz_coeficient is >= 0 and <= 1
    If not, put default 0.5

    OUTPUT:
        True or False
    '''


    def __check_hurwicz_coeficient(self, hurwicz_coeficient):
        result = True
        if type(hurwicz_coeficient) != float:
            if hurwicz_coeficient < 0 or hurwicz_coeficient > 1:
                result = False
        return result


    '''
    FUNCTION:
    check_dmuu_criteria_list(dmuu_criteria_list=[]):

    DESCRIPTION:
    Check and transform if dmuu_criteria_list is a list of correct dmuu criteria
    and defines default criteria for DMUU

    OUTPUT:
        dmuu_criteria_list transformed or default
    '''


    def __check_dmuu_criteria_list(self, dmuu_criteria_list=[]):

        # defines default criteria for DMUU
        default_list = ["maximax", "maximin", "laplace", "minimax-regret", "hurwicz"]

        if type(dmuu_criteria_list) != list:
            dmuu_criteria_list = [dmuu_criteria_list]

        for c in dmuu_criteria_list:
            if c not in default_list:
                dmuu_criteria_list.remove(c)

        if dmuu_criteria_list == []:
            dmuu_criteria_list = default_list

        return dmuu_criteria_list

    def pretty_decision(self, tablefmt='psql'):
        return tabulate(self.decision, headers='keys', tablefmt=tablefmt)

    def pretty_calc(self, tablefmt='psql'):
        return tabulate(self.df_calc, headers='keys', tablefmt=tablefmt)

    def pretty_original(self, tablefmt='psql'):
        return tabulate(self.df_original, headers='keys', tablefmt=tablefmt)
