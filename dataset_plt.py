
import pandas as pd
import matplotlib.pyplot as plt
from bokeh.io import output_notebook, show
output_notebook()
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.sampledata.autompg import autompg_clean as df
from bokeh.transform import factor_cmap

class DatasetPlot:

    def __init__(self, dataset):
        self.dataset = dataset
    # methods
    def getDataset(self):
        return self.dataset

    def plot_dataset(self):
        def label_function(val):
            return f'{val / 100 * len(self.dataset):.0f}\n{val:.0f}%'

        self.dataset.hist(figsize=(30,10), grid=True, layout=(3, 3), bins = 20, column=["distance","surge_multiplier","price"])

        fig, axs = plt.subplots(1,3,figsize=(32,6))
        axs = axs.ravel()

        self.dataset.groupby("cab_type").size().plot(kind="pie", autopct=label_function, textprops={'fontsize': 12}, colors=['gold', 'skyblue'], ax=axs[0])
        self.dataset.groupby("name").size().plot(kind="pie", autopct=label_function, textprops={'fontsize': 12}, ax=axs[1])
        self.dataset.plot(kind="scatter", x="distance", y="price", ax=axs[2])

        axs[0].set_title("Plot showing the Cab Types")
        axs[1].set_title("Plot showing the ")
        axs[2].set_title("Plot showing no missing data after using the filling technique")

    def bokeh_plot(self):
        group = self.dataset.groupby("name")
        source = ColumnDataSource(group)

        p = figure(plot_width=800, plot_height=300, title="Mean MPG by # Cylinders and Manufacturer",
                x_range=group, toolbar_location=None, tools="")

        p.xgrid.grid_line_color = None
        p.xaxis.axis_label = "Manufacturer grouped by # Cylinders"
        p.xaxis.major_label_orientation = 1.2

        # index_cmap = factor_cmap('cyl_mfr', palette=['#2b83ba', '#abdda4', '#ffffbf', '#fdae61', '#d7191c'], 
        #                          factors=sorted(df.cyl.unique()), end=1)

        p.vbar(x='name', top='distance_std', width=1, source=source,
            line_color="white", 
            hover_line_color="darkgrey")

        # p.add_tools(HoverTool(tooltips=[("MPG", "@mpg_mean"), ("Cyl, Mfr", "@cyl_mfr")]))

        show(p)