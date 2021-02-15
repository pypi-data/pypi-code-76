from .mcda import MCDA, pd, np

class WPM(MCDA):
    def __init__(self):
        super().__init__()        
    
    def decide(self, normalization_method=None):  
        """
        Method for decision making using WPM. 

        :param normalization_method: (default=None) Must be defined when the problem data is different units,
        :type normalization_method: some value defined in NORMALIZATION_METHODS constant

        :returns: none value
        :rtype: none
        """   
        self._MCDA__set_normalization_method(normalization_method)
        self._MCDA__normalize()
        self._MCDA__weighting_from_normalized()
        self.__wpm()

    def __wpm(self):
        wpm = pd.DataFrame(self.df_weighted.iloc[:, 1:])
        wpm = pd.DataFrame(wpm.prod(axis=1), columns=["WPM"])

        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(wpm).sort_values(by=["WPM"], ascending=False)
        df_ranking["rank"] = i

        self.df_decision = df_ranking.sort_index()

