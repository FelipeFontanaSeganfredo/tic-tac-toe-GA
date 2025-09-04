import random
import os
import concurrent.futures
from tabuleiro import Tabuleiro
from individuo import Individuo
from crossover import Crossover
from torneio import Torneio
from copy import deepcopy
import matplotlib.pyplot as plt

def avaliar_individuo_paralelo(individuo, populacao_para_jogar, n_partidas, tabuleiro):
    """Função auxiliar para avaliar um indivíduo em paralelo."""
    tab_temp = deepcopy(tabuleiro)
    
    for _ in range(n_partidas):
        adversario = random.choice(populacao_para_jogar)
        if adversario != individuo:
            vencedor = Torneio.competir(individuo, adversario, tab_temp)
            if vencedor == individuo:
                individuo.fitness += 1
            elif vencedor == adversario:
                individuo.fitness -= 1
                
    return individuo

def salvar_resultados(individuos, caminho_arquivo="resultados.txt"):
    """Salva os genes dos indivíduos em um arquivo txt."""
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)
    with open(caminho_arquivo, "w") as f:
        for i, ind in enumerate(individuos, 1):
            f.write(f"Indivíduo {i}: Genes = {ind.genes}\n")

def simular_desempenho(individuo, num_simulacoes, tabuleiro):
    """Simula jogos do indivíduo contra oponentes aleatórios e retorna os resultados."""
    vitorias = 0
    empates = 0
    derrotas = 0
    
    for _ in range(num_simulacoes):
        adversario_aleatorio = Individuo(tabuleiro)
        vencedor = Torneio.competir(individuo, adversario_aleatorio, tabuleiro)
        
        if vencedor == individuo:
            vitorias += 1
        elif vencedor == adversario_aleatorio:
            derrotas += 1
        else:
            empates += 1
            
    return vitorias, empates, derrotas

def main():
    # --- Parâmetros ---
    tamanho_populacao = 1000
    num_geracoes = 400
    taxa_mutacao = 0.10
    elitismo = True
    n_partidas = 30
    historico_fitness = []
    
    # --- Inicialização ---
    tab = Tabuleiro()
    populacao = [Individuo(tab) for _ in range(tamanho_populacao)]
    
    torneio = Torneio(
        populacao=populacao,
        tabuleiro=tab,
        taxa_mutacao=taxa_mutacao,
        elitismo=elitismo
    )
    
    print("Iniciando o algoritmo genético...")
    
    num_threads = os.cpu_count() or 4
    
    # --- Loop de gerações ---
    for geracao in range(num_geracoes):
        # 1. Avalia a aptidão da população (paralelo)
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            resultados = executor.map(
                avaliar_individuo_paralelo,
                populacao,
                [populacao] * len(populacao),
                [n_partidas] * len(populacao),
                [tab] * len(populacao)
            )
        
        populacao = list(resultados)
        torneio.populacao = populacao
        
        # 2. Cria a nova geração usando seleção, crossover e mutação
        nova_populacao = torneio.nova_geracao(tamanho_populacao)
        
        # 3. Substitui a população antiga pela nova
        populacao = nova_populacao
        torneio.populacao = populacao
        
        # Opcional: Mostra o progresso e salva no histórico
        melhor_individuo = max(populacao, key=lambda ind: ind.fitness)
        historico_fitness.append((geracao + 1, melhor_individuo.fitness))
        print(f"Geração {geracao + 1}/{num_geracoes}, Melhor Fitness: {melhor_individuo.fitness}")

    # Encontra e imprime o melhor indivíduo da última geração
    melhor_individuo_final = max(populacao, key=lambda ind: ind.fitness)
    print("\n--- Melhor Indivíduo da Última Geração ---")
    print(f"Genes: {melhor_individuo_final.genes}")
    print(f"Fitness: {melhor_individuo_final.fitness}")

    print("\nAlgoritmo concluído. Salvando resultados...")
    salvar_resultados(populacao, "resultados/resultados_finais.txt")
    print("Resultados salvos em 'resultados/resultados_finais.txt'")

    # --- Plotagem da evolução do Fitness ---
    geracoes_plot = [item[0] for item in historico_fitness]
    fitness_plot = [item[1] for item in historico_fitness]

    plt.figure(figsize=(10, 6))
    plt.plot(geracoes_plot, fitness_plot, color='blue', linewidth=2)
    plt.title('Evolução do Melhor Fitness por Geração')
    plt.xlabel('Geração')
    plt.ylabel('Fitness')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Simulação e Plotagem de Desempenho ---
    print("\nIniciando simulação de 10000 jogos para comparação...")
    
    num_simulacoes = 10000
    
    # Simula o desempenho do melhor indivíduo do GA
    vitorias_ga, empates_ga, derrotas_ga = simular_desempenho(melhor_individuo_final, num_simulacoes, tab)
    
    # Simula o desempenho de um indivíduo aleatório
    individuo_aleatorio = Individuo(tab)
    vitorias_rand, empates_rand, derrotas_rand = simular_desempenho(individuo_aleatorio, num_simulacoes, tab)

    # Prepara os dados para o gráfico
    labels = ['Vitórias', 'Empates', 'Derrotas']
    resultados_ga = [vitorias_ga, empates_ga, derrotas_ga]
    resultados_rand = [vitorias_rand, empates_rand, derrotas_rand]

    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(12, 6))
    rects1 = ax.bar(x, resultados_ga, width, label='Algoritmo Genético', color='skyblue')
    rects2 = ax.bar([p + width for p in x], resultados_rand, width, label='Estratégia Aleatória', color='coral')

    ax.set_ylabel('Número de Jogos')
    ax.set_title('Comparação de Desempenho: GA vs. Aleatório')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.show()

    print("\n--- Resultados Finais das Simulações ---")
    print("Desempenho do Melhor Indivíduo (GA):")
    print(f"Vitórias: {vitorias_ga}, Empates: {empates_ga}, Derrotas: {derrotas_ga}")
    print("\nDesempenho de uma Estratégia Aleatória:")
    print(f"Vitórias: {vitorias_rand}, Empates: {empates_rand}, Derrotas: {derrotas_rand}")


if __name__ == "__main__":
    main()
