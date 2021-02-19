import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def data_preprocessing(url):
    primary= pd.read_csv(url)
    primary["resolution1_name"].fillna(1,inplace=True)
    primary["Month"] = primary["Import_Time"].apply(month)

    primary["ResolutionType"] = primary["resolution1_name"].apply(resolution)

    primary_rules = primary[((primary["resolution1_name"] == "Chargeback Received - Fraud") | (primary["resolution1_name"] == "Buyer Fraud  Loss") |  (primary["resolution1_name"] == 1) |
                         (primary["resolution1_name"] == "Buyer Fraud Prevented") | (primary["resolution1_name"] == "Cancelled - non fraud") | (primary["resolution1_name"] == "Chargeback Received - Fraud") |
                         (primary["resolution1_name"] == "Chargeback Received - Dispute") |  (primary["resolution1_name"] == "Fraud Reviewed  Allowed"))]


    rule_map = pd.read_excel("rule_servant_pizzani/rules.xlsx",index_col=0)
    rule_mapping = rule_map.to_dict()
#rules= "5237260000001273434,5237260000001273454,5237260000001284293,5237260000001265373,5237260000001273337,5237260000001291513,5237260000001291533,5237260000001297293,5237260000001297494,5237260000001297513,5237260000001303254,5237260000001310733,5237260000001312153,5237260000001313913,5237260000001314653,5237260000001314654,5237260000001314655,5237260000001315973,5237260000001315994,5237260000001316014,5237260000001316733,5237260000001316675,5237260000001316693,5237260000001316716,5237260000001316753,5237260000001328413,5237260000001328475,5237260000001329214,5237260000001329274,5237260000001329293,5237260000001329333,5237260000001329334,5237260000001329353,5237260000001329354,5237260000001329473,5237260000001329533,5237260000001330394,5237260000001333794,5237260000001333833,5237260000001334874,5237260000001336193,5237260000001336195,5237260000001336233,5237260000001336253,5237260000001336433,5237260000001341913,5237260000001270393,5237260000001351613,5237260000001356833,5237260000001357113,5237260000001358417,5237260000001361113,5237260000001367953,5237260000001367993,5237260000001368035,5237260000001371673,5237260000001375515,5237260000001377673,5237260000001379794,5237260000001382314,5237260000001442553,5237260000001385235,5237260000001387173,5237260000001387594,5237260000001387693,5237260000001387853,5237260000001389234,5237260000001389453,5237260000001391213,5237260000001392233,5237260000001401514,5237260000001402653,5237260000001402674,5237260000001402873,5237260000001405218,5237260000001411293,5237260000001412493,5237260000001419534,5237260000001432018,5237260000001434013,5237260000001436294,5237260000001436293,5237260000001442653,5237260000001436975,5237260000001437173,5237260000001437413,5237260000001442533,5237260000001442474,5237260000001442573,5237260000001442633,5237260000001444013,5237260000001446915,5237260000001446953,5237260000001450313,5237260000001450314,5237260000001451199,5237260000001451233,5237260000001452473,5237260000001452513,5237260000001453954,XYZ,5237260000001455553,5237260000001453959,5237260000001455493,5237260000001458213,5237260000001460933,5237260000001464713,5237260000001464713,5237260000001467494,5237260000001467503,5237260000001470540,5237260000001469073,5237260000001467494,5237260000001469285,5237260000001469286,5237260000001469899,5237260000001470369,5237260000001470394,5237260000001470551,5237260000001471138,5237260000001471222,5237260000001471527,5237260000001471533,5237260000001471551,5237260000001471533,5237260000001471774,5237260000001471829,5237260000001471842,5237260000001471853,5237260000001472008,5237260000001472010,5237260000001472012,5237260000001474332,5237260000001475964,5237260000001476796,5237260000001477013,5237260000001477017,5237260000001477221,5237260000001478585,5237260000001478760,5237260000001479039,5237260000001479040"
#ruleset = rules.split(",")
    ruleset = [str(x) for x in (rule_map.index).to_list()]

    rule_scores = rule_mapping["SCORE"]
    DS_ruleset = rule_map[rule_map["SCORE"] <0].to_dict()["SCORE"]

    UP_ruleset = rule_map[rule_map["SCORE"] >= 0].to_dict()["SCORE"]
    
    Rule_Efficiency = rule_giver(ruleset,DS_ruleset,UP_ruleset,primary_rules,rule_scores,rule_mapping)
    Rule_Efficiency["Fraud Rate %"] = round((Rule_Efficiency["Fraud"]  / Rule_Efficiency["Total triggered orders"])*100,2)
        #Rule_Efficiency["Total triggered orders"] = Rule_Efficiency["Fraud"] + Rule_Efficiency["No Fraud"]
        #Rule_Efficiency["Total Live Orders"] = primary_rules[primary_rules["Score_Total_Score"] >= 4000].count()[0]
        #Rule_Efficiency["Automation %"] = round((1- (Rule_Efficiency["Total Live Orders"]  / ( Rule_Efficiency["Total triggered orders"] +  Rule_Efficiency["Total Live Orders"] )))*100,2)
        #Rule_Efficiency = Rule_Efficiency[~Rule_Efficiency.index.duplicated(keep='first')]
        #Rule_Efficiency= Rule_Efficiency[Rule_Efficiency["Total triggered orders"]>0]
    Rule_Efficiency= Rule_Efficiency[~Rule_Efficiency.index.duplicated(keep='first')]
    remove_zeros_scores(Rule_Efficiency)
    score_adjustments = Score_Adjustment(Rule_Efficiency,ruleset,DS_ruleset,UP_ruleset)
        
        
    Rule_Efficiency["Score Adjustment"] = Rule_Efficiency.index.map(score_adjustments.to_dict()['Score Ajustment'])
    Rule_Efficiency= Rule_Efficiency[Rule_Efficiency["Total triggered orders"] >0]
    upscores_adjust(Rule_Efficiency)  #in test

    Rule_Efficiency = Rule_Efficiency[['Rule Name','Rule Score','Score Adjustment','Fraud','No Fraud','Fraud Rate %','Total triggered orders','Total Live Orders','Real Impact UP','Real Fraud Impact UP','Real Impact DS','Real Fraud Impact DS','Distribution','Fraud Distribution','Fraud Scores','Scores','Order ID','Real vs total trigger rate','Global Automation %']]
    #Rule_Efficiency= Rule_Efficiency.style.bar(subset=['Rule Score', 'Score Adjustment'], align='mid', color=['#d65f5f', '#5fba7d'])
        
    Rule_Efficiency.to_excel(r"Accertify - Rules Efficiency Report-{}.xlsx".format("TEST"))
    print("An Excel file has been created into Shared drives/Rule-Servant directory")
    return Rule_Efficiency

