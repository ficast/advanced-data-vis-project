from dash import dcc, html
from components.timeline import timeline
from components.scale import Scale
from utils.map_utils import get_map_figure

fig, min_nota_rounded, max_nota_rounded = get_map_figure()

map = html.Div(
    className="map-container",
    children=[
        dcc.Graph(
            id="map-graph",
            figure=fig,
            style={"height": "100%", "width": "100%", "position": "relative"},
            config={
                "scrollZoom": True,
                "displayModeBar": False,
                "doubleClick": "reset",
            },
        ),
        Scale(min_nota_rounded, max_nota_rounded),
        timeline,
    ],
)
