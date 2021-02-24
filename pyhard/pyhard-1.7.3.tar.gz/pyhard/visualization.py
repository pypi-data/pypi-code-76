import io
import logging
from pathlib import Path

import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn
from bokeh.models import HoverTool
from bokeh.themes.theme import Theme
from holoviews import opts, dim, streams
from holoviews.plotting.links import DataLink
from shapely.geometry import Point, Polygon, MultiPolygon
from sklearn.decomposition import PCA

from pyhard.utils import reduce_dim


dark_color = '#292929'
light_color = '#ffffff'
footprint_colors = {'good': '#58D68D', 'best': '#9B59B6', 'bad': 'yellow'}

dark_theme = Theme(
    json={
        'attrs': {
            'Figure': {
                'background_fill_color': dark_color,
                'border_fill_color': dark_color,
                'outline_line_color': '#444444',
            },
            'Title': {
                'text_color': 'white',
                'text_font_size': '14pt'
            },
            'Grid': {
                'grid_line_dash': [6, 4],
                'grid_line_alpha': .3,
            },

            'Axis': {
                'major_label_text_color': 'white',
                'axis_label_text_color': 'white',
                'major_tick_line_color': 'white',
                'minor_tick_line_color': 'white',
                'axis_line_color': "white"
            },

            'ColorBar': {
                'background_fill_color': dark_color,
                'major_label_text_color': 'white',
                'title_text_color': 'white'
            },

            'Plot': {
                'sizing_mode': 'stretch_both',
                'margin': (0, 0, 0, 0)
            }
        }
    })

light_theme = Theme(
    json={
        'attrs': {
            'Figure': {
                'background_fill_color': light_color,
                'border_fill_color': light_color,
                'outline_line_color': '#444444',
            },
            'Title': {
                'text_color': 'black',
                'text_font_size': '14pt'
            },
            'Grid': {
                'grid_line_dash': [6, 4],
                'grid_line_alpha': .9,
            },

            'Axis': {
                'major_label_text_color': 'black',
                'axis_label_text_color': 'black',
                'major_tick_line_color': 'black',
                'minor_tick_line_color': 'black',
                'axis_line_color': 'black'
            },

            'ColorBar': {
                'background_fill_color': light_color,
                'major_label_text_color': 'black',
                'title_text_color': 'black'
            },

            'Plot': {
                'sizing_mode': 'stretch_both',
                'margin': (0, 0, 0, 0)
            }
        }
    })

dark_template = f"""
{{% extends base %}}

{{% block title %}}Instance Hardness dashboard{{% endblock %}}

{{% block preamble %}}
<style>
  @import url(https://fonts.googleapis.com/css?family=Noto+Sans);
  body {{
    font-family: 'Noto Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    color: #fff;
    background: {dark_color};
  }}
</style>
{{% endblock %}}
"""

light_template = f"""
{{% extends base %}}

{{% block title %}}Instance Hardness dashboard{{% endblock %}}

{{% block preamble %}}
<style>
  @import url(https://fonts.googleapis.com/css?family=Noto+Sans);
  body {{
    font-family: 'Noto Sans', sans-serif;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
    color: #000;
    background: {light_color};
  }}
</style>
{{% endblock %}}
"""

_my_path = Path(__file__).parent


