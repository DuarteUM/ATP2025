import FreeSimpleGUI as sg

from clinic import simula
from config import (
    NUM_MEDICOS_DEFAULT,
    TAXA_CHEGADA_DEFAULT,
    TEMPO_MEDIO_CONSULTA_DEFAULT,
    TEMPO_SIMULACAO_DEFAULT,
    DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT,
)

# -------------------------------
# Valores iniciais
# -------------------------------
num_medicos = NUM_MEDICOS_DEFAULT
taxa_chegada_hora = 10.0
tempo_medio_consulta = TEMPO_MEDIO_CONSULTA_DEFAULT
tempo_simulacao = TEMPO_SIMULACAO_DEFAULT
dist_consulta = DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT


def formata_resultados(stats):
    linhas = []
    linhas.append(f"Doentes atendidos: {stats['doentes_atendidos']:.0f}")
    linhas.append(f"Tempo médio de espera (min): {stats['tempo_medio_espera']:.2f}")
    linhas.append(f"Tempo médio de consulta (min): {stats['tempo_medio_consulta']:.2f}")
    linhas.append(f"Tempo médio na clínica (min): {stats['tempo_medio_total_clinica']:.2f}")
    linhas.append(f"Tamanho médio da fila: {stats['tamanho_medio_fila']:.2f}")
    linhas.append(f"Tamanho máximo da fila: {stats['tamanho_max_fila']}")
    linhas.append("Ocupação dos médicos:")
    for i, occ in enumerate(stats["ocupacao_medicos"]):
        linhas.append(f"  Médico m{i}: {occ*100:.1f}%")
    return "\n".join(linhas)


# -------------------------------
# Layout da interface
# -------------------------------
layout = [
    [sg.Text("Parâmetros da simulação", font=("Arial", 12, "bold"))],

    [sg.Text("Número de médicos:", size=(25, 1)),
     sg.Input(str(num_medicos), key="-MEDICOS-")],

    [sg.Text("Taxa de chegada (doentes/hora):", size=(25, 1)),
     sg.Input(str(taxa_chegada_hora), key="-TAXA-")],

    [sg.Text("Tempo médio de consulta (min):", size=(25, 1)),
     sg.Input(str(tempo_medio_consulta), key="-CONSULTA-")],

    [sg.Text("Tempo total de simulação (min):", size=(25, 1)),
     sg.Input(str(tempo_simulacao), key="-SIMULACAO-")],

    [sg.Text("Distribuição do tempo de consulta:")],
    [
        sg.Radio("Exponencial", "DIST", key="-EXP-", default=(dist_consulta=="exponential")),
        sg.Radio("Normal", "DIST", key="-NORM-", default=(dist_consulta=="normal")),
        sg.Radio("Uniforme", "DIST", key="-UNIF-", default=(dist_consulta=="uniform")),
    ],

    [sg.Button("Executar simulação", key="-RUN-", size=(20, 1))],

    [sg.Text("Resultados:", font=("Arial", 12, "bold"))],
    [sg.Multiline("Resultados aparecerão aqui.",
                  size=(70, 15),
                  key="-OUT-",
                  disabled=True)],
]

window = sg.Window("Simulação Clínica Médica", layout)


# -------------------------------
# Loop principal
# -------------------------------
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        break

    if event == "-RUN-":
        try:
            num_medicos = int(values["-MEDICOS-"])
            taxa_chegada_hora = float(values["-TAXA-"])
            tempo_medio_consulta = float(values["-CONSULTA-"])
            tempo_simulacao = float(values["-SIMULACAO-"])

            if values["-EXP-"]:
                dist_consulta = "exponential"
            elif values["-NORM-"]:
                dist_consulta = "normal"
            else:
                dist_consulta = "uniform"

            taxa_minuto = taxa_chegada_hora / 60.0

            stats, _ = simula(
                num_medicos=num_medicos,
                taxa_chegada=taxa_minuto,
                tempo_medio_consulta=tempo_medio_consulta,
                tempo_simulacao=tempo_simulacao,
                dist_tempo_consulta=dist_consulta,
                debug=False,
            )

            window["-OUT-"].update(formata_resultados(stats))

        except Exception as e:
            window["-OUT-"].update(f"ERRO NA SIMULAÇÃO:\n{e}")

window.close()


