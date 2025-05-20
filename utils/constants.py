import os

MIN_NOTA = 350
MAX_NOTA = 700
NUMBER_OF_COLORS = 10
NUMBER_OF_STEPS = 8

COLOR_ESTADO = "#E63946"
COLOR_MUNICIPIO = "#2A9D8F"
COLOR_BRASIL = "#1D3557"
LOADING_COLOR = "#4694C7"

MAPBOX_STYLE = "mapbox://styles/ficast/cmaqktc0d01o301qo7c994rgz"
MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")
MAPBOX_ZOOM = 3.5
MAPBOX_CENTER = {"lat": -14, "lon": -52}

FAIXAS_RENDA = {
    "A": "Até 1 SM",
    "B": "De 1 a 3 SM",
    "C": "De 3 a 6 SM",
    "D": "De 6 a 10 SM",
    "E": "De 10 a 20 SM",
    "F": "Mais de 20 SM",
    # "G": "Não informado"
}

MAPPING_COR_RACA_LABEL = {
    # 0: "Não declarado",
    1: "Branca",
    2: "Preta",
    3: "Parda",
    4: "Amarela",
    5: "Indígena"
}

MAPPING_TP_ESCOLA_LABEL = {
    0: "Não informado",
    1: "Pública",
    2: "Privada",
}
