from dash import dcc, html

timeline = html.Div(
        children=[
            dcc.Graph(
                id='timeline-graph',
            config={
                "displayModeBar": False,
                "scrollZoom": False,
            },
            style={"height": "100px"}
        )
    ],
    className="timeline-card"
)