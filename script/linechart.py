''' A weather chart for three cities using a csv file.
This illustration demonstrates different interpretation of the same data
with the distribution option.
.. note::
    This example needs the Scipy and Pandas package to run. See
    ``README.md`` for more information.
'''
import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select, Panel
from bokeh.models.widgets import CheckboxGroup
from bokeh.palettes import Blues4
from bokeh.plotting import figure

def line_chart(covid):

    def get_dataset(src, option, cb_act):
        df = src.set_index('Date')
        
        df = df[df['Country'] == option]
        if 0 in cb_act : df['value1'] = df['Confirmed'].to_list() 
        else : df['value1'] = None
        if 1 in cb_act : df['value2'] = df['Recovered'].to_list() 
        else : df['value2'] = None
        if 2 in cb_act : df['value3'] = df['Deaths'].to_list() 
        else : df['value3'] = None

        # df['value'] = src[option].to_list()
        return ColumnDataSource(data=df)

    def make_plot(source, title):
        plot = figure(x_axis_type="datetime", width=1200, height=600)
        plot.line(x='Date', y='value1', source=source, color='red', legend_label="Confirmed")
        plot.line(x='Date', y='value2', source=source, color='blue', legend_label="Recovered")
        plot.line(x='Date', y='value3', source=source, color='black', legend_label="Deaths")

        # fixed attributes
        plot.title.text = title
        plot.xaxis.axis_label = None
        plot.yaxis.axis_label = f"{title}"
        plot.axis.axis_label_text_font_style = "bold"

        return plot

    def update_plot(attrname, old, new):
        col = col_select.value
        cb_act = cbs_selection.active
        plot.title.text = f"{col}"
        
        src = get_dataset(df, col, cb_act)
        source.data.update(src.data)

    default_option = 'Confirmed'
    default_cb = None

    df = covid.copy()
    # df = pd.read_csv(join(dirname(__file__), 'data/countries-aggregated.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df.dropna(inplace=True)


    options = list(df.Country.unique())
    cbs = ['Confirmed', 'Recovered', 'Deaths']

    col_select = Select(value=default_option, title='Country', options=options)
    cbs_selection = CheckboxGroup(labels=cbs, active=[0, 1, 2])

    source = get_dataset(df, 'Afghanistan', [0, 1, 2])
    plot = make_plot(source, f"{default_option}")

    col_select.on_change('value', update_plot)
    cbs_selection.on_change('active', update_plot)

    controls = column(col_select, cbs_selection)

    # curdoc().add_root(row(plot, controls))
    # curdoc().title = "Weather"

    layout = row(controls, plot)

    tab = Panel(child = layout , title = 'Summary Table')

    return tab