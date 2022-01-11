import datetime
from os.path import dirname, join

import pandas as pd
from scipy.signal import savgol_filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, DataRange1d, Select, Panel, LabelSet
from bokeh.models.widgets import CheckboxGroup
from bokeh.palettes import Blues4
from bokeh.plotting import figure

# STATISTICS = ['record_min_temp', 'actual_min_temp', 'average_min_temp', 'average_max_temp', 'actual_max_temp', 'record_max_temp']
def bar_chart(covid):
    def get_dataset(src, option):
        df = src.set_index('Date')
        
        df = df[df['Country'] == option].max()

        # df['value'] = src[option].to_list()
        yo = {
            'country' : [df.Country],
            'confirmed' : [df.Confirmed],
            'recovered' : [df.Recovered],
            'deaths' : [df.Deaths]
        }
        return ColumnDataSource(data=dict(x=['confirmed', 'recovered', 'deaths'], top=[[df.Confirmed], [df.Recovered], [df.Deaths]]))

    def make_plot(source, title) :
        # s = source.data
        # stats = list(s.keys())[1:]
        # counts = list(s.values())[1:]
        plot = figure(x_range=source.data['x'], height=250, title=f"{title}", toolbar_location=None, tools="")

        plot.vbar(x='x', top='top', source=source, width=0.9, name='pmbar')


        return plot

    def update_plot(attrname, old, new):
        col = col_select.value
        plot.title.text = f"{col}"
        
        src = get_dataset(df, col)
        source.data.update(src.data)
       
    default_option = 'Afghanistan'

    df = covid.copy()
    # df = pd.read_csv(join(dirname(__file__), 'data/countries-aggregated.csv'))
    df['Date'] = pd.to_datetime(df['Date'])
    df.dropna(inplace=True)


    options = list(df.Country.unique())

    col_select = Select(value=default_option, title='Country', options=options)

    source = get_dataset(df, 'Afghanistan')
    plot = make_plot(source, f"{default_option}")

    col_select.on_change('value', update_plot)

    controls = column(col_select)

    # curdoc().add_root(row(plot, controls))
    # curdoc().title = "Weather"

    layout = row(controls, plot)

    tab = Panel(child = layout , title = 'Total Status Covid')

    return tab