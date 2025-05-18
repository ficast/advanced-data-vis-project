import os

MIN_NOTA = 350
MAX_NOTA = 700
NUMBER_OF_STEPS = 8

COLOR_RED_ESTADO = "#E63946"
COLOR_GREEN_MUNICIPIO = "#2A9D8F"
COLOR_BLUE_BRASIL = "#1D3557"

MAPBOX_STYLE = "mapbox://styles/ficast/cmaqktc0d01o301qo7c994rgz"
MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
MAPBOX_ZOOM = 3.5
MAPBOX_CENTER = {"lat": -14, "lon": -52}

FAIXAS_RENDA = {
    "A": "1 SM",
    "B": "2 a 3 SM",
    "C": "3 a 6 SM",
    "D": "6 a 10 SM",
    "E": "10 a 20 SM",
    "F": "20 a 30 SM",
    "G": "+ 30 SM"
}

CORES_PASTEL = [
    "#A3C1DA", "#F7CAC9", "#B5EAD7", "#FFDAC1",
    "#E2F0CB", "#C7CEEA", "#FFF1BA"
]