def month(date):
    if str(date) >= "2019-07-00 00:00:00" and str(date) < "2019-07-31 23:59:59":
        return "July19"
    elif str(date) >= "2019-02-00 00:00:00" and str(date) < "2019-02-31 23:59:59":
        return "February19"
    elif str(date) >= "2019-01-00 00:00:00" and str(date) < "2019-01-31 23:59:59":
        return "January19"
    elif str(date) >= "2019-03-00 00:00:00" and str(date) < "2019-03-31 23:59:59":
        return "March19"
    elif str(date) >= "2019-04-00 00:00:00" and str(date) < "2019-04-31 23:59:59":
        return "April19"
    elif str(date) >= "2019-05-00 00:00:00" and str(date) < "2019-05-31 23:59:59":
        return "May19"
    elif str(date) >= "2019-06-00 00:00:00" and str(date) < "2019-06-31 23:59:59":
        return "June19"
    elif str(date) >= "2019-08-00 00:00:00" and str(date) < "2019-08-31 23:59:59":
        return "August19"
    elif str(date) >= "2019-09-00 00:00:00" and str(date) < "2019-09-31 23:59:59":
        return "September19"
    elif str(date) >= "2019-10-00 00:00:00" and str(date) < "2019-10-31 23:59:59":
        return "October19"
    elif str(date) >= "2019-11-00 00:00:00" and str(date) < "2019-11-31 23:59:59":
        return "November19"
    elif str(date) >= "2019-12-00 00:00:00" and str(date) < "2019-12-31 23:59:59":
        return "December19"
    elif str(date) >= "2020-01-00 00:00:00" and str(date) < "2020-01-31 23:59:59":
        return "January20"
    elif str(date) >= "2020-02-00 00:00:00" and str(date) < "2020-02-31 23:59:59":
        return "February20"
    elif str(date) >= "2020-03-00 00:00:00" and str(date) < "2020-03-31 23:59:59":
        return "March20"
    elif str(date) >= "2020-04-00 00:00:00" and str(date) < "2020-04-31 23:59:59":
        return "April20"
    elif str(date) >= "2020-05-00 00:00:00" and str(date) < "2020-05-31 23:59:59":
        return "May20"
    elif str(date) >= "2020-06-00 00:00:00" and str(date) < "2020-06-31 23:59:59":
        return "June20"
    elif str(date) >= "2020-07-00 00:00:00" and str(date) < "2020-07-31 23:59:59":
        return "July20"
    elif str(date) >= "2020-08-00 00:00:00" and str(date) < "2020-08-31 23:59:59":
        return "August20"
    elif str(date) >= "2020-09-00 00:00:00" and str(date) < "2020-09-31 23:59:59":
        return "September20"
    elif str(date) >= "2020-10-00 00:00:00" and str(date) < "2020-10-31 23:59:59":
        return "October20"
    elif str(date) >= "2020-11-00 00:00:00" and str(date) < "2020-11-31 23:59:59":
        return "November20"
    elif str(date) >= "2020-12-00 00:00:00" and str(date) < "2020-12-31 23:59:59":
        return "December20"
    elif str(date) >= "2021-01-00 00:00:00" and str(date) < "2021-01-31 23:59:59":
        return "January21"
    elif str(date) >= "2021-02-00 00:00:00" and str(date) < "2021-02-31 23:59:59":
        return "February21"


