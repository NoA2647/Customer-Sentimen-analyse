from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.palettes import Turbo256, Spectral7
from bokeh.plotting import figure
from bokeh.models.layouts import Column
import matplotlib.pyplot as plt


def chart(positive_reviews, negative_reviews):
    output_file("results.html")
    negative_reviews = dict(sorted(negative_reviews.items(), key=lambda item: item[1]))
    positive_reviews = dict(sorted(positive_reviews.items(), key=lambda item: item[1], reverse=True))

    positive_sum = sum(list(positive_reviews.values()))
    negative_sum = sum(list(negative_reviews.values()))

    positive_aspects = list(positive_reviews.keys())
    negative_aspects = list(negative_reviews.keys())

    positive_frequencies = list(positive_reviews.values())
    negative_frequencies = list(negative_reviews.values())

    positive_percentages = [(freq / positive_sum) * 100 for freq in positive_frequencies]
    negative_percentages = [(abs(freq) / abs(negative_sum)) * 100 for freq in negative_frequencies]

    color = Spectral7 + Turbo256

    p_source = ColumnDataSource(data=dict(positive_aspects=positive_aspects, positive_percentages=positive_percentages,
                                          color=color[0:len(positive_aspects)]))
    positive = figure(x_range=positive_aspects, plot_height=325, plot_width=len(positive_aspects) * 100,
                      title='Positive Aspects', toolbar_location=None, tools="")
    positive.vbar(x='positive_aspects', top='positive_percentages', color='color', legend_field="positive_aspects",
                  width=0.9, source=p_source)

    n_source = ColumnDataSource(data=dict(negative_aspects=negative_aspects,
                                          negative_percentages=[abs(value) for value in negative_percentages],
                                          color=color[0:len(negative_aspects)]))
    negative = figure(x_range=negative_aspects, plot_height=325, plot_width=len(negative_aspects) * 100,
                      title='Negative Aspects', toolbar_location=None, tools="")
    negative.vbar(x='negative_aspects', top='negative_percentages', color='color', legend_field="negative_aspects",
                  width=0.9, source=n_source)

    positive.xgrid.grid_line_color = None
    positive.y_range.start = 0
    positive.legend.orientation = "horizontal"
    positive.legend.location = "top_center"

    negative.xgrid.grid_line_color = None
    negative.y_range.start = 0
    negative.legend.orientation = "horizontal"
    negative.legend.location = "top_center"

    p = Column(positive, negative)

    show(p)