class App:
    def __init__(self, df_dataset: pd.DataFrame, df_metadata: pd.DataFrame,
                 df_is: pd.DataFrame, df_footprint: pd.DataFrame, df_foot_perf=None):
        hv.extension('bokeh')
        hv.renderer('bokeh').theme = light_theme
        self.tmpl = pn.Template(light_template)

        self.logger = logging.getLogger(__name__)
        # Temporary solution for known warnings
        logging.getLogger("param").setLevel(logging.ERROR)

        self.df_original = df_dataset
        self.df_metadata = df_metadata
        self.df_is = df_is
        self.df_footprint = df_footprint
        self.df_foot_perf = df_foot_perf

        if len(df_dataset.columns) > 3:
            X = df_dataset.iloc[:, :-1]
            y = df_dataset.iloc[:, -1]

            pca = PCA(n_components=2)
            X_embedded = pca.fit_transform(X)

            df = pd.DataFrame(X_embedded, columns=[f'Component1',  # ({(100 * pca.explained_variance_ratio_[0]):.2f}%)
                                                   f'Component2'],  # ({(100 * pca.explained_variance_ratio_[1]):.2f}%)
                              index=X.index)
            df_dataset = pd.concat([df, y], axis=1)
        self.df_dataset = df_dataset

        data = self.df_is.join(self.df_dataset)
        self.data = data.join(self.df_metadata)
        self.mlist = ['circle', 'triangle', 'square', 'diamond', 'asterisk', 'hex', '+', 'x']
        self.is_kdims = df_is.columns.to_list()[0:2]
        self.data_dims = df_dataset.columns.to_list()
        self.data_kdims = self.data_dims[0:2]
        self.class_label = self.data_dims[2]
        self.meta_dims = df_metadata.columns.to_list()

        self.w_color = pn.widgets.Select(options=self.meta_dims + [self.class_label], value=self.meta_dims[0])
        self.w_color_range = pn.widgets.RangeSlider(start=0, end=20, value=(0, 5), step=0.5)
        self.w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
        self.w_footprint_on = pn.widgets.Checkbox(name='draw footprint area', value=True)

        val = 'instance_hardness' if 'instance_hardness' in df_footprint.index else ''
        self.w_footprint_algo = pn.widgets.Select(options=df_footprint.index.unique(level='algo').to_list(), value=val)

        self.bbox = None
        self.cmap = 'coolwarm'

    @staticmethod
    def footprint2polygons(footprint: np.ndarray):
        poly_list = np.split(footprint, np.argwhere(np.isnan(footprint).any(axis=1)).flatten())
        return MultiPolygon(list(map(lambda x: Polygon(x[~np.isnan(x).any(axis=1)]), poly_list)))

    @classmethod
    def remove_intersection(cls, fp_good: np.ndarray, fp_bad: np.ndarray):
        p_good = MultiPolygon(cls.footprint2polygons(fp_good))
        p_bad = MultiPolygon(cls.footprint2polygons(fp_bad))
        p_diff_good = p_good.difference(p_bad)
        p_diff_bad = p_bad.difference(p_good)

        fp_good_clean = None
        if isinstance(p_diff_good, Polygon):
            x, y = p_diff_good.exterior.coords.xy
            fp_good_clean = np.array([x, y]).T
        else:
            for poly in p_diff_good:
                x, y = poly.exterior.coords.xy
                if fp_good_clean is None:
                    fp_good_clean = np.array([x, y]).T
                else:
                    new = np.append(np.array([[np.nan, np.nan]]), np.array([x, y]).T, axis=0)
                    fp_good_clean = np.append(fp_good_clean, new, axis=0)

        fp_bad_clean = None
        if isinstance(p_diff_bad, Polygon):
            x, y = p_diff_bad.exterior.coords.xy
            fp_bad_clean = np.array([x, y]).T
        else:
            for poly in p_diff_bad:
                x, y = poly.exterior.coords.xy
                if fp_bad_clean is None:
                    fp_bad_clean = np.array([x, y]).T
                else:
                    new = np.append(np.array([[np.nan, np.nan]]), np.array([x, y]).T, axis=0)
                    fp_bad_clean = np.append(fp_bad_clean, new, axis=0)

        return fp_good_clean, fp_bad_clean

    def footprint_area(self, algo):
        try:
            border_points_good = self.df_footprint.xs([algo, 'good']).values
        except KeyError:
            border_points_good = np.array([[0, 0]])
        # try:
        #     border_points_bad = self.df_footprint.xs([algo, 'bad']).values
        # except KeyError:
        #     border_points_bad = np.array([[0, 0]])
        try:
            border_points_best = self.df_footprint.xs([algo, 'best']).values
        except KeyError:
            border_points_best = np.array([[0, 0]])

        # if border_points_good.shape[0] > 2 and border_points_bad.shape[0] > 2:
        #     try:
        #         border_good, border_bad = self.remove_intersection(border_points_good, border_points_bad)
        #     except TopologicalError:
        #         border_good, border_bad = border_points_good, border_points_bad
        #         self.logger.warning(f"It was not possible to remove overlapping regions from the {algo} footprints. "
        #                             "Likely cause is invalidity of the geometry.")
        # else:
        #     border_good, border_bad = border_points_good, border_points_bad
        border_good, border_best = border_points_good, border_points_best

        footprint_good = hv.Polygons([border_good.tolist()], label='Good Footprint').opts(line_width=1, line_alpha=0.2,
                                                                                          line_color='black',
                                                                                          fill_color=footprint_colors[
                                                                                              'good'],
                                                                                          fill_alpha=.2,
                                                                                          show_legend=True)
        # footprint_bad = hv.Polygons([border_bad.tolist()], label='Bad').opts(line_width=1, line_alpha=0.2,
        #                                                                      line_color='black',
        #                                                                      fill_color=footprint_colors['bad'],
        #                                                                      fill_alpha=.2, show_legend=True)
        footprint_best = hv.Polygons([border_best.tolist()], label='Best Footprint').opts(line_width=1, line_alpha=0.2,
                                                                                          line_color='black',
                                                                                          fill_color=footprint_colors[
                                                                                              'best'],
                                                                                          fill_alpha=.2,
                                                                                          show_legend=True)
        return footprint_good * footprint_best  # * footprint_bad

    def select_instances(self):
        if self.bbox is None:
            return pd.DataFrame()
        x, y = list(self.bbox.keys())
        if len(self.bbox[x]) == 2:
            V1 = np.column_stack([self.bbox[x], self.bbox[y]])
            V2 = V1.copy()
            V2[0, 1], V2[1, 1] = V1[1, 1], V1[0, 1]
            V = np.array([V1[0, :], V2[0, :], V1[1, :], V2[1, :]])
            contour = list(map(tuple, V))
        else:
            contour = list(map(tuple, np.column_stack([self.bbox[x], self.bbox[y]])))
        polygon = Polygon(contour)
        mask = self.data[[x, y]].apply(lambda p: polygon.contains(Point(p[0], p[1])), raw=True, axis=1)
        return self.df_original[mask]

    def data_space(self, c, lim, autorange_on):
        if not autorange_on:
            lim = (np.nan, np.nan)
        cmap = self.cmap
        # hover_list = [c] + hover_list
        # tooltips = [(s, '@' + s) for s in hover_list]
        # hover = HoverTool(tooltips=tooltips)
        scatter1 = hv.Scatter(self.data, kdims=self.data_kdims, vdims=[self.class_label] + self.meta_dims
                              ).opts(responsive=True, aspect=1.2, color=c,
                                     cmap=cmap, show_grid=True,
                                     marker=dim(self.class_label).categorize(self.mlist),
                                     tools=['lasso_select', 'box_select', 'hover'],
                                     size=6, framewise=True, colorbar=True, clim=lim)
        return scatter1

    def instance_space(self, c, lim, autorange_on):
        if not autorange_on:
            lim = (np.nan, np.nan)
        cmap = self.cmap
        # hover_list = [c] + hover_list
        # tooltips = [(s, '@' + s) for s in hover_list]
        # hover = HoverTool(tooltips=tooltips)
        scatter2 = hv.Scatter(self.data, kdims=self.is_kdims, vdims=[self.class_label] + self.meta_dims
                              ).opts(responsive=True, aspect=1.2, color=c,
                                     cmap=cmap, show_grid=True,
                                     marker=dim(self.class_label).categorize(self.mlist),
                                     tools=['lasso_select', 'box_select', 'hover'],
                                     size=6, framewise=True, colorbar=True, clim=lim)
        return scatter2

    def get_pane(self):
        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value)
        def update_plot1(color, lim, autorange_on):
            return self.data_space(color, lim, autorange_on)

        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value)
        def update_plot2(color, lim, autorange_on):
            return self.instance_space(color, lim, autorange_on)

        def selection_callback1(bbox, region_element, selection_expr, resetting):
            self.bbox = bbox
            # button.button_type = 'default'
            # if bbox is not None:
            #     button.disabled = False
            if resetting:
                self.bbox = None
                # button.disabled = True
            return hv.Polygons([[[0, 0]]])

        @pn.depends(footprint=self.w_footprint_algo.param.value, fp_on=self.w_footprint_on.param.value)
        def selection_callback2(bbox, region_element, selection_expr, footprint, fp_on):
            self.bbox = bbox
            # button.button_type = 'default'
            # if bbox is not None:
            #     button.disabled = False
            if fp_on:
                return self.footprint_area(footprint)
            else:
                return (hv.Polygons([[[0, 0]]], label='Good Footprint').opts(fill_color=footprint_colors['good']) *
                        hv.Polygons([[[0, 0]]], label='Best Footprint').opts(fill_color=footprint_colors['best']))
                # hv.Polygons([[[0, 0]]], label='Bad').opts(fill_color=footprint_colors['bad']) * \

        dmap1 = hv.DynamicMap(update_plot1)
        dmap2 = hv.DynamicMap(update_plot2)
        dmap1.opts(title='Principal Components')
        dmap2.opts(title='Instance Space')

        selection1 = hv.streams.SelectionExpr(source=dmap1)
        reset = hv.streams.PlotReset()
        sel1_dmap = hv.DynamicMap(selection_callback1, streams=[selection1, reset])

        selection2 = hv.streams.SelectionExpr(source=dmap2)
        sel2_dmap = hv.DynamicMap(selection_callback2, streams=[selection2])

        def file_cb():
            df = self.select_instances()
            sio = io.StringIO()
            df.to_csv(sio)
            sio.seek(0)
            return sio

        button = pn.widgets.FileDownload(embed=False, auto=True, callback=file_cb,
                                         filename='selection.csv',
                                         label='Save selected points',
                                         button_type='primary')

        layout = (dmap1 * sel1_dmap + dmap2 * sel2_dmap).cols(2).opts(
            opts.Layout(shared_axes=False, shared_datasource=True, framewise=True),
            opts.Polygons(show_legend=True, legend_position='bottom'))

        gspec = pn.GridSpec(sizing_mode='stretch_both', background=light_color, margin=0)
        gspec[0, 0] = pn.Column('## Color', self.w_color, '### Color Bar', self.w_checkbox, self.w_color_range,
                                pn.Row(pn.Spacer(), height=20),
                                '## Footprint', self.w_footprint_on, self.w_footprint_algo,
                                pn.Row(pn.Spacer(), height=20),
                                '## Selection', button,
                                background=light_color)
        gspec[0, 1:5] = layout
        tabs = pn.Tabs(('PyHard', gspec))
        tabs.append(('Footprint performance', pn.widgets.DataFrame(self.df_foot_perf, name='DataFrame',
                                                                   disabled=True, sizing_mode='stretch_both')))
        return tabs

    def show(self, **kwargs):
        tabs = self.get_pane()
        self.tmpl.add_panel(name='IS', panel=tabs)
        self.tmpl.servable()
        self.tmpl.show(title="Instance Hardness", **kwargs)


