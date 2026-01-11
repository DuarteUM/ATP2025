import numpy as np
import json
import os

# Constantes
CHEGADA = "chegada"
SAIDA = "saída"

# --- Funções de Suporte ---
def e_tempo(e): return e[0]
def e_tipo(e): return e[1]
def e_doente(e): return e[2]

def procuraPosQueue(q, t):
    i = 0
    while i < len(q) and t > q[i][0]: i += 1
    return i

def enqueue(q, e):
    pos = procuraPosQueue(q, e[0])
    return q[:pos] + [e] + q[pos:]

def dequeue(q):
    return q[0], q[1:]

def mOcupa(m):
    m[1] = not m[1]
    return m

def gera_proxima_chegada_poisson(taxa_lmbda):
    return np.random.exponential(1.0 / taxa_lmbda)

def gera_tempo_consulta(mean_service_time, dist):
    if dist == "exponential": return np.random.exponential(mean_service_time)
    elif dist == "normal": return max(1, np.random.normal(mean_service_time, mean_service_time / 3))
    return mean_service_time

# --- Função Principal ---
def simula(num_medicos, taxa_chegada, tempo_medio_consulta, tempo_simulacao, dist_tempo_consulta="exponential", caminho_json="pessoas (1).json", debug=False):
    
    # Carregar JSON com verificação de erro
    if os.path.exists(caminho_json):
        with open(caminho_json, 'r', encoding='utf-8') as f:
            lista_pessoas = json.load(f)
    else:
        print(f"AVISO: Ficheiro {caminho_json} não encontrado! A usar nomes genéricos.")
        lista_pessoas = [{"nome": f"Doente_{i}", "idade": 30, "sexo": "M"} for i in range(1000)]

    tempo_atual = 0.0
    contadorDoentes = 0
    queueEventos = []
    queue = []
    
    # Médico: [id, ocupado, doente_corrente, total_tempo_ocupado, inicio_consulta]
    medicos = [[f"m{i}", False, None, 0.0, 0.0] for i in range(num_medicos)]
    
    chegadas = {}
    tempos_espera, tempos_consulta, tempos_total_clinica = [], [], []
    timeline_tempo, timeline_fila, timeline_ocupa = [], [], []

    # Gerar chegadas (Poisson)
    t_chegada = gera_proxima_chegada_poisson(taxa_chegada)
    while t_chegada < tempo_simulacao and contadorDoentes < len(lista_pessoas):
        nome = lista_pessoas[contadorDoentes]['nome']
        chegadas[nome] = t_chegada
        queueEventos = enqueue(queueEventos, (t_chegada, CHEGADA, nome))
        t_chegada += gera_proxima_chegada_poisson(taxa_chegada)
        contadorDoentes += 1

    # Ciclo de Simulação
    while queueEventos:
        evento, queueEventos = dequeue(queueEventos)
        tempo_atual, tipo, doente = evento

        # Logs para gráficos
        ocs = sum(1 for m in medicos if m[1])
        timeline_tempo.append(tempo_atual); timeline_fila.append(len(queue)); timeline_ocupa.append(ocs/num_medicos)

        if tipo == CHEGADA:
            medico_livre = next((m for m in medicos if not m[1]), None)
            if medico_livre:
                medico_livre[1] = True; medico_livre[2] = doente; medico_livre[4] = tempo_atual
                tempos_espera.append(tempo_atual - chegadas[doente])
                t_cons = gera_tempo_consulta(tempo_medio_consulta, dist_tempo_consulta)
                tempos_consulta.append(t_cons)
                queueEventos = enqueue(queueEventos, (tempo_atual + t_cons, SAIDA, doente))
            else:
                queue.append((doente, tempo_atual))

        elif tipo == SAIDA:
            for m in medicos:
                if m[2] == doente:
                    m[3] += (tempo_atual - m[4]); m[1] = False; m[2] = None
                    tempos_total_clinica.append(tempo_atual - chegadas[doente])
                    if queue:
                        prox_nome, _ = queue.pop(0)
                        m[1] = True; m[2] = prox_nome; m[4] = tempo_atual
                        tempos_espera.append(tempo_atual - chegadas[prox_nome])
                        t_cons = gera_tempo_consulta(tempo_medio_consulta, dist_tempo_consulta)
                        tempos_consulta.append(t_cons)
                        queueEventos = enqueue(queueEventos, (tempo_atual + t_cons, SAIDA, prox_nome))
                    break

    stats = {
        "doentes_atendidos": len(tempos_total_clinica),
        "tempo_medio_espera": np.mean(tempos_espera) if tempos_espera else 0,
        "tempo_medio_consulta": np.mean(tempos_consulta) if tempos_consulta else 0,
        "tempo_medio_total_clinica": np.mean(tempos_total_clinica) if tempos_total_clinica else 0,
        "tamanho_medio_fila": np.mean(timeline_fila) if timeline_fila else 0,
        "tamanho_max_fila": max(timeline_fila) if timeline_fila else 0,
        "ocupacao_medicos": [m[3] / tempo_simulacao for m in medicos]
    }
    return stats, {"tempo": timeline_tempo, "tamanho_fila": timeline_fila, "ocupacao_medicos": timeline_ocupa}
