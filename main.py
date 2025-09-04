import random
import os
import concurrent.futures
from tabuleiro import Tabuleiro
from individuo import Individuo
from crossover import Crossover
from torneio import Torneio
from copy import deepcopy

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

def carregar_populacao(caminho_arquivo, tamanho_populacao, tabuleiro):
    """
    Carrega indivíduos de um arquivo de resultados para semear a nova geração.
    Se o arquivo não existir, retorna uma lista vazia.
    """
    if not os.path.exists(caminho_arquivo):
        print(f"Aviso: Arquivo '{caminho_arquivo}' não encontrado. Iniciando com população aleatória.")
        return []

    populacao_carregada = []
    with open(caminho_arquivo, "r") as f:
        linhas = f.readlines()
        
        # Limita o número de indivíduos para não exceder o tamanho da população
        linhas_a_usar = linhas[:tamanho_populacao]

        for linha in linhas_a_usar:
            try:
                # Extrai apenas a parte dos genes da string
                genes_str = linha.split("Genes = ")[1].strip()
                # Converte a string de lista em uma lista de inteiros
                genes = [int(g) for g in genes_str[1:-1].split(',')]
                
                # Cria um novo indivíduo com os genes lidos
                novo_individuo = Individuo(tabuleiro)
                novo_individuo.genes = genes
                novo_individuo.fitness = 0  # Reseta o fitness para a nova avaliação
                populacao_carregada.append(novo_individuo)
            except Exception as e:
                print(f"Erro ao ler linha: {linha.strip()} -> {e}")
                
    return populacao_carregada

def main():
    # --- Parâmetros ---
    tamanho_populacao = 10000
    num_geracoes = 10
    taxa_mutacao = 0.04
    elitismo = True
    n_partidas = 5  # Número de partidas para avaliar o fitness de cada indivíduo
    
    # --- Inicialização ---
    tab = Tabuleiro()
    
    # Tenta carregar a população a partir de um arquivo
    populacao = carregar_populacao("resultados/resultados_finais.txt", tamanho_populacao, tab)
    
    # Se o carregamento falhar ou o arquivo estiver vazio, cria uma nova população aleatória
    if not populacao:
        populacao = [Individuo(tab) for _ in range(tamanho_populacao)]
    else:
        print(f"População inicial de {len(populacao)} indivíduos carregada com sucesso do arquivo.")
    
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
        
        # Opcional: Mostra o progresso
        melhor_individuo = max(populacao, key=lambda ind: ind.fitness)
        print(f"Geração {geracao + 1}/{num_geracoes}, Melhor Fitness: {melhor_individuo.fitness}")

    # Encontra e imprime o melhor indivíduo da última geração
    melhor_individuo_final = max(populacao, key=lambda ind: ind.fitness)
    print("\n--- Melhor Indivíduo da Última Geração ---")
    print(f"Genes: {melhor_individuo_final.genes}")
    print(f"Fitness: {melhor_individuo_final.fitness}")

    print("\nAlgoritmo concluído. Salvando resultados...")
    salvar_resultados(populacao, "resultados/resultados_finais.txt")
    print("Resultados salvos em 'resultados/resultados_finais.txt'")

if __name__ == "__main__":
    main()