def app(df_dataset: pd.DataFrame, df_metadata: pd.DataFrame, df_is: pd.DataFrame, df_footprint: pd.DataFrame):
    hv.extension('bokeh')
    hv.renderer('bokeh').theme = dark_theme
    tmpl = pn.Template(dark_template)

    if len(df_dataset.columns) > 3:
        X = df_dataset.iloc[:, :-1]
        y = df_dataset.iloc[:, -1]
        X_embedded = reduce_dim(X, y)
        df = pd.DataFrame(X_embedded, columns=['V1', 'V2'], index=X.index)
        df_dataset = pd.concat([df, y], axis=1)

    data = df_is.join(df_dataset)
    data = data.join(df_metadata)
    mlist = ['circle', 'triangle', 'square', 'diamond', '+', 'x']
    is_kdims = df_is.columns.to_list()[0:2]
    data_dims = df_dataset.columns.to_list()
    data_kdims = data_dims[0:2]
    class_label = data_dims[2]
    meta_dims = df_metadata.columns.to_list()

    # data['class'] = data['class'].apply(lambda x: mlist[x])
    def footprint_area(algo):
        points_good = df_footprint.xs([algo, 'good']).values.tolist()
        points_bad = df_footprint.xs([algo, 'bad']).values.tolist()
        footprint_good = hv.Polygons([points_good], label='Good').opts(line_width=1, line_alpha=0.2, line_color='black',
                                                                       fill_color='white', fill_alpha=.2,
                                                                       show_legend=True)
        footprint_bad = hv.Polygons([points_bad], label='Bad').opts(line_width=1, line_alpha=0.2, line_color='black',
                                                                    fill_color='orange', fill_alpha=.2,
                                                                    show_legend=True)
        return footprint_good * footprint_bad

    def plotter(c, lim, autorange_on, hover_list, footprint_selected, fp_on, **kwargs):
        if not autorange_on:
            lim = (np.nan, np.nan)
        cmap = 'Blues_r'
        scatter1 = hv.Scatter(data, kdims=data_kdims, vdims=[class_label, c] + meta_dims,
                              label='Original Data').opts(responsive=True, aspect=1.2, color=c,
                                                          cmap=cmap, show_grid=True,
                                                          marker=dim(class_label).categorize(mlist))

        scatter = hv.Scatter(data, kdims=is_kdims,
                             vdims=[class_label, c] + meta_dims).opts(responsive=True,
                                                                      aspect=1.2, color=c,
                                                                      cmap=cmap, show_grid=True,
                                                                      marker=dim(class_label).categorize(mlist))
        if fp_on:
            area = footprint_area(footprint_selected)
        else:
            area = hv.Polygons([[[0, 0]]], label='Good').opts(show_legend=True) * \
                   hv.Polygons([[[0, 0]]], label='Bad').opts(show_legend=True)
            # scatter2 = hv.Scatter(data, kdims=is_kdims, vdims=[class_label, c] + meta_dims,
            #                       label='Instance Space').opts(responsive=True, aspect=1.2, color=c,
            #                                                    cmap=cmap, show_grid=True,
            #                                                    marker=dim(class_label).categorize(mlist))
        scatter2 = (scatter * area).relabel('Instance Space')

        hover_list = [c] + hover_list
        tooltips = [(s, '@' + s) for s in hover_list]
        hover = HoverTool(tooltips=tooltips)

        dlink = DataLink(scatter1, scatter2)

        return (scatter1 + scatter2).cols(2).opts(opts.Scatter(tools=['box_select', 'lasso_select', hover],
                                                               size=4, framewise=True, colorbar=True, clim=lim),
                                                  opts.Layout(shared_axes=True, shared_datasource=True,
                                                              framewise=True))

    w_color = pn.widgets.Select(options=meta_dims + [class_label], value='')
    w_color_range = pn.widgets.IntRangeSlider(start=-40, end=40, value=(0, 30), step=1)
    w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
    w_selector_hover = pn.widgets.MultiChoice(value=data_dims + is_kdims,
                                              options=data.columns.to_list())
    w_footprint_on = pn.widgets.Checkbox(name='draw footprint area', value=False)
    w_footprint_algo = pn.widgets.Select(options=df_footprint.index.unique(level='algo').to_list(), value='')

    @pn.depends(color=w_color.param.value, lim=w_color_range.param.value, autorange_on=w_checkbox.param.value,
                hover_list=w_selector_hover.param.value, footprint=w_footprint_algo.param.value,
                fp_on=w_footprint_on.param.value)
    def update_plot(color, lim, autorange_on, hover_list, footprint, fp_on, **kwargs):
        return plotter(color, lim, autorange_on, hover_list, footprint, fp_on)

    dmap = hv.DynamicMap(update_plot)

    # row = pn.Row(pn.Column(pn.WidgetBox('## Color', w_color,
    #                                     '### Color Bar', w_checkbox, w_color_range,
    #                                     height=200, width=250, sizing_mode='scale_both'),
    #                        sizing_mode='scale_both'), dmap, sizing_mode='scale_both')  # pn.layout.HSpacer()
    # pane = pn.Column(row, '## Hover Info', w_selector_hover)
    # pane.show(title="Instance Hardness")

    md_color = '<span style="color:#292929">{0}</span>'
    gspec = pn.GridSpec(sizing_mode='stretch_both', background='#292929', margin=0)
    # gspec[0, 0:5] = pn.pane.Markdown('# Instance Hardness analysis app', style={'color': '#1A76FF'})
    gspec[0:10, 0] = pn.Column('## Color', w_color,  # md_color.format('Color')
                               '### Color Bar', w_checkbox, w_color_range,  # '### ' + , w_checkbox, w_color_range,
                               pn.Row(pn.Spacer(), height=20),
                               '## Footprint', w_footprint_on, w_footprint_algo,
                               background='#292929')  # pn.Row(pn.Spacer(), height=20)
    gspec[0:10, 1:5] = dmap
    # gspec[10, 0:4] = pn.Row('## Hover options', w_selector_hover)
    tmpl.add_panel(name='A', panel=gspec)
    tmpl.servable()
    tmpl.show(title="Instance Hardness")
    # gspec.show(title="Instance Hardness")


