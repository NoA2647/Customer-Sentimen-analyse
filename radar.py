import itertools
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from plotly.subplots import make_subplots


def beautiful_spider(positive_reviews, negative_reviews):
    negative_reviews = dict(sorted(negative_reviews.items(), key=lambda item: item[1]))
    positive_reviews = dict(sorted(positive_reviews.items(), key=lambda item: item[1], reverse=True))

    five_top_positive_reviews = dict(itertools.islice(positive_reviews.items(), 5))
    five_top_negative_reviews = dict(itertools.islice(negative_reviews.items(), 5))

    positive_sum = sum(list(positive_reviews.values()))
    negative_sum = sum(list(negative_reviews.values()))

    five_top_positive_aspects = list(five_top_positive_reviews.keys())
    five_top_negative_aspects = list(five_top_negative_reviews.keys())

    five_top_positive_frequencies = list(five_top_positive_reviews.values())
    five_top_negative_frequencies = list(five_top_negative_reviews.values())

    five_top_positive_percentages = [(freq / positive_sum) * 100 for freq in five_top_positive_frequencies]
    five_top_negative_percentages = [(abs(freq) / abs(negative_sum)) * 100 for freq in five_top_negative_frequencies]

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Five Most Frequent Positive Aspects", "Five Most Frequent Negative Aspects"),
        specs=[[{"type": "polar"}, {"type": "polar"}]]
    )

    fig = fig.add_trace(go.Scatterpolar(
        r=five_top_positive_percentages,
        theta=five_top_positive_aspects,
        fill='toself',
        name='Positive Aspects'
    ),
        row=1, col=1
    )

    fig = fig.add_trace(go.Scatterpolar(
        r=[abs(value) for value in five_top_negative_percentages],
        theta=five_top_negative_aspects,
        fill='toself',
        name='Negative Aspects'
    ),
        row=1, col=2
    )

    fig.update_layout(
        width=1000,
        height=650,
        polar=dict(
            radialaxis=dict(
                visible=True,
            ),
        ),
        showlegend=False
    )

    app = dash.Dash()
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ], style={
        'height': '75%',
        'width': '75%',
        "display": "block",
        "margin-left": "auto",
        "margin-right": "auto",
    })
    app.run_server(debug=False)
