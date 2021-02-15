from .mcda import MCDA, pd, np, tabulate

class ELECTRE_I(MCDA):
    def __init__(self):
        super().__init__()     
        self.df_concordance_matrix: 0
        self.df_discordance_matrix: 0
        self.df_credibility_matrix: 0
   
    def decide(self, c=1, d=0, normalization_method=None):
        """
        Method for decision making using ELECTRE I. 

        :param c: (optional) concordance index. Default 1 is the strict case  
        :type c: c > 0.5 up to 1

        :param d: (optional) discordance index. Deafault 0 is the strict case  
        :type c: c < 0.5 up to 0

        :param normalization_method: (default=None) Must be defined when the problem data is different units,
        :type normalization_method: some value defined in NORMALIZATION_METHODS constant

        :returns: print
        :rtype: string
        """          
        if self.__check_cd(c, d) is True:
            self._MCDA__set_normalization_method(normalization_method)
            self._MCDA__normalize()
            self.__make_concordance_matrix()
            self.__make_discordance_matrix()
            self.__electre_i(c, d)
            return "electre_i"

    def __make_concordance_matrix(self):
        # define shape of c_matrix
        n_rows = (self.df_normalized.shape[0])
        alternatives = list(self.df_normalized.iloc[:, 0])
        df_concordance_mtx = pd.DataFrame(0, index=np.arange(n_rows), columns=alternatives)
        df_concordance_mtx.insert(loc=0, column='Concordance MTX', value=alternatives)

        W = sum(self.weights)

        for alt in range(n_rows):
            for i in range(n_rows):
                if i != alt:
                    Cab = 0
                    for col in range(1, self.df_normalized.shape[1]):
                        a = self.df_normalized.iloc[alt, col]
                        b = self.df_normalized.iloc[i, col]
                        if a >= b:
                            Cab = Cab + self.weights[col-1]
                        else:
                            Cab = Cab + 0
                    Cab = Cab/W
                    df_concordance_mtx.iloc[alt, i+1] = Cab

        self.df_concordance_matrix = df_concordance_mtx
    
    def __make_discordance_matrix(self):
        # define shape of c_matrix
        n_rows = (self.df_normalized.shape[0])
        alternatives = list(self.df_normalized.iloc[:, 0])
        df_discordance_mtx = pd.DataFrame(0, index=np.arange(n_rows), columns=alternatives)
        df_discordance_mtx.insert(loc=0, column='Discordance MTX', value=alternatives)

        S = list(self.df_normalized.iloc[:, 1:].max(axis=0) - self.df_normalized.iloc[:, 1:].min(axis=0))
      
        for alt in range(n_rows):
            for i in range(n_rows):
                if i != alt:
                    Dab = []
                    count_negatives = 0
                    for col in range(1, self.df_normalized.shape[1]):
                        a = self.df_normalized.iloc[alt, col]
                        b = self.df_normalized.iloc[i, col]
                        d = (b - a)/S[col-1]
                        Dab.append(d)
                        if d < 0:
                            count_negatives = count_negatives + 1
                    if count_negatives == n_rows:
                        Dab = 0
                    else:
                        Dab = max(Dab)
                    df_discordance_mtx.iloc[alt, i+1] = Dab
        
        self.df_discordance_matrix = df_discordance_mtx

    def __electre_i(self, c, d):

        # init credibility matrix
        self.df_credibility_matrix = self.df_concordance_matrix.rename(columns={'Concordance MTX': 'OUTRANKING'})

        n_rows = self.df_normalized.shape[0]
        dominance_relationship = []
        for i in range(n_rows):
            prevalent = 0
            for j in range(n_rows):
                c_cell = self.df_concordance_matrix.iloc[i, j+1]
                d_cell = self.df_discordance_matrix.iloc[i, j+1]
                if i != j:
                    if c_cell >= c and d_cell <= d:
                        self.df_credibility_matrix.iloc[i, j+1] = str(1)
                        prevalent = prevalent + 1     
                    else:
                        self.df_credibility_matrix.iloc[i, j+1] = str(0)
                else:
                    self.df_credibility_matrix.iloc[i, j+1] = "-"
            if prevalent > 0:
                dominance_relationship.append("prevalent")
            else:
                dominance_relationship.append("subdued")

        df_dominance_relationship = pd.DataFrame({"Alternatives": self.df_concordance_matrix.iloc[:, 1:].columns,
                                                  "Outranking": dominance_relationship})

        self.df_decision = df_dominance_relationship

    def __check_cd(self, c, d):
        if c > 0.5 and d < 0.5:
            return True
        else:
            raise ValueError("Wrong concordance (c > 0.5) or discrdance (d < 0.5) indexes")

    def get_graph(self):
        """
        Function returns nodes and edges to draw electre I graph.

        :returns: {"nodes": list of nodes_id, 
                   "edges": list of edges in generic format {"source": node_id ,"target": node_id}, 
                   "edges_networkx": list of edges in networkx format
                   } 
        :rtype: dict
        """
        n_rows = self.df_credibility_matrix.shape[0]
        edges = []
        edges_networkx = []
        nodes = list(self.df_credibility_matrix.iloc[:, 0])
        for a in range(n_rows):
            for b in range(n_rows):
                if self.df_credibility_matrix.iloc[a, b+1] == "1":
                    edges.append({"source": self.df_credibility_matrix.iloc[a, 0],"target": self.df_credibility_matrix.columns[b+1]})
                    edges_networkx.append((self.df_credibility_matrix.iloc[a, 0],self.df_credibility_matrix.columns[b+1]))
        
        return {"nodes": nodes, "edges": edges, "edges_networkx": edges_networkx}

    def pretty_concordance_matrix(self, tablefmt='psql'):
        """
        Print a pretty table about specific attribute.

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """        
        return tabulate(self.df_concordance_matrix, headers='keys', tablefmt=tablefmt)
            
    def pretty_discordance_matrix(self, tablefmt='psql'):
        """
        Print a pretty table about specific attribute.

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """        
        return tabulate(self.df_discordance_matrix, headers='keys', tablefmt=tablefmt)

    def pretty_credibility_matrix(self, tablefmt='psql'):
        """
        Print a pretty table about specific attribute.

        :param tablefmt: (default=psql) format of output 
        :type: string constant: 'html', 'latex' or 'psql'

        :returns: print
        :rtype: string

        """        
        return tabulate(self.df_credibility_matrix, headers='keys', tablefmt=tablefmt)
