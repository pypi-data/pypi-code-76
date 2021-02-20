

def plot_heatmap(data, figsize=None, cmap='rainbow', cbar=True,
                 annot=True, square=True, vmax=1, vmin=0, linewidths=0,
                 xticklabels=True, yticklabels=True, is_mask=False):
    """
    URL: http://seaborn.pydata.org/generated/seaborn.heatmap.html?highlight=heatmap#seaborn.heatmap
    """

    # Import libs
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt

    if is_mask:
        mask = np.zeros_like(data)
        mask[np.triu_indices_from(mask)] = True

        fig = plt.figure(figsize=figsize)
        sns.heatmap(data, cmap=cmap, cbar=cbar, annot=annot, square=square,
                    vmax=vmax, vmin=vmin, linewidths=linewidths,
                    xticklabels=xticklabels, yticklabels=yticklabels, mask=mask)
        plt.plot()
        plt.show()
    else:
        fig = plt.figure(figsize=figsize)
        sns.heatmap(data, cmap=cmap, cbar=cbar, annot=annot, square=square,
                    vmax=vmax, vmin=vmin, linewidths=linewidths,
                    xticklabels=xticklabels, yticklabels=yticklabels)
        plt.plot()
        plt.show()
