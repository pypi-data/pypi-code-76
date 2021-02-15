from .mcda import MCDA, pd, np

class WSM(MCDA):
    def __init__(self):
        super().__init__()        
    
    def decide(self, normalization_method=None):  
        """
        Method for decision making using WSM/SAW. 

        :param normalization_method: (default=None) Must be defined when the problem data is different units,
        :type normalization_method: some value defined in NORMALIZATION_METHODS constant

        :returns: none value
        :rtype: none
        """   
        self._MCDA__set_normalization_method(normalization_method)
        self._MCDA__normalize()
        self._MCDA__weighting_from_normalized()
        self.__wsm()

    def __wsm(self):
        wsm = pd.DataFrame(self.df_weighted.iloc[:, 1:])
        wsm = pd.DataFrame(wsm.sum(axis=1), columns=["WSM"])

        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(wsm).sort_values(by=["WSM"], ascending=False)
        df_ranking["rank"] = i

        self.df_decision = df_ranking.sort_index()

