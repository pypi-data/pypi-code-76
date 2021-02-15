from .mcda import MCDA, pd, np
from .topsis import TOPSIS
from .wpm import WPM
from .wsm import WSM
from .vikor import VIKOR
from .promethee_ii import PROMETHEE_II
from .electre_ii import ELECTRE_II
from .waspas import WASPAS


class ENSEMBLE(MCDA):
    """
    The concept of ensemble class came from machine learning methods to combine the predictions 
    of several base estimators built with a given learning algorithm in order to improve generalizability
    or robustness over a single estimator.
    """
    def __init__(self):
        super().__init__()        
        self.df_decision: 0
    
    def ranking_by_voting(self, list_mcda_intances, voting='soft'):  
        """
        The idea behind the ranking_by_voting Method is to combine conceptually different MCDA Raking Methods and 
        use a majority vote (hard vote) or the average of preferences normalized (soft vote) to estabilish a ranking. 
        
        It can be useful for a set of equally well performing model in order to balance out their individual weaknesses.

        In majority voting, the priority/rank achieved for a particular alternative is the priority/rank 
        that represents the majority (mode) achieved by each individual MCDA method.

        E.g., if the rank for a given problem is

                            PROMETHEE II  TOPSIS   WSM   WPM    Majority
        Alternative 1 ->              1º      2º     2º   2º          2º
        Alternative 2 ->              3º      3º     1º   3º          3º
        Alternative 3 ->              2º      1º     3º   1º          1º
        
        the ranking_by_voting (with 'hard') would rank the problem as “A1: 2º, A2: 3º and A3: 1º” based on the majority.

        In the cases of a tie, the ranking_by_voting will set "a tie" as result.      

        The hard method allows duplicated priority
      
        :param list_mcda_intances: (default=None) Must be defined when the problem data is different units,
        :type list_mcda_intances: some value defined in NORMALIZATION_METHODS constant

        :param voting: (default='soft') type of voting 'hard' or 'soft'
        :type voting: string 'hard' or 'soft'

        :returns: none value
        :rtype: none
        """   
        if self.__check_mcda_method(list_mcda_intances) is True:
            if self.__check_voting_method(voting) == 'soft':
                self.__soft_voting(list_mcda_intances)
                self.__verdict()
            else:
                self.__hard_voting(list_mcda_intances)
        
            return self.df_decision

    def __check_voting_method(self, voting):
        if voting in ["hard", "soft"]:
            return voting
        else:
            return "soft"

    def __check_mcda_method(self, list_mcda_intances):
        for mcdm in list_mcda_intances:
            if type(mcdm) not in [TOPSIS, PROMETHEE_II, WASPAS, WSM, WPM, VIKOR, ELECTRE_II]:
              raise ValueError("list_mcda_intances must be a list of instances of MCDA RANKING methods (TOPSIS, PROMETHEE_II, WASPAS, WSM, WPM, VIKOR, ELECTRE_II)")        
        return True

    def __verdict(self):
        i = np.arange(1, len(self.df_decision.index)+1, 1)
        df_ranking = self.df_decision.sort_values(by=["voting"], ascending=False)
        df_ranking["rank"] = i
        self.df_decision = df_ranking.sort_index()


    def __norm(self, df):
        normalized = df.iloc[:, 1:]/df.iloc[:, 1:].sum(axis=0)
        self.df_normalized = normalized

    def __soft_voting(self, list_mcda_intances):
        df_soft = pd.DataFrame(np.zeros((list_mcda_intances[0].df_decision.shape[0], len(list_mcda_intances))))
        column = 0
        for m in list_mcda_intances:
            if type(m) == VIKOR: 
                df_soft[column] = 1 - m.df_decision.iloc[:, -2] # VIKOR need to be inverted for sort correctly            
            else:
                df_soft[column] = m.df_decision.iloc[:, -2]
            df_soft = df_soft.rename(columns={column: type(m).__name__})
            column = column + 1

        # normalizing
        # self.__norm(df_soft)
        # df_soft = self.df_normalized
        # df_soft["voting"] = self.df_normalized.iloc[:,:].mean(axis=1)
        df_soft["voting"] = df_soft.iloc[:,:].mean(axis=1)

        df_soft = pd.DataFrame(list_mcda_intances[0].df_decision.iloc[:, 0]).join(df_soft)
        
        self.df_decision = df_soft

    def __hard_voting(self, list_mcda_intances):
        df_hard = pd.DataFrame(np.zeros((list_mcda_intances[0].df_decision.shape[0], len(list_mcda_intances))))
        column = 0
        for m in list_mcda_intances:
            if type(m) == VIKOR: # filter * in VIKOR compromise conditions
                vikor_list = str(m.df_decision.iloc[:, -1].values).replace("*", "").replace("[", "").replace("]", "").replace("'", "").replace(" ", "")
                vikor_list = np.array(list(vikor_list), dtype=int)
                df_hard[column] = vikor_list
            else:
                df_hard[column] = m.df_decision.iloc[:, -1]
            df_hard = df_hard.rename(columns={column: type(m).__name__})
            column = column + 1

        # Get a tie
        a_tie = df_hard.iloc[:,:].agg(lambda x: "a tie" if x.value_counts().values[0] in x.value_counts().values[1:] else x.value_counts().values[0] , axis=1).values.tolist()

        df_hard["std"] = df_hard.iloc[:,:].std(axis=1)
        df_hard["voting"] = df_hard.iloc[:,:].agg(lambda x: x.value_counts().index[0], axis=1)
        df_hard["rank"] = df_hard.iloc[:,:].agg(lambda x: x.value_counts().index[0], axis=1)


        # set a tie when entropy = 1
        for x in range(0, df_hard.shape[0]):
            elements = []
            for y in range(0, df_hard.shape[1]-3):
                if float(df_hard.iloc[x,y]) not in elements: 
                    elements.append(df_hard.iloc[x,y])
                    if (df_hard.shape[1]-3) == len(elements):
                        df_hard.iloc[x, -2] = "a tie"
                        df_hard.iloc[x, -1] = "a tie"
        # Set a tie
        for t in a_tie:
            if t == "a tie":
                df_hard.iloc[a_tie.index(t), -2] = "a tie"
                df_hard.iloc[a_tie.index(t), -1] = "a tie"

        df_hard = pd.DataFrame(list_mcda_intances[0].df_decision.iloc[:, 0]).join(df_hard)
        
        self.df_decision = df_hard
