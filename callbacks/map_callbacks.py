import dash
from dash import dcc, html, Input, Output
from app import app

@app.callback(
    Output('nome-estado', 'children'),
    Input('map-graph', 'selectedData')
)
def atualizar_nome_estado(selectedData):
    if not selectedData or not selectedData.get('points'):
        return "Brasil"
    estado_selecionado = selectedData['points'][0].get('text', 'Desconhecido').strip()
    return estado_selecionado