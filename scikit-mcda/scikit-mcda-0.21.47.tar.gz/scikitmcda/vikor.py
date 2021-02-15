from .mcda import MCDA, pd, np, MIN, MAX

class VIKOR(MCDA):
    """
    *Višekriterijumska Optimizacija I Kompromisno Rješenje (VIKOR)*

    References:

    - OPRICOVIC, S. Fuzzy VIKOR with an application to water resources planning. Expert Systems with Apliccations, v. 38, n. 10, p. 12983- 12990, 2011.
    - Opricovic, S. Tzeng, G.-H. (2007). Extended VIKOR method in comparison with outranking methods. European Journal of Operational Research, 178(2): 514-529.
    - OPRICOVIC, S. TZENG, G.. Compromisse solution by MCDM methods: a comparative analysis of VIKOR and TOPSIS. European Journal of Operational Research, v. 16, p. 445-455, 2004.
    - OPRICOVIC, S. TZENG, G.. Multicriteria planning of post-earthquake sustainable reconstruction. Computer-Aided Civil and Infrastructure Engineering, v. 17, p. 211-220, 2002.
    """
    def __init__(self):
        super().__init__()
        self.x_best = []
        self.x_worst = []
        self.df_Si_Ri = []        
        self.S_minmax = (0, 0)
        self.R_minmax = (0, 0)
        self.df_Qi = []        
        self.Conditions = {"C1": True, "C2": True}
        
    def decide(self, v=0.5):  
        """
        Method for decision making using VIKOR. 
        Multi-criteria Optimization AND compromise solution

        :param v: (default=0.5) Where v the weight for the strategy of maximum group utility and 
                  1 - v is the weight of the individual regret. 
                  Usually v = 0.5 and when v > 0.5, the index of Qj will tend to majority agreement 
                  and clearly when v < 0.5, the index of Qj will indicate majority negative attitude.

        :returns: Conditions C1 - Acceptable Advantage and C2 - Accetable Stability in Decision Making
        :rtype: dict
        """   
        self.__calc_X()
        self.__calc_Si_Ri()
        self.__calc_Qi(v)
        self.__vikor()

        return self.Conditions

    def __calc_X(self):
        max_ = list(self.df_original.iloc[:, 1:].max(axis=0)) 
        min_ = list(self.df_original.iloc[:, 1:].min(axis=0))
       
        self.x_best = []
        self.x_worst = []        
    
        i = 0
        for s in self.signals:
            if s > 0:
                self.x_best.append(max_[i])
                self.x_worst.append(min_[i])
            else:
                self.x_best.append(min_[i])
                self.x_worst.append(max_[i])
            i = i + 1

    def __calc_Si_Ri(self):

        self.df_Si_Ri = self.df_original
        
        n_rows, n_cols = self.df_original.shape
        
        Si = 0
        for i in range(n_rows): 
            for j in range(n_cols-1): 
                if (self.x_best[j] - self.x_worst[j]) == 0: # prevent div by zero
                    Si = 0
                else:
                    Si = self.weights[j] * (  (self.x_best[j] - float(self.df_original.iloc[i, j+1]))  / (self.x_best[j] - self.x_worst[j]) )    
                self.df_Si_Ri.iloc[i, j+1] = Si
        
        self.df_Si_Ri["Si"] = self.df_Si_Ri.sum(axis=1) 
        self.df_Si_Ri["Ri"] = self.df_Si_Ri.iloc[:, 1:-1].max(axis=1) 

        self.S_minmax = (self.df_Si_Ri.iloc[:, -2].min(axis=0), self.df_Si_Ri.iloc[:, -2].max(axis=0))
        self.R_minmax = (self.df_Si_Ri.iloc[:, -1].min(axis=0), self.df_Si_Ri.iloc[:, -1].max(axis=0))

    def __calc_Qi(self, v):

        self.df_Qi = self.df_Si_Ri
        
        n_rows, n_cols = self.df_original.shape
        
        Qi = []
        for i in range(n_rows): 
            Qi.append(v * ((self.df_Si_Ri.iloc[i, -2] - self.S_minmax[0])/(self.S_minmax[1] - self.S_minmax[0])) +  ((1-v) * ((self.df_Si_Ri.iloc[i, -1] - self.R_minmax[0])/(self.R_minmax[1] - self.R_minmax[0]))))
        
        self.df_Qi["Qi"] = Qi
        self.df_normalized = self.df_Qi
        self.df_weighted = self.df_Qi

    def __vikor(self):
        i = np.arange(1, len(self.df_original.index)+1, 1)
        df_ranking = pd.DataFrame(self.df_original.iloc[:,0]).join(self.df_Qi.iloc[:,-3:]).sort_values(by=["Qi"], ascending=True)
        df_ranking["rank"] = i
        
        self.df_decision = df_ranking.sort_index()
        self.__check_compromise()

    def __check_compromise(self):
        # Check Conditions C1 and C2
        QA1 = 0
        RA1 = 0
        SA1 = 0
        QA2 = 0
        DQ = 1 / (self.df_original.shape[0] - 1)
        for r in range(self.df_decision.shape[0]):
            if self.df_decision.iloc[r, 4] == 1:
                QA1 =  self.df_decision.iloc[r, 3]
                RA1 =  self.df_decision.iloc[r, 2]
                SA1 =  self.df_decision.iloc[r, 1]
            if self.df_decision.iloc[r, 4] == 2:
                QA2 =  self.df_decision.iloc[r, 3]
                RA2 =  self.df_decision.iloc[r, 2]
                SA2 =  self.df_decision.iloc[r, 1]

        # Check C1 - Acceptable Advantage
        if QA2 - QA1 >= DQ:
            self.Conditions["C1"] = True
        else:
            self.Conditions["C1"] = False
            # Just Q(A^(M)) - Q(A1) < DQ. where max M
            for r in range(self.df_decision.shape[0]):
                if self.df_decision.iloc[r, 3] - QA1 < DQ:
                    self.df_decision.iloc[r, 4] = str(self.df_decision.iloc[r, 4]) + "*"

        # check C2 - Accetable Stability in Decision Making
        # Alterative A1 must also be the best ranked by S or/and R
        S_min = self.df_decision.iloc[:, 1].min()
        R_min = self.df_decision.iloc[:, 2].min()
        if SA1 == S_min or RA1 == R_min:
            self.Conditions["C2"] = True
        else:
            self.Conditions["C2"] = False
            # Just A1 and A2
            for r in range(self.df_decision.shape[0]):
                if self.df_decision.iloc[r, 4] == 1 or self.df_decision.iloc[r, 4] == 2:
                    self.df_decision.iloc[r, 4] = str(self.df_decision.iloc[r, 4]) + "*"