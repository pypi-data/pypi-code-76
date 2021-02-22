import seaborn as sns
import pandas as pd

def plot_correlation(data,file_loc):
    plt.figure(figsize=(10,10))

    corr = data.corr().round(1)
    #corr = corrdata.corr().abs().round(1)
    corr.index = corrdata.columns
    sns.heatmap(corr, annot = False, cmap='viridis', vmin=-1, vmax=1,square=True, linewidths=.5,)
    plt.title("Correlation Heatmap", fontsize=16)
    plt.savefig(file_loc)
    plt.show()

