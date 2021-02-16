
def plot_shap_abundances_and_ratio(estimator, train, important_features, bacteria_name, short_bacteria_name_fn, file_name, threshold = 0.5):
    """ Plot the shap values and abundances and ratios

    Plot that is used when working with ratios. We wanted to see plots side-by-side that represent the abundance of bacteria. On the other plot
    the ratio of these two bacterias. We wanted to understand better this mapping of abundances to ratios. At the end we concluded that we want 
    to use the bacteria in the numerator that has the least number of crossings when we look at the 2 abundances.
    """
    sns.set_style("whitegrid")
    _X_train, _y_train = df2vectors(train, important_features)
    _y_train = np.array(_y_train.values)//30
    #print(_y_train.shape, _X_train.shape)
    #df_abundance ={"X_train":X_train, "y_train":np.array(y_train.values)//30}
    
    train["month"] = train["age_at_collection"]//30
    train_mon = train[important_features+[bacteria_name, "month"]].groupby("month").agg(np.mean).reset_index()
    X_train, y_train = df2vectors(train_mon, important_features, time_col="month")
    X_features_and_age = np.hstack((X_train, np.array(y_train).reshape(-1, 1)))
    
    important_features_short = list(map(short_bacteria_name_fn, important_features)) #list(map(lambda x: f"log of ratio {x.split('g__')[1]}/{bacteria_name.split('g__')[1]}" if len( x.split("g__"))>1 else 'Other' ,important_features))
    
    plt.rc('axes', labelsize= 14)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize= 12)
    plt.rc('legend', fontsize= 13)

    fig, axs = plt.subplots(len(important_features), 3, figsize=(30,len(important_features)*7))
    
    for i in range(len(important_features)):
        name = important_features[i]
        name_short = important_features_short[i]
        
        #idx_same = np.where(np.isclose(X_train[:,i], 0.0, atol=threshold))[0]
        
        train_bacteria_name = train[[f"abundance_{bacteria_name}", "month"]].groupby("month").agg(np.mean)
        train_name          = train[[f"abundance_{name}", "month"]].groupby("month").agg(np.mean)
        months              = train_bacteria_name.reset_index()["month"].values
        diff_ref_and_taxa   = train_bacteria_name.values.reshape(-1) - train_name.values.reshape(-1)
        diff_ref_and_taxa   = -diff_ref_and_taxa if diff_ref_and_taxa[0]<0 else diff_ref_and_taxa
        signchange =  ((np.roll(np.sign(diff_ref_and_taxa), 1) - np.sign(diff_ref_and_taxa)) != 0).astype(int) 
        signchange[0] = 0
        idx_cross = np.where(signchange==1)[0]

        # shap plot
        #X_features_and_age = np.hstack((X_train, np.array(y_train).reshape(-1, 1)))
        idx_of_age = X_features_and_age.shape[1]-1
        explainer = shap.TreeExplainer(estimator)
        shap_values = explainer.shap_values(X_features_and_age)
        inds = shap.approximate_interactions(idx_of_age, shap_values, X_features_and_age)
        shap.dependence_plot(i, shap_values, X_features_and_age, feature_names=important_features_short+["Age at collection [month]"], interaction_index=inds[idx_of_age], ax=axs[i][0], show=False, dot_size=30)
        axs[i][0].plot(np.zeros(10), np.linspace(np.min(shap_values[:,i]), np.max(shap_values[:,i]), 10), lw=10, alpha=0.5, color="orange")
        axs[i][0].plot(X_features_and_age[:,i][idx_cross],shap_values[:,i][idx_cross], marker="X", markersize=15, color="red", lw=0, alpha=0.7)
        
        sns.pointplot(x=train["age_at_collection"]//30, y=train[f"abundance_{name}"], capsize=.2, alpha=0.4, ax=axs[i][1], color="green", label=name_short)
        sns.pointplot(x=train["age_at_collection"]//30, y=train[f"abundance_{bacteria_name}"], capsize=.2, alpha=0.4, ax=axs[i][1], color="blue", label=f"{bacteria_name.split('g__')[1]} (reference)")
        #axs[i][1].plot(months[idx_same], train_name.values.reshape(-1)[idx_same], marker="*", markersize=10, color="orange", lw=0, label="same")
        axs[i][1].plot(months[idx_cross]-0.5, train_name.values.reshape(-1)[idx_cross], marker="X", markersize=15, color="red", lw=0, alpha=1.0, label="crossed")
        axs[i][1].set_ylabel("Abundance")
        axs[i][1].set_xlabel("Age at collection [month]")

        
        sns.pointplot(x=_y_train, y=_X_train[:,i], capsize=.2, alpha=0.4, ax=axs[i][2], color="gray")
        #x = (np.array(y_train)//30).flatten()
        #y = X_train[:,i].flatten()
        #axs[i][2].plot(x[idx_same], y[idx_same], marker="*", markersize=10, color="orange", lw=0)
        axs[i][2].plot(np.linspace(0, 38, 10), np.zeros(10), lw=10, alpha=0.5, color="orange")
        axs[i][2].plot(months[idx_cross]-0.5, np.zeros(len(idx_cross)), alpha=0.7, marker="X", markersize=15, color="red", lw=0)
        axs[i][2].set_ylabel(important_features_short[i])
        axs[i][2].set_xlabel("Age at collection [month]")
        

        custom_lines = [Line2D([0], [0], color="green", ls="-", marker="o", lw=4),
                        Line2D([0], [0], color="blue", ls="-", marker="o", lw=4),
                        #Line2D([0], [0], color="orange", marker="*", markersize=10, ls="--", lw=0),
                        Line2D([0], [0], color="red", marker="X", markersize=10, ls="--", lw=0),
                        Line2D([0], [0], color="orange", ls="-", alpha=0.4, lw=10)]
        #print(name_short)
        axs[i][2].legend(custom_lines, [important_features[i].split('g__')[1], f"{bacteria_name.split('g__')[1]} (reference)", "crossed", "zero log-ratio"], loc="upper left", bbox_to_anchor=(1, 1))

    #print("/".join(file_name.split("/")[:-1]))
    pathlib.Path("/".join(file_name.split("/")[:-1])).mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()



def shap_important_bacteria_ratios_with_age(estimator, X_train, y_train, important_features, short_bacteria_name_fn, file_name):
    """Dependency plot: y-axis = shap value, x-axis = bacteria abundance/ratio, color = age"""
    ncols = 5
    fig, axs = plt.subplots(len(important_features)//ncols+1, ncols, figsize=(42,(len(important_features)//ncols+1)*5)) 

    important_features_short = list(map(lambda x: short_bacteria_name_fn(x), important_features))

    X_features_and_age = np.hstack((X_train, np.array(y_train).reshape(-1, 1)))
    idx_of_age = X_features_and_age.shape[1]-1
    explainer = shap.TreeExplainer(estimator)
    shap_values = explainer.shap_values(X_features_and_age)
    inds = shap.approximate_interactions(idx_of_age, shap_values, X_features_and_age)
    
    for i in range(len(important_features_short)):
        shap.dependence_plot(i, shap_values, X_features_and_age, feature_names=important_features_short+["Age at collection [day]"], interaction_index=inds[idx_of_age], ax=axs[i//ncols,i%ncols], show=False, dot_size=20, cmap=None)
        bact_min = np.min(X_features_and_age[:,i])
        bact_max = np.max(X_features_and_age[:,i])
        axs[i//ncols,i%ncols].plot(np.linspace(bact_min, bact_max, 10), np.zeros(10), lw=4, alpha=0.5, color="orange")
        if i%ncols == 0:
            axs[i//ncols,i%ncols].set_ylabel("SHAP value")
        else:
            axs[i//ncols,i%ncols].set_ylabel("")
        if i != 0:
            fig.axes[-1].remove()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.show()
