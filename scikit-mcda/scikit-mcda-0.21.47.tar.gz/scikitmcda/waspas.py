from .mcda import MCDA, pd, np

class WASPAS(MCDA):
    def __init__(self):
        super().__init__()        
    
    def decide(self, lambda_=0.5, normalization_method=None):
        """
        Method for decision making using WASPAS. 

        :param lambda_: (default=0.5) Must be defined for tunning purpose,
        :type lambda_: float

        :param normalization_method: (default=None) Must be defined when the problem data is different units,
        :type normalization_method: some value defined in NORMALIZATION_METHODS constant

        :returns: none value
        :rtype: none
        """   
        if self.__check_lambda(lambda_) is True:
            self._MCDA__set_normalization_method(normalization_method)
            self._MCDA__normalize()
            self._MCDA__weighting_from_normalized()
            self.__waspas(lambda_)

    def __waspas(self, lambda_):
        w_df = pd.DataFrame(self.df_weighted.iloc[:, 1:])       
       
        q_wsm = pd.DataFrame(w_df.sum(axis=1), columns=["WSM"]) * lambda_
        q_wpm = pd.DataFrame(w_df.prod(axis=1), columns=["WPM"]) * (1 - lambda_) 

        waspas = q_wsm.iloc[:,0] + q_wpm.iloc[:,0]
        label = "WASPAS (λ " + str(lambda_) + " )" 
        waspas_df = pd.DataFrame(waspas, columns=[label]) 

        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(waspas_df).sort_values(by=[label], ascending=False)
        df_ranking["rank"] = i

        self.df_decision = df_ranking.sort_index()

    def __check_lambda(self, lambda_):
        result = False
        if type(lambda_) == float:
            if (lambda_ >= 0 and lambda_ <= 1):
                result = True
            else:
                raise ValueError("Lambda must be a value between 0 and 1!")                
        return result