class Demo:
    def __init__(self, datadir=None):
        hv.extension('bokeh', logo=False)

        if datadir is None:
            self.datadir = _my_path / 'data'
        else:
            self.datadir = Path(datadir)

        self.list_dir = [x.name for x in self.datadir.glob('**/*') if x.is_dir()]
        self.list_dir.sort()

        self.w_dir = pn.widgets.Select(options=self.list_dir, value='overlap')
        self.w_color = pn.widgets.Select(options=[], value='')
        self.w_color_range = pn.widgets.IntRangeSlider(start=-40, end=40, value=(-20, 20), step=1)
        self.w_checkbox = pn.widgets.Checkbox(name='manual colorbar range', value=False)
        self.w_selector_hover = pn.widgets.MultiChoice(value=[], options=[])
        self.w_dim = pn.widgets.RadioButtonGroup(options=['LDA', 'NCA', 'PCA'], value='LDA', button_type='default')

        self.mlist = ['circle', 'triangle', 'square', 'diamond', '+', 'x']
        self.df_data = self.df_metadata = self.df_feat_proc = self.df_is = None
        self.is_kdims = self.data_dims = self.data_kdims = self.class_label = self.meta_dims = []
        self.folder = None

        self.load_data(self.w_dir.value)
        self.update_components()

    def load_data(self, path, dim_method='LDA'):
        if path != self.folder:
            self.folder = path
            path = self.datadir / path
            dataset = pd.read_csv(path / 'data.csv')

            if len(dataset.columns) > 3:
                X = dataset.iloc[:, :-1]
                y = dataset.iloc[:, -1]
                X_embedded = reduce_dim(X, y, method=dim_method)
                df = pd.DataFrame(X_embedded, columns=['V1', 'V2'], index=X.index)
                dataset = pd.concat([df, y], axis=1)

            self.df_metadata = pd.read_csv(path / 'metadata.csv', index_col='instances')
            self.df_is = pd.read_csv(path / 'coordinates.csv', index_col='Row')
            self.df_is.index.name = 'instances'

            dataset.index = self.df_metadata.index
            self.df_data = self.df_is.join(dataset)
            self.df_data = self.df_data.join(self.df_metadata)

            # TODO: organizar kdims e vdims
            self.is_kdims = self.df_is.columns.to_list()[0:2]
            self.data_dims = dataset.columns.to_list()
            self.data_kdims = self.data_dims[0:2]
            self.class_label = self.data_dims[2]
            self.meta_dims = self.df_metadata.columns.to_list()

    def get_ranges(self):
        r = list()
        a = 1.1
        r.append((self.df_data[self.data_kdims[0]].min() * a, self.df_data[self.data_kdims[0]].max() * a))
        r.append((self.df_data[self.data_kdims[1]].min() * a, self.df_data[self.data_kdims[1]].max() * a))
        r.append((self.df_data[self.is_kdims[0]].min() * a, self.df_data[self.is_kdims[0]].max() * a))
        r.append((self.df_data[self.is_kdims[1]].min() * a, self.df_data[self.is_kdims[1]].max() * a))
        return r

    def plotter(self, c, lim, autorange_on, hover_list, **kwargs):
        if not autorange_on:
            lim = (np.nan, np.nan)
        # cmap = 'RdYlBu_r'
        # if c == self.class_label:
        #     cmap = 'Set1'
        # else:
        #     cmap = 'jet'
        cmap = 'coolwarm'

        hover_list = [c] + hover_list if c not in hover_list else hover_list
        tooltips = [('index', '$index')] + [(s, '@' + s) for s in hover_list]
        hover = HoverTool(tooltips=tooltips)

        r = self.get_ranges()

        scatter1_vdims = [self.data_kdims[1], self.class_label] + self.meta_dims + self.is_kdims
        scatter1 = hv.Scatter(self.df_data, kdims=self.data_kdims[0], vdims=scatter1_vdims,
                              label='Original Data').opts(color=c,  # width=490, height=440
                                                          cmap=cmap, show_grid=True,
                                                          marker=dim(self.class_label).categorize(self.mlist),
                                                          xlim=r[0], ylim=r[1], responsive=True, aspect=1.2)

        scatter2_vdims = [self.is_kdims[1], self.class_label] + self.meta_dims + self.data_kdims
        scatter2 = hv.Scatter(self.df_data, kdims=self.is_kdims[0], vdims=scatter2_vdims,
                              label='Instance Space').opts(color=c,
                                                           cmap=cmap, show_grid=True,
                                                           marker=dim(self.class_label).categorize(self.mlist),
                                                           xlim=r[2], ylim=r[3], responsive=True, aspect=1.2)

        # dlink = DataLink(scatter1, scatter2)

        return (scatter1 + scatter2).opts(opts.Scatter(tools=['box_select', 'lasso_select', 'tap', hover],
                                                       size=4, colorbar=True, clim=lim, framewise=True),
                                          opts.Layout(shared_axes=False, shared_datasource=True)).cols(2)

    def update_components(self):
        self.w_color.options = self.meta_dims + [self.class_label]
        self.w_selector_hover.options = self.df_data.columns.to_list()
        self.w_selector_hover.value = self.data_dims + self.is_kdims

    def display(self):
        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value, hover_list=self.w_selector_hover.param.value,
                    folder=self.w_dir.param.value, method=self.w_dim.param.value)
        def update_plot(color, lim, autorange_on, hover_list, folder, method, **kwargs):
            self.load_data(folder, method)
            self.update_components()
            return self.plotter(color, lim, autorange_on, hover_list)

        dmap = hv.DynamicMap(update_plot)

        # row = pn.Row(pn.Column(pn.WidgetBox('## Dataset', self.w_dir,
        #                                     '### Dimensionality Reduction', self.w_dim,
        #                                     width=250, ), # height=200
        #                        pn.WidgetBox('## Color', self.w_color,
        #                                     '### Color Bar', self.w_checkbox, self.w_color_range,
        #                                     width=250, ),
        #                        ), dmap, sizing_mode='stretch_width')  # pn.layout.HSpacer()
        # pane = pn.Column(row, '## Hover Info', self.w_selector_hover, sizing_mode='stretch_width', height=200)

        md_color = '<span style="color:#292929">{0}</span>'
        # blue #1A76FF

        gspec = pn.GridSpec(sizing_mode='stretch_both')
        # gspec[0, 0:5] = pn.pane.Markdown('# Instance Hardness dashboard demo', style={'color': '#1A76FF'})
        # gspec[0, 4] = pn.pane.JPG(str(_my_path.parent / 'docs/img/ita_rgb.jpg'), width=100)
        gspec[0:3, 0] = pn.WidgetBox('## Dataset', self.w_dir,
                                     '### Dimensionality Reduction', self.w_dim,
                                     pn.Row(pn.Spacer(), height=20))
        gspec[3:7, 0] = pn.WidgetBox('## Color', self.w_color,
                                     '### Color Bar', self.w_checkbox,
                                     self.w_color_range,
                                     pn.Row(pn.Spacer(), height=20))
        gspec[0:7, 1:5] = dmap

        return gspec  # pane

    def display_notebook(self):
        @pn.depends(color=self.w_color.param.value, lim=self.w_color_range.param.value,
                    autorange_on=self.w_checkbox.param.value, hover_list=self.w_selector_hover.param.value,
                    folder=self.w_dir.param.value, method=self.w_dim.param.value)
        def update_plot(color, lim, autorange_on, hover_list, folder, method, **kwargs):
            self.load_data(folder, method)
            self.update_components()
            return self.plotter(color, lim, autorange_on, hover_list)

        dmap = hv.DynamicMap(update_plot)

        gspec = pn.GridSpec(sizing_mode='stretch_both', max_height=800)
        gspec[0, 0:2] = pn.WidgetBox('## Dataset', self.w_dir,
                                     '### Dimensionality Reduction', self.w_dim)
        gspec[0, 2:] = pn.WidgetBox('## Color', self.w_color,
                                    '### Color Bar', self.w_checkbox, self.w_color_range)
        gspec[1:4, :4] = dmap

        return gspec


if __name__ == "__main__":
    demo = Demo()
    fig = demo.display()
    # fig.servable()
    # fig.show(port=5006, allow_websocket_origin=["localhost:5000"])
    pn.serve(fig.get_root(), port=5006, websocket_origin=["localhost:5000", "127.0.0.1:5000"], show=False)
