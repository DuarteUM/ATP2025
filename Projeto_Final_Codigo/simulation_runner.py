from clinic import simula
from config import (
    NUM_MEDICOS_DEFAULT,
    TAXA_CHEGADA_DEFAULT,
    TEMPO_MEDIO_CONSULTA_DEFAULT,
    TEMPO_SIMULACAO_DEFAULT,
    DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT,
)

def run_single_simulation():
    stats, _ = simula(
        num_medicos=NUM_MEDICOS_DEFAULT,
        taxa_chegada=TAXA_CHEGADA_DEFAULT,
        tempo_medio_consulta=TEMPO_MEDIO_CONSULTA_DEFAULT,
        tempo_simulacao=TEMPO_SIMULACAO_DEFAULT,
        dist_tempo_consulta=DISTRIBUICAO_TEMPO_CONSULTA_DEFAULT,
        debug=False,
    )

    print("=== Resultados da simulação ===")
    print(f"Doentes atendidos: {stats['doentes_atendidos']:.0f}")
    print(f"Tempo médio de espera (min): {stats['tempo_medio_espera']:.2f}")
    print(f"Tempo médio de consulta (min): {stats['tempo_medio_consulta']:.2f}")
    print(f"Tempo médio total na clínica (min): {stats['tempo_medio_total_clinica']:.2f}")
    print(f"Tamanho médio da fila: {stats['tamanho_medio_fila']:.2f}")
    print(f"Tamanho máximo da fila: {stats['tamanho_max_fila']}")
    print("Ocupação dos médicos:")
    for i, occ in enumerate(stats["ocupacao_medicos"]):
        print(f"  Médico m{i}: {occ*100:.1f}%")

if __name__ == "__main__":
    run_single_simulation()
