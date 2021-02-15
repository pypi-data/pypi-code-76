from .mcda import MCDA, pd, np, LinearMinMax_

class PROMETHEE_II(MCDA):
    def __init__(self):
        self.df_dif_pref = 0        
        self.df_apf = 0        
        self.df_flows = 0        
        super().__init__()
    
    def decide(self, normalization_method=LinearMinMax_):
        """
        Method for decision making using PROMETHEE_II. 

        :param normalization_method: (default=LinearMinMax_) Must be defined when the problem data is different units,
        :type normalization_method: some value defined in NORMALIZATION_METHODS constant

        :returns: none value
        :rtype: none
        """         
        self._MCDA__set_normalization_method(normalization_method)
        self._MCDA__normalize()
        self.__dif_pref()
        self.__flows()
        self.__promethee_ii()

    def __flows(self):
        df_temp = pd.DataFrame({"alternatives":  list(self.df_original.iloc[:, 0]),
                                "Leaving Flow φ+":  list(self.df_apf.iloc[:, 1:].sum(axis=1)/(self.df_apf.shape[0]-1)),
                                "Flow φ-": list(self.df_apf.iloc[:, 1:].sum(axis=0)/(self.df_apf.shape[0]-1))
                                })
        
        df_temp["Net Flow φ"] = df_temp.iloc[:, 1] - df_temp.iloc[:, 2] 
        self.df_flows = df_temp

    
        
    def __dif_pref(self):
    
        # define shape of dif table
        n_rows = (self.df_normalized.shape[0]-1)*(self.df_normalized.shape[1]-1)
        df_temp = pd.DataFrame(0, index=np.arange(n_rows), columns=self.df_normalized.iloc[:, 1:].columns.values)
    
        labels = [None] * n_rows
    
        for c in range(1, self.df_normalized.shape[1]):
            r = 0
            for i in range(self.df_normalized.shape[0]):
                for j in range(self.df_normalized.shape[0]):            
                    if i != j: 
                        dif = self.df_normalized.iloc[i,c] - self.df_normalized.iloc[j,c]
                        if dif < 0:
                            dif = 0
                        df_temp.iloc[r,c-1] = dif * self.weights[c-1]
                        labels[r] = "(M" + str(i+1) + " x M" + str(j+1) + ")"
                        r = r + 1
                        if r >= n_rows:
                            r = 0

        # Aggregating Perform Function
        df_temp["APF"] = df_temp.iloc[:, 0:].sum(axis=1) / sum(self.weights) 
         
        alternatives = list(self.df_original.iloc[:, 0])

        df_apf = pd.DataFrame(0, index=np.arange(len(alternatives)), columns=alternatives)

        n_colsrows = self.df_original.shape[0]
        x = 0
        for i in range(0, n_colsrows):
            for j in range(0, n_colsrows):            
                if i != j:
                    df_apf.iloc[i, j] = df_temp.iloc[x, -1]
                    x = x + 1
                    
        self.df_dif_pref = pd.DataFrame(labels, columns=["CRITERIA"]).join(df_temp)
        self.df_weighted = self.df_dif_pref
        self.df_apf = pd.DataFrame(alternatives, columns=["APF"]).join(df_apf)


    def __promethee_ii(self):
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = self.df_flows.sort_values(by=["Net Flow φ"], ascending=False)
        df_ranking["rank"] = i
        
        self.df_decision = df_ranking.sort_index()