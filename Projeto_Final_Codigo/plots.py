# plots.py
import numpy as np
import matplotlib.pyplot as plt

from clinic import simula
from config import (
    NUM_MEDICOS_DEFAULT,
    TAXA_CHEGADA_DEFAULT,
    TEMPO_MEDIO_CONSULTA_DEFAULT,
    TEMPO_SIMULACAO_DEFAULT,
    DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT,
)

# ---------------------------------------------------------
# 1. Gráfico: Evolução do tamanho da fila ao longo do tempo
# ---------------------------------------------------------
def grafico_fila_tempo():
    stats, timeline = simula(
        num_medicos=NUM_MEDICOS_DEFAULT,
        taxa_chegada=TAXA_CHEGADA_DEFAULT,
        tempo_medio_consulta=TEMPO_MEDIO_CONSULTA_DEFAULT,
        tempo_simulacao=TEMPO_SIMULACAO_DEFAULT,
        dist_tempo_consulta=DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT,
        debug=False,
    )

    t = timeline["tempo"]
    fila = timeline["tamanho_fila"]

    plt.figure()
    plt.plot(t, fila, label="Tamanho da fila")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Número de doentes em espera")
    plt.title("Evolução do tamanho da fila ao longo do tempo")
    plt.legend()
    plt.grid(True)
    plt.show()

# ---------------------------------------------------------
# 2. Gráfico: Ocupação dos médicos ao longo do tempo
# ---------------------------------------------------------
def grafico_ocupacao_tempo():
    stats, timeline = simula(
        num_medicos=NUM_MEDICOS_DEFAULT,
        taxa_chegada=TAXA_CHEGADA_DEFAULT,
        tempo_medio_consulta=TEMPO_MEDIO_CONSULTA_DEFAULT,
        tempo_simulacao=TEMPO_SIMULACAO_DEFAULT,
        dist_tempo_consulta=DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT,
        debug=False,
    )

    t = timeline["tempo"]
    occ = [x * 100 for x in timeline["ocupacao_medicos"]]

    plt.figure()
    plt.plot(t, occ, label="Ocupação (%)")
    plt.xlabel("Tempo (min)")
    plt.ylabel("Ocupação dos médicos (%)")
    plt.title("Evolução da ocupação dos médicos ao longo do tempo")
    plt.legend()
    plt.grid(True)
    plt.show()

# ---------------------------------------------------------
# 3. Gráfico: Tamanho médio da fila vs taxa de chegada
# ---------------------------------------------------------
def grafico_fila_vs_taxa_chegada():
    taxas = np.arange(10, 31, 2)  # 10 a 30 doentes/hora
    tamanhos_medios = []

    for taxa_hora in taxas:
        taxa_minuto = taxa_hora / 60
        stats, _ = simula(
            num_medicos=NUM_MEDICOS_DEFAULT,
            taxa_chegada=taxa_minuto,
            tempo_medio_consulta=TEMPO_MEDIO_CONSULTA_DEFAULT,
            tempo_simulacao=TEMPO_SIMULACAO_DEFAULT,
            dist_tempo_consulta=DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT,
            debug=False,
        )
        tamanhos_medios.append(stats["tamanho_medio_fila"])

    plt.figure()
    plt.plot(taxas, tamanhos_medios, marker="o")
    plt.xlabel("Taxa de chegada de doentes (doentes/hora)")
    plt.ylabel("Tamanho médio da fila")
    plt.title("Tamanho médio da fila vs taxa de chegada")
    plt.grid(True)
    plt.show()

# ---------------------------------------------------------
# Execução direta (opcional)
# ---------------------------------------------------------
if __name__ == "__main__":
    grafico_fila_tempo()
    grafico_ocupacao_tempo()
    grafico_fila_vs_taxa_chegada()