def resolution(res):
    if (res == "Buyer Fraud Prevented") or (res == "Buyer Fraud  Loss") or (res == "Chargeback Received - Fraud"):
        return "Fraud"
    else:
        return "No Fraud"


def rule_searcher(rule,primary_rules):
    rule_table = primary_rules[primary_rules["Rules_Tripped_in_RTD"].str.contains(rule)]
    rule_table_pivot = rule_table.pivot_table(index=["Rules_Tripped_in_RTD"],columns=["ResolutionType"],values=["Order_ID"],aggfunc="count")
    rule_table_pivot.fillna(0)
    rule_db =  rule_table_pivot
    if  (len(rule_db.columns) == 2) and   (rule_db.columns[0][1] == "Fraud" ):
        new_rule_db = pd.DataFrame(data = [[rule_db["Order_ID"]["Fraud"].sum(),rule_db["Order_ID"]["No Fraud"].sum()]],index=[rule])
        new_rule_db.columns = ["Fraud","No Fraud"]
        new_rule_db["Fraud Rate"] = ((rule_db["Order_ID"]["Fraud"].sum()) / (new_rule_db["No Fraud"]+new_rule_db["Fraud"].sum()))*100
        return new_rule_db
    elif (len(rule_db.columns) == 1) and (rule_db.columns[0][1] == "Fraud"):
        new_rule_db = pd.DataFrame(data = [[rule_db["Order_ID"]["Fraud"].sum()]],index=[rule])
        new_rule_db.columns = ["Fraud"]
        new_rule_db["Fraud Rate"] = (rule_db["Order_ID"]["Fraud"].sum() /(rule_db["Order_ID"]["Fraud"].sum()))*100
        return new_rule_db
    elif rule_db.columns[0][1] == "No Fraud":
        new_rule_db = pd.DataFrame(data = [[rule_db["Order_ID"]["No Fraud"].sum()]],index=[rule])
        new_rule_db.columns = ["No Fraud"]
        new_rule_db["Fraud Rate"] = (0 / rule_db["Order_ID"]["No Fraud"].sum())*100
        return new_rule_db


#primary_rules = primary[((primary["sim_dc_reasons"] == "{'Fraud Reviewed - Allowed'}") | (primary["sim_dc_reasons"] == "{'Alto riesgo de fraude'}") |  (primary["sim_dc_reasons"] == "{}") |
 #                        (primary["sim_dc_reasons"] == "{'Colusion vendedor-comprador'}") | (primary["sim_dc_reasons"] == "{'Detectado fraude en fraud check/documentacion retocada'}") | (primary["sim_dc_reasons"] == "{'Fraud Discovered'}") |
  #                       (primary["sim_dc_reasons"] == "{'Suplantacion de identidad'}") |  (primary["sim_dc_reasons"] == "{'Comprador desconoce el cargo'}"))  & ((primary["sim_dc"] == "{'REJECTED'}") |(primary["sim_dc"] == "{'APPROVED'}")| (primary["sim_dc"] == "{'APPROVED FRAUD SUFFERED'}"))]

