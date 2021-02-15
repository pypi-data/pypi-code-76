from .electre_i import ELECTRE_I, np, pd

class ELECTRE_II(ELECTRE_I):
    def __init__(self):
        super().__init__()     
        self.pure_concordance: 0
        self.pure_discordance: 0
   
    def decide(self, c=1, d=0, normalization_method=None):
        """
        Method for decision making using ELECTRE II. It results in a ranking of alternatives 
        by median of pure concordance x pure discordance rankings

        :param c: (optional) concordance index. Default 1 is the strict case  
        :type c: c > 0.5 up to 1

        :param d: (optional) discordance index. Deafault 0 is the strict case  
        :type c: c < 0.5 up to 0

        :param normalization_method: (default=None) Must be defined when the problem data is different units,
        :type normalization_method: some value defined in NORMALIZATION_METHODS constant

        :returns: print
        :rtype: string
        """          
        if self._ELECTRE_I__check_cd(c, d) is True:
            self._MCDA__set_normalization_method(normalization_method)
            self._MCDA__normalize()
            self._ELECTRE_I__make_concordance_matrix()
            self._ELECTRE_I__make_discordance_matrix()
            self._ELECTRE_I__electre_i(c, d)
            self.__electre_ii()
            return "electre_ii"

    def __electre_ii(self):
        self.__calc_pure_concordance()
        self.__calc_pure_discordance()
        self.__median()
        
    def __calc_pure_concordance(self):
    
        sum_row = np.array(self.df_concordance_matrix.iloc[:, 1:].sum(axis=1).to_list())
        sum_col = np.array(self.df_concordance_matrix.iloc[:, 1:].sum(axis=0).to_list())
        self.pure_concordance = pd.DataFrame(sum_row - sum_col, columns=["pure concordance"])
        
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(self.pure_concordance).sort_values(by=["pure concordance"], ascending=False)
        df_ranking["rank concordance"] = i

        self.pure_concordance = df_ranking.sort_index()
        
    def __calc_pure_discordance(self):
        
        sum_row = np.array(self.df_discordance_matrix.iloc[:, 1:].sum(axis=1).to_list())
        sum_col = np.array(self.df_discordance_matrix.iloc[:, 1:].sum(axis=0).to_list())
        self.pure_discordance = pd.DataFrame(sum_row - sum_col, columns=["pure discordance"])
    
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(self.pure_discordance).sort_values(by=["pure discordance"], ascending=True)
        df_ranking["rank discordance"] = i

        self.pure_discordance = df_ranking.sort_index()

    def __median(self):
        ranks = self.pure_concordance.join(self.pure_discordance.iloc[:,-1])
        median = 1 - (pd.DataFrame(ranks.iloc[:,-2:].median(axis=1), columns=["median scaled inverted"]) / ranks.iloc[:,-2:].median(axis=1).sum(axis=0))
        final_rank = pd.DataFrame(ranks.iloc[:,-2:].median(axis=1), columns=["rank"])
        self.df_decision = self.pure_concordance.join(self.pure_discordance.iloc[:,1:]).join(median).join(final_rank)
