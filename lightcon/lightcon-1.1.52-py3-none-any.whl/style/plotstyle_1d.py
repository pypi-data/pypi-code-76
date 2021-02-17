import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.offsetbox import ( OffsetImage,AnchoredOffsetbox)

import numpy as np
from PIL import Image
from pathlib import Path
from matplotlib import rcParams

available_wm_widths = np.array([100, 150, 300, 800, 1200])
wm_min_ratio_axis = 0.3
wm_min_ratio_figure = 0.5
wm_alpha = 0.2

def apply_style():
    """Applies the Light Conversion stylesheet to matplotlib
    """
    stylesheet_path = Path(str(Path(__file__).parent) + '\\lcstyle.mplstyle')

    mpl.style.use('default')
    mpl.style.use(stylesheet_path)
    
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['Source Sans Pro']

def reset():
    """Applies the default matplotlib stylesheet"""
    mpl.style.use('default')
    

def _determine_width_(target_width, ratio, use_larger = True):
    """Determines the optimal width for watermark"""
    out_width = None
    if use_larger:
        avails = available_wm_widths[available_wm_widths > target_width * ratio]
        out_width = target_width * ratio if len(avails)==0 else avails[0]
    else:
        avails = available_wm_widths[available_wm_widths < target_width * ratio]
        out_width = target_width * ratio if len(avails)==0 else avails[::-1][0]
    
    if out_width > target_width and use_larger:        
        return _determine_width_(target_width, ratio, use_larger = False)
    else:
        return out_width    

def add_watermarks():
    """Adds watermarks to all subplots of the current figure"""
    fig = plt.gcf()
    for ax in fig.axes:
        add_watermark(ax, target='axis')

def add_watermark(ax, target='axis', loc='lower left'):
    """Add watermark to current axis or figure

    Args:
        ax (:obj:`str`): Axis object (not relevant if target=='figure')
        target (:obj:`str`): Draw axis for the whole 'figure' (default) or 'axis'
        loc (:obj:`str`): Location of the watermark ('upper right'|'upper left'|'lower left'|'lower right'|'center left'|'center right'|'lower center'|'upper center'|'center').
            Default value is 'center' when target=='figure' and 'lower left' for target=='axis'
    """
    file_name = str(Path(__file__).parent) + '\\lclogo.png'
    img = Image.open(file_name)
    
    if target == 'axis':
        fig = ax.get_figure()
        bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width = bbox.width * fig.dpi
        
        wm_width = int(_determine_width_(width, wm_min_ratio_axis))                       # make watermark larger than given ratio
        scaling = (wm_width / float(img.size[0]))
        wm_height = int(float(img.size[1])*float(scaling))
        img = img.resize((wm_width, wm_height), Image.ANTIALIAS)
    
        imagebox = OffsetImage(img, zoom=1, alpha=wm_alpha)
        imagebox.image.axes = ax
    
        ao = AnchoredOffsetbox(loc, pad=0.5, borderpad=0, child=imagebox)
        ao.patch.set_alpha(0)
        ax.add_artist(ao)
    if target == 'figure':
        fig = plt.gcf()
        bbox = fig.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        width, height = ax.figure.get_size_inches() * fig.dpi
        
        wm_width = int(_determine_width_(width, wm_min_ratio_figure, use_larger=True))    # make watermark smaller than given ratio
        scaling = (wm_width / float(img.size[0]))
        wm_height = int(float(img.size[1])*float(scaling))
        
        img = img.resize((wm_width, wm_height), Image.ANTIALIAS)
        
#        if loc == 'center':
        logo_pos = [(fig.bbox.xmax - wm_width)/2, (fig.bbox.ymax - wm_height)/2]

        
        fig.figimage(img, logo_pos[0], logo_pos[1], alpha=wm_alpha)