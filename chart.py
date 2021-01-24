from bokeh.io import output_file, show
from bokeh.plotting import figure


def chart(reviews, total_rate, status):
    aspects = []
    frequencies = []
    title = ""

    if status == -1:
        title = 'Negative Aspects'
        output_file("negative_aspects.html")
        reviews = dict(sorted(reviews.items(), key=lambda item: item[1]))
    if status == 1:
        title = 'Positive Aspects'
        output_file("positive_aspects.html")
        reviews = dict(sorted(reviews.items(), key=lambda item: item[1], reverse=True))

    for review in reviews:
        aspects.append(review)
        frequencies.append(abs(reviews[review])/total_rate*100)

    p = figure(x_range=aspects, plot_height=500, plot_width=len(aspects) * 100,
               title=title, toolbar_location=None, tools="")

    p.vbar(x=aspects, top=frequencies, width=0.9)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    show(p)
