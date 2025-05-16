from dash import Output, Input
from app import app

@app.callback(
    Output('limpar-ano', 'style'),
    Input('ano-selecionado', 'children')
)
def mostrar_ou_ocultar_botao_limpar(ano_selecionado):
    if ano_selecionado and ano_selecionado.strip() != "":
        return {"display": "inline-block"}
    else:
        return {"display": "none"}