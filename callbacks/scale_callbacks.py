from components.scale import criar_escala_cores
from utils.constants import MIN_NOTA, MAX_NOTA
from dash import Input, Output
from app import app

@app.callback(
    Output('scale-graph', 'figure'),
    Input('nome-estado', 'children')
)
def atualizar_escala_cores(nome_estado):
    if nome_estado and nome_estado != 'Brasil':
        return criar_escala_cores(MIN_NOTA, MAX_NOTA, cor_escala="Reds")
    else:
        return criar_escala_cores(MIN_NOTA, MAX_NOTA, cor_escala="Blues")
    