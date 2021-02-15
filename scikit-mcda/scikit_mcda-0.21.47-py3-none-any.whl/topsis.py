from .mcda import MCDA, pd, np, Vector_, tabulate

class TOPSIS(MCDA):
    def __init__(self):
        self.df_pis = []
        self.df_nis = []
        self.df_closeness = 0
        super().__init__()        
    
    def decide(self, normalization_method=Vector_):        
        """
        Method for decision making using TOPSIS. 

        :param normalization_method: (default=Vector_) Must be defined when the problem data is different units,
        :type normalization_method: some value defined in NORMALIZATION_METHODS constant

        :returns: none value
        :rtype: none
        """   
        self._MCDA__set_normalization_method(normalization_method)      
        self._MCDA__normalize(True)
        self._MCDA__weighting_from_normalized()
        self.__xis()
        self.__topsis()
         
    def __xis(self):
        pis = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals).max(axis=0) * self.signals
        self.df_pis = pis
        nis = pd.DataFrame(self.df_weighted.iloc[:, 1:] * self.signals).min(axis=0) * self.signals
        self.df_nis = nis

    def __topsis(self):
        dp = np.sqrt(self.df_weighted.iloc[:, 1:].sub(self.df_pis).pow(2).sum(axis=1))
        dn = np.sqrt(self.df_weighted.iloc[:, 1:].sub(self.df_nis).pow(2).sum(axis=1))
        closeness = pd.DataFrame(dn.div(dp+dn), columns=["performance score"])
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(closeness).sort_values(by=["performance score"], ascending=False)
        df_ranking["rank"] = i

        self.df_decision = df_ranking.sort_index()

    def pretty_Xis(self, tablefmt='psql'):
        """
        Print a pretty table about positive and negative ideal solutions attributes (df_pis and df_nis).

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """        
        return tabulate(pd.DataFrame(self.df_pis, columns=['PIS']).join(pd.DataFrame(self.df_nis, columns=["NIS"])).T, headers='keys', tablefmt=tablefmt)
