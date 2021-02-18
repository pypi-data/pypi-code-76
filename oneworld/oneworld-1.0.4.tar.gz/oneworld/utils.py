"""Common functions for StaticMap and WebMap"""
import os
import re
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import pandas as pd
#
def get_hexes(data, palette, n_colors, minval, maxval, ndec):
    """given a seq of nums or strings (categorical), 
       get the corresponding hex colors according
       to palette. Palette can be an array of hex colors or a string
       with the name of the seaborn palette
       (Note: it uses seaborn palette bc specifying
       n_colors in seaborn returns the corresponding palette as
       in the colorbrewer webpage. The plt default colormaps
       just use the whole 9 color palette and divide them in more
       or less chunks)"""
    # numerical data
    if all(isinstance(x, (int, float)) for x in data):
        quant = False
        if not minval:
            minval = min(data)
        if not maxval:
            maxval = max(data)
        curr_palette = sns.color_palette(palette, n_colors)
        full_palette_hex = curr_palette.as_hex()
        sm = plt.cm.ScalarMappable(cmap=mcolors.ListedColormap(curr_palette),
                                norm=plt.Normalize(vmin=minval, vmax=maxval))
        rgba_lst = sm.to_rgba(data)
        col_lst = [mcolors.to_hex(x) for x in rgba_lst]
        col_leg = []
        # get the evenly spaced intervals and the corresponding color
        for i in range(n_colors):
            lower_lim = minval + i * (maxval - minval) / n_colors
            upper_lim = minval + (i+1) * (maxval - minval) / n_colors
            legend_label = '{:,.{}f} - {:,.{}f}'.format(lower_lim, ndec, upper_lim, ndec)
            col_leg.append((legend_label,full_palette_hex[i]))
    # categorical data
    elif all(isinstance(x, str) for x in data):
        quant = True
        # Get unique values (preserve order, no sets)
        uniq_vals = []
        for val in data:
            if val not in uniq_vals:
                uniq_vals.append(val)
        # set palette for the number of unique values
        n_colors = len(uniq_vals)
        if isinstance(palette, (list, tuple)):
            if len(palette) < n_colors:
                raise IndexError("Palette smaller than number of categories")
                return
            curr_palette = [mcolors.to_rgb(x) for x in palette]
            full_palette_hex = palette
        else:
            curr_palette = sns.color_palette(palette, n_colors)
            full_palette_hex = curr_palette.as_hex()
        # set colors list corresponding to given vars
        col_lst = [full_palette_hex[uniq_vals.index(x)] for x in data]
        # now the full color spectrum (full ordered palette) for the legend
        col_leg = [list(x) for x in zip(uniq_vals, full_palette_hex)]
        # set a scalar mappable in case it is requested by a colorbar
        sm = plt.cm.ScalarMappable(cmap = mcolors.ListedColormap(curr_palette))
    # if not (mixed vals), no can do
    else:
        raise ValueError("Mixed variable types in color column")
        return
    # all done
    return col_lst, col_leg, quant, sm
#
def get_sizes(data, sizes, legend_labels, minval, maxval, ndec):
    """Get the corresponding sizes chosen
       from an evenly divided range between sizes[0] and sizes[1].
       Set also the value-size pairs for the legend"""
    # get caps as desired
    if not minval:
        minval = min(data)
    if not maxval:
        maxval = max(data)
    # size scale
    minsiz = float(sizes[0])
    maxsiz = float(sizes[1])
    # rescale values on the size scale
    siz_lst = rescale(minval, maxval, minsiz, maxsiz, data)
    # choose n values to plot on legend
    siz_leg = []
    # if legend_labels is a number, get evenly spaced intervals
    if isinstance(legend_labels, (int, float)):
        legend_vals = []
        for indx_lbl in range(legend_labels):
            this_val = minval + indx_lbl*(maxval - minval)/(legend_labels-1)
            legend_vals.append(this_val)
    # if it is a seq, get the sizes corresponding to each element
    elif isinstance(legend_labels, (list, tuple)):
        legend_vals = legend_labels
    # unrecognized type
    else:
        raise TypeError("legend_labels must be int, float, list or tuple")
        return
    #rescale values on the size scale
    legend_sizes = rescale(minval, maxval, minsiz, maxsiz, legend_vals)
    # set the legend labels-sizes pairs
    legend_vals_fmt = ['{:,.{}f}'.format(x, ndec) for x in legend_vals]
    siz_leg = [list(x) for x in zip(legend_vals_fmt, legend_sizes)]
    # Done
    return siz_lst, siz_leg
#
def rescale(x0, x1, y0, y1, z_seq):
    """Given a seq z_seq between x0 and x1 rescale all its elements 
       in the scale [y0, y1] maintaining proportional position"""
    z_prime_seq = []
    for z in z_seq:
        z_prime = y0 + (z - x0) * ((y1-y0) / (x1-x0))
        z_prime_seq.append(z_prime)
    return z_prime_seq

def clean_string(string):
    """Remove non alphanumeric characters from a layer name. Do not
    change regex, or if you do, change colorbar template accordingly"""
    regex = re.compile('[\W]+', re.UNICODE)
    clean_string = regex.sub('', string)
    return clean_string

def load_dataset(name):
    """load an example dataset"""
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                             '..','tests','tests_data'))
    kwargs = {}
    if name == "farms": kwargs = {"dtype" : {"FIPS":str}}
    if name == "conferences": kwargs = {"dtype" : {"Expenditures": float}}
    if name == "connections": kwargs = {"dtype" : {"Init": int, "Final": int}}
    df = pd.read_csv(data_path+'/'+name+".csv", **kwargs)
    return df

