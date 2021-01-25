import itertools
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html


def beautiful_spider(positive_reviews, negative_reviews, total):
    seven_top_aspects = []
    frequencies_positive = []
    frequencies_negative = []

    negative_reviews = dict(sorted(negative_reviews.items(), key=lambda item: item[1]))
    positive_reviews = dict(sorted(positive_reviews.items(), key=lambda item: item[1], reverse=True))

    four_top_positive_reviews = dict(itertools.islice(positive_reviews.items(), 4))
    three_top_negative_reviews = dict(itertools.islice(negative_reviews.items(), 3))

    print(three_top_negative_reviews)
    print(four_top_positive_reviews)

    merged_reviews = four_top_positive_reviews.copy()
    merged_reviews.update(three_top_negative_reviews)

    print(merged_reviews)

    for review in merged_reviews:
        seven_top_aspects.append(review)

    for key in seven_top_aspects:
        positive_value = positive_reviews.get(key)
        negative_value = negative_reviews.get(key)
        if positive_value is None:
            positive_value = 0
        if negative_value is None:
            negative_value = 0
        frequencies_positive.append(abs(positive_value) / total * 100)
        frequencies_negative.append(abs(negative_value) / total * 100)

    print(frequencies_negative)
    print(frequencies_positive)
    print(seven_top_aspects)

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=frequencies_positive,
        theta=seven_top_aspects,
        fill='toself',
        name='Positive'
    ))
    fig.add_trace(go.Scatterpolar(
        r=frequencies_negative,
        theta=seven_top_aspects,
        fill='toself',
        name='Negative'
    ))
    fig.update_layout(
        width=650,
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
        'height': '50%',
        'width': '50%',
        "display": "block",
        "margin-left": "auto",
        "margin-right": "auto",
    })

    app.run_server(debug=False, use_reloader=False)