# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
# from bokeh.script.linechart import line_chart


# Each tab is drawn by one script
from script.linechart import line_chart
from script.maxtable import bar_chart

# Using included state data from Bokeh for map
# from bokeh.sampledata.us_states import data as states

# Read data into dataframes
df = pd.read_csv(join(dirname(__file__), 'data/countries-aggregated.csv'))

# Formatted Flight Delay Data for map

# Create each of the tabs
tab1 = line_chart(df)
tab2 = bar_chart(df)

# Put all the tabs into one application
tabs = Tabs(tabs = [tab1, tab2])

# Put the tabs in the current document for display
curdoc().add_root(tabs)