def rule_giver(ruleset,DS_ruleset,UP_ruleset,primary_rules,rule_scores,rule_mapping):

    scores = pd.DataFrame([[0]],index=ruleset)
    count_DS={key:0 for key in DS_ruleset}
    count_UP = {key:0 for key in UP_ruleset}
    count_UP_only_fraud = {key:0 for key in UP_ruleset}
    count_DS_only_fraud = {key:0 for key in DS_ruleset}
    Fraud_scores ={key:[0] for key in ruleset}
  

    for rul in ruleset:

      for id in primary_rules[primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)]["Score_FARE"]:
        df = primary_rules[primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)]
        fscore= df[df["ResolutionType"] == "Fraud"]["Score_FARE"].values
        Fraud_scores[rul] =  sorted(fscore)

        if (int(rul) in DS_ruleset.keys()) & (id >= 4000) & (pd.Series(int(rul)).map(DS_ruleset)[0] != 0):
          if (id +(pd.Series(int(rul)).map(DS_ruleset)[0]) < 4000) & (id >= 4000):
            scores.update(pd.DataFrame([[" ".join(sorted([str(x) for x in primary_rules[primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)]["Score_FARE"].values]))]],index=[rul]))
            count_DS[int(rul)] += 1
            if (id +(pd.Series(int(rul)).map(DS_ruleset)[0]) < 4000) & (id >= 4000):
              count_DS_only_fraud[rul] = primary_rules[(primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)) & (primary_rules["ResolutionType"] == "Fraud") & ((primary_rules["Score_FARE"] + pd.Series(int(rul)).map(rule_scores)[0] )<4000) & (primary_rules["Score_FARE"] >= 4000)]["Score_FARE"].count()


        else:
          if (int(rul)  in UP_ruleset.keys()) & (id < 4000)& (pd.Series(int(rul)).map(UP_ruleset)[0] != 0)  :
            if (id + (pd.Series(int(rul)).map(UP_ruleset)[0]) >= 4000)  & (id < 4000):
          
              count_UP[int(rul)] += 1
              scores.update(pd.DataFrame([[" ".join(sorted([str(x) for x in primary_rules[primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)]["Score_FARE"].values]))]],index=[rul]))
              if (id + (pd.Series(int(rul)).map(UP_ruleset)[0]) >= 4000)  & (id < 4000):
                count_UP_only_fraud[rul] = primary_rules[(primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)) & (primary_rules["ResolutionType"] == "Fraud") & ((primary_rules["Score_FARE"] + pd.Series(int(rul)).map(rule_scores)[0] )>=4000) & (primary_rules["Score_FARE"] < 4000)]["Score_FARE"].count()
              
              
    data = pd.DataFrame(data=[[0.0,0.0,0.0]],index=ruleset)
    data.columns = ["Fraud","No Fraud","Fraud Rate %"]
    data["Rule Name"] = pd.Series([int(x) for x in data.index],index=ruleset).map(rule_mapping["RULE NAME"])
    orders = pd.DataFrame([[0]],index=ruleset)
    dist = pd.DataFrame([[0]],index=ruleset)
    dist_fraud = pd.DataFrame([[0]],index=ruleset)

    for rul in data.index:
        if primary_rules["Rules_Tripped_in_RTD"].str.contains(rul).sum() > 0:
            data.update(rule_searcher(rul,primary_rules))
            dist.update(pd.DataFrame([[primary_rules[primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)]["Recommendation_Code"].value_counts()]],index=[rul]))
            dist_fraud.update(pd.DataFrame([[primary_rules[(primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)) & (primary_rules["ResolutionType"] == "Fraud")]["Recommendation_Code"].value_counts()]],index=[rul]))
            orders.update(pd.DataFrame([[" ".join([str(x) for x in primary_rules[primary_rules["Rules_Tripped_in_RTD"].str.contains(rul)]["Order_ID"].values])]],index=[rul]))

    data["Total triggered orders"] = data["Fraud"] + data["No Fraud"]
    data["Total Live Orders"] = primary_rules[primary_rules["Score_Total_Score"] >= 4000].count()[0]
    data["Real Impact DS"] = pd.Series([int(x) for x in data.index],index=ruleset).map(count_DS)
    data["Real Impact UP"]= data["Real Impact DS"].fillna(0)
    data["Real Impact UP"] = pd.Series([int(x) for x in data.index],index=ruleset).map(count_UP)
    data["Real Impact UP"]= data["Real Impact UP"].fillna(0)

    data["Real Fraud Impact UP"] = data.index.map(count_UP_only_fraud)
    data["Real Fraud Impact DS"] = data.index.map(count_DS_only_fraud)

    data["Fraud Scores"] = data.index.map(Fraud_scores)
    data= data[~data.index.duplicated(keep='first')]
    #data["Automation % per rule"] = round((1- (data["Total Live Orders"]  / ( data["Total triggered orders"] +  data["Total Live Orders"] )))*100,2)
    data["Global Automation %"] = round((1- (data["Total Live Orders"]  / ( data["Real Impact DS"].sum() +  data["Total Live Orders"] )))*100,2)
    scores.columns = ["Scores"]
    dist.columns = ["Distribution"]
    dist_fraud.columns = ["Fraud Distribution"]
    orders.columns = ["Order ID"]
    
    merge_0 = pd.merge(dist ,dist_fraud, left_index=True, right_index=True)
    merge_1 = pd.merge(orders ,merge_0, left_index=True, right_index=True)
    merge_2 = pd.merge(data,merge_1 , left_index=True, right_index=True)
    merge_3 = pd.merge(merge_2,scores , left_index=True, right_index=True)
    #merge_2["Scores"] = pd.Series([int(x) for x in merge_2.index.index],index=ruleset).map(scores)
    merge_3["Real vs total trigger rate"] = round(((merge_3["Real Impact DS"] + merge_3["Real Impact UP"]) / merge_3["Total triggered orders"])*100,2)
    merge_3["Rule Score"] = pd.Series([int(x) for x in merge_3.index],index=merge_3.index).map(rule_scores)  
    return merge_3


