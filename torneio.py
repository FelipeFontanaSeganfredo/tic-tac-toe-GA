import random
from jogo import Jogo
from individuo import Individuo
from tabuleiro import Tabuleiro
from crossover import Crossover
from copy import deepcopy

class Torneio:
    def __init__(self, populacao, tabuleiro: Tabuleiro, taxa_mutacao=0.05, elitismo=True):
        self.populacao = populacao
        self.tabuleiro = tabuleiro
        self.crossover = Crossover()
        self.taxa_mutacao = taxa_mutacao
        self.elitismo = elitismo

    @staticmethod
    def competir(ind1: Individuo, ind2: Individuo, tabuleiro: Tabuleiro):
        """
        Simula uma partida de jogo da velha entre dois indivíduos.
        Retorna o vencedor (ind1, ind2) ou None se empate.
        """
        tab_temp = deepcopy(tabuleiro)  # tabuleiro limpo
        jogo = Jogo(ind1, ind2, tab_temp)
        resultado = jogo.jogar()  # 1 = ind1 venceu, 2 = ind2 venceu, 0 = empate

        if resultado == 1:
            return ind1
        elif resultado == 2:
            return ind2
        else:
            return None

    def jogar_rodada(self, ind1: Individuo, ind2: Individuo):
        """
        Executa uma rodada e atualiza fitness do vencedor.
        """
        vencedor = Torneio.competir(ind1, ind2, self.tabuleiro)
        if vencedor == ind1:
            ind1.fitness += 1
            ind2.fitness -= 1
        elif vencedor == ind2:
            ind2.fitness += 1
            ind1.fitness -= 1
        # empate = não altera fitness
        return vencedor

    def avaliar_populacao(self, n_partidas=5):
        """Cada indivíduo joga várias vezes contra adversários aleatórios."""
        for individuo in self.populacao:
            for _ in range(n_partidas):
                adversario = random.choice(self.populacao)
                if adversario != individuo:
                    self.jogar_rodada(individuo, adversario)

    def selecionar_pais(self, k=5):
        """Seleciona dois pais via torneio de tamanho k."""
        candidatos = random.sample(self.populacao, k)
        pai1 = max(candidatos, key=lambda ind: ind.fitness)
        candidatos = random.sample(self.populacao, k)
        pai2 = max(candidatos, key=lambda ind: ind.fitness)
        return pai1, pai2

    def mutar(self, individuo: Individuo):
        """Aplica mutação trocando dois genes de posição."""
        if random.random() < self.taxa_mutacao:
            i, j = random.sample(range(len(individuo.genes)), 2)
            individuo.genes[i], individuo.genes[j] = individuo.genes[j], individuo.genes[i]

    def nova_geracao(self, tamanho_populacao):
        """Cria nova geração via crossover + mutação + elitismo."""
        nova_pop = []

        # Elitismo: mantém o melhor indivíduo da geração atual
        if self.elitismo:
            melhor = max(self.populacao, key=lambda ind: ind.fitness)
            clone = Individuo(melhor.tabuleiro)
            clone.genes = melhor.genes[:]  # copia genes
            clone.fitness = melhor.fitness
            nova_pop.append(clone)

        # Preenche o resto da população
        while len(nova_pop) < tamanho_populacao:
            pai1, pai2 = self.selecionar_pais()
            filho = self.crossover.fazer_crossover(pai1, pai2)
            self.mutar(filho)  # aplica mutação
            nova_pop.append(filho)

        return nova_pop
