import numpy as np
import json
import random

# Constantes de Eventos
CHEGADA = "CHEGADA"
SAIDA = "SAIDA"

# Pesos de prioridade (Protocolo de Manchester)
# Quanto menor o número, maior a prioridade (0 ultrapassa todos)
PULSEIRAS = {"vermelha": 0, "laranja": 1, "amarela": 2, "verde": 3}

def carregar_base_dados_pessoas(caminho_json):
    """
    Carrega o dataset JSON fornecido com informações de doentes.
    """
    try:
        with open(caminho_json, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar ficheiro JSON: {e}")
        return []

def gera_tempo_consulta(mean_service_time, dist, idade):
    """
    Gera o tempo de duração da consulta baseado na distribuição escolhida.
    Aplica um aumento de 20% no tempo se o doente for idoso (> 65 anos).
    """
    # EXTRA: Se for idoso, o tempo médio de consulta aumenta 20%
    media_ajustada = mean_service_time * 1.2 if idade > 65 else mean_service_time
    
    if dist == "exponential": 
        return np.random.exponential(media_ajustada)
    elif dist == "normal": 
        return max(1, np.random.normal(media_ajustada, media_ajustada / 3))
    
    # Por defeito, usa distribuição uniforme
    return np.random.uniform(media_ajustada * 0.5, media_ajustada * 1.5)

def simula(num_medicos, taxa_chegada, tempo_medio_consulta, tempo_simulacao, dist_tempo_consulta, dados_pessoas):
    """
    Executa a simulação de eventos discretos da clínica.
    Gere as chegadas por Poisson e a fila por prioridade de cores.
    Calcula a satisfação baseada no tempo de espera individual.
    """
    tempo_atual = 0
    queue_eventos = []
    
    # 1. Geração de Chegadas (Distribuição de Poisson)
    while tempo_atual < tempo_simulacao:
        # O intervalo entre chegadas segue uma distribuição exponencial
        tempo_atual += np.random.exponential(60.0 / taxa_chegada)
        
        if tempo_atual < tempo_simulacao:
            # Selecionar uma pessoa aleatória do dataset JSON
            pessoa = random.choice(dados_pessoas) if dados_pessoas else {"nome": f"Doente {len(queue_eventos)}", "idade": 30, "sexo": "masculino"}
            
            # LÓGICA DE TRIAGEM (Manchester)
            hr = random.randint(40, 140)
            
            if hr < 50 or hr > 100:
                cor = "vermelha"
            else:
                # Teste dos 3 booleanos aleatórios
                testes = [random.choice([True, False]) for _ in range(3)]
                trues = sum(testes)
                
                if trues == 3:
                    cor = "vermelha"
                elif trues == 2:
                    cor = "laranja"
                elif trues == 1:
                    cor = "amarela"
                else:
                    cor = "verde"
            
            queue_eventos.append({
                'tempo': tempo_atual, 
                'tipo': CHEGADA, 
                'nome': pessoa['nome'],
                'idade': int(pessoa.get('idade', 30)),
                'sexo': pessoa.get('sexo', 'masculino').lower(),
                'cor': cor,
                'prioridade': PULSEIRAS[cor]
            })

    # Ordenar a queue inicial pelo tempo de chegada
    queue_eventos.sort(key=lambda x: x['tempo'])
    
    fila = []
    # Estado dos médicos: [id, ocupado, doente_nome, tempo_total_ocupado, inicio_atendimento_atual]
    medicos = [[i, False, None, 0.0, 0.0] for i in range(num_medicos)]
    
    stats = {
        "atendidos": 0, 
        "espera": [], 
        "timeline_fila": [], 
        "timeline_tempo": [],
        "timeline_ocupacao": [], 
        "ocupacao_media": 0,
        "idades": [], 
        "sexos": [], 
        "cores_atendidas": [],
        "satisfacao_individual": [] 
    }
    chegadas = {}

    # 2. Loop de Processamento
    while queue_eventos:
        ev = queue_eventos.pop(0)
        t_evento, tipo, doente = ev['tempo'], ev['tipo'], ev
        
        if t_evento <= tempo_simulacao:
            stats["timeline_tempo"].append(t_evento)
            stats["timeline_fila"].append(len(fila))
            ocupados = sum(1 for m in medicos if m[1])
            stats["timeline_ocupacao"].append((ocupados / num_medicos) * 100)

        if tipo == CHEGADA:
            chegadas[doente['nome']] = t_evento
            medico_livre = next((m for m in medicos if not m[1]), None)
            
            if medico_livre:
                # Médico livre: Iniciar atendimento imediato
                medico_livre[1], medico_livre[2], medico_livre[4] = True, doente['nome'], t_evento
                stats["espera"].append(0)
                stats["satisfacao_individual"].append(100) 
                stats["idades"].append(doente['idade'])
                stats["sexos"].append(doente['sexo'])
                stats["cores_atendidas"].append(doente['cor'])
                
                # Gerar tempo de consulta e agendar evento de saída
                t_cons = gera_tempo_consulta(tempo_medio_consulta, dist_tempo_consulta, doente['idade'])
                queue_eventos.append({'tempo': t_evento + t_cons, 'tipo': SAIDA, 'nome': doente['nome']})
                queue_eventos.sort(key=lambda x: x['tempo'])
            else:
                # Nenhum médico livre: Entra na fila e REORDENA por pulseira
                fila.append(doente)
                # Ordena primeiro por pulseira (0 a 3) e depois pelo tempo em que chegou
                fila.sort(key=lambda x: (x['prioridade'], x['tempo']))

        elif tipo == SAIDA:
            m = next((m for m in medicos if m[2] == doente['nome']), None)
            if m:
                # Finalizar consulta e calcular tempo de ocupação real
                fim_real = min(t_evento, tempo_simulacao)
                if fim_real > m[4]:
                    m[3] += (fim_real - m[4])
                
                m[1], m[2] = False, None
                stats["atendidos"] += 1
                
                # Se houver alguém na fila, o médico atende logo o próximo (o mais prioritário)
                if fila:
                    prox = fila.pop(0)
                    t_espera = max(0, t_evento - chegadas[prox['nome']])
                    
                    # CÁLCULO DE SATISFAÇÃO: Baseado na espera real
                    satisfacao = max(5, 100 - (max(0, t_espera - 10) * 1.5))
                    
                    m[1], m[2], m[4] = True, prox['nome'], t_evento
                    stats["espera"].append(t_espera)
                    stats["satisfacao_individual"].append(satisfacao)
                    stats["idades"].append(prox['idade'])
                    stats["sexos"].append(prox['sexo'])
                    stats["cores_atendidas"].append(prox['cor'])
                    
                    t_cons = gera_tempo_consulta(tempo_medio_consulta, dist_tempo_consulta, prox['idade'])
                    queue_eventos.append({'tempo': t_evento + t_cons, 'tipo': SAIDA, 'nome': prox['nome']})
                    queue_eventos.sort(key=lambda x: x['tempo'])

    total_trabalho = sum(m[3] for m in medicos)
    stats["ocupacao_media"] = min(100.0, (total_trabalho / (num_medicos * tempo_simulacao)) * 100)
    
    return stats, medicos