"""def Score_Adjustment(Rule_Efficiency):  #old version
  optimization_advise ={key:[0] for key in [x for x in set(ruleset)]}
  optimization_advise_DS2 = {str(key):[0] for key in DS_ruleset}  
  optimization_advise_DS = {str(key):[0] for key in DS_ruleset}  
  optimization_advise_UP = {str(key):[0] for key in UP_ruleset}  

  for rul in ruleset:
    if Rule_Efficiency.loc[rul]["Scores"] != 0:
      
      for sc in Rule_Efficiency.loc[rul]["Scores"].split(" "):
        if (float(Rule_Efficiency.loc[rul]["Rule Score"]) < 0) & (float(sc) >=4000) & (float(sc) <10000):
          optimization_advise_DS2[rul] = [float(Rule_Efficiency.loc[rul]["Rule Score"]) - (float(max(Rule_Efficiency.loc[rul]["Scores"].split(" ")))  - (float(4000) - float(Rule_Efficiency.loc[rul]["Rule Score"])))]
          if (float(sc) + Rule_Efficiency.loc[rul]["Rule Score"]) < 4000:
          #print([Rule_Efficiency.loc[rul]["Rule Score"] - (Rule_Efficiency.loc[rul]["Rule Score"] + (float(sc) - 4000))])
            optimization_advise_DS[rul] += [Rule_Efficiency.loc[rul]["Rule Score"] - (Rule_Efficiency.loc[rul]["Rule Score"] + (float(sc) - 4000))]
      #optimization_advise["5237260000001437413"] += [(float(sc) - 4000)]
            

        elif (float(Rule_Efficiency.loc[rul]["Rule Score"]) > 0) & (float(sc) < 4000):
          if (float(sc) + Rule_Efficiency.loc[rul]["Rule Score"]) >= 4000:
          #print([-1*((Rule_Efficiency.loc[rul]["Rule Score"]) - (Rule_Efficiency.loc[rul]["Rule Score"] + (4000 - float(sc))))])
            optimization_advise_UP[rul] += [-1*((Rule_Efficiency.loc[rul]["Rule Score"]) - (Rule_Efficiency.loc[rul]["Rule Score"] + (4000 - float(sc))))]

  optimization_advise_DS2 = pd.DataFrame([min(value) for value in optimization_advise_DS2.values()],index=optimization_advise_DS2.keys())
  optimization_advise_DS2.columns = ["Score Ajustment"]
  optimization_advise_UP = pd.DataFrame([max(value) for value in optimization_advise_UP.values()],index=optimization_advise_UP.keys())
  optimization_advise_UP.columns = ["Score Ajustment"]
  return pd.concat([optimization_advise_DS2,optimization_advise_UP])"""

