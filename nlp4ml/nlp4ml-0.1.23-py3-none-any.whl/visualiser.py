import matplotlib.pyplot as plt
import seaborn as sns


def plot_missing_value_heatmap(data):
    """
    Parameters
    ----------
    data: pd.DataFrame
    """
    plt.figure(figsize=(15, 10))
    sns.heatmap(data.isnull(), cbar=True, cmap=sns.color_palette("cubehelix"))
    plt.title("Missing Values Heatmap",
              fontdict={'family': 'serif', 'weight': 'normal', 'size': 16})
    plt.show()


def plot_correlation(corr):
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        corr[(corr >= 0.5) | (corr <= -0.4)],
        cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
        annot=True, annot_kws={"size": 8}, square=True)
    plt.show()