def Score_Adjustment(Rule_Efficiency,ruleset,DS_ruleset,UP_ruleset):
  optimization_advise ={key:[0] for key in [x for x in set(ruleset)]}
  optimization_advise_DS2 = {str(key):[0] for key in DS_ruleset}  
  optimization_advise_UP2 = {str(key):[0] for key in UP_ruleset}
  optimization_advise_DS = {str(key):[0] for key in DS_ruleset}  
  optimization_advise_UP = {str(key):[0] for key in UP_ruleset}  
  for rul in Rule_Efficiency.index.values:
    if Rule_Efficiency.loc[rul]["Scores"] != 0:

        for sc in Rule_Efficiency.loc[rul]["Scores"].split(" "):
          if (float(Rule_Efficiency.loc[rul]["Rule Score"]) < 0) & (float(sc) >=4000) & (float(sc) <10000):
            optimization_advise_DS2[rul] = [round(float(Rule_Efficiency.loc[rul]["Rule Score"]) - (float(max(Rule_Efficiency.loc[rul]["Scores"].split(" ")))  - (float(4000) - float(Rule_Efficiency.loc[rul]["Rule Score"]))),-2)]
            #if (float(sc) + Rule_Efficiency.loc[rul]["Rule Score"]) < 4000:
        #print([Rule_Efficiency.loc[rul]["Rule Score"] - (Rule_Efficiency.loc[rul]["Rule Score"] + (float(sc) - 4000))])
              #optimization_advise_DS[rul] += [Rule_Efficiency.loc[rul]["Rule Score"] - (Rule_Efficiency.loc[rul]["Rule Score"] + (float(sc) - 4000))]
      #optimization_advise["5237260000001437413"] += [(float(sc) - 4000)]
            

          elif (float(Rule_Efficiency.loc[rul]["Rule Score"]) > 0) & (float(sc) < 4000):
            
            if (float(sc) + Rule_Efficiency.loc[rul]["Rule Score"]) >= 4000:
              #print([-1*((Rule_Efficiency.loc[rul]["Rule Score"]) - (Rule_Efficiency.loc[rul]["Rule Score"] + (4000 - float(sc))))])
              #optimization_advise_UP[rul] += [-1*((Rule_Efficiency.loc[rul]["Rule Score"]) - (Rule_Efficiency.loc[rul]["Rule Score"] + (4000 - float(sc))))]
              if (Rule_Efficiency.loc[rul]["Fraud Scores"] != [0]) & (Rule_Efficiency.loc[rul]["Fraud Scores"] != []):
                optimization_advise_UP2[rul] = [round((4000 - (min(Rule_Efficiency.loc[rul]["Fraud Scores"]) + Rule_Efficiency.loc[rul]["Rule Score"])) + Rule_Efficiency.loc[rul]["Rule Score"],-2)]

  optimization_advise_DS2 = pd.DataFrame([min(value) for value in optimization_advise_DS2.values()],index=optimization_advise_DS2.keys())
  optimization_advise_DS2.columns = ["Score Ajustment"]
  optimization_advise_UP2 = pd.DataFrame([max(value) for value in optimization_advise_UP2.values()],index=optimization_advise_UP2.keys())
  optimization_advise_UP2.columns = ["Score Ajustment"]
  return pd.concat([optimization_advise_DS2,optimization_advise_UP2])

def upscores_adjust(df):
  for order in df.index.values:
    if (df["Rule Score"][order] >0) & (df["Score Adjustment"][order] < 0):
      df["Score Adjustment"][order] = 0
    else:
      df["Score Adjustment"][order] = round(df["Score Adjustment"][order],-2)

def remove_zeros_scores(df):
  for order in df.index.values:
    if 0 in df["Fraud Scores"][order]:
      df["Fraud Scores"][order].remove(0)