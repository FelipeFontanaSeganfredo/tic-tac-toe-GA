from individuo import Individuo
from tabuleiro import Tabuleiro
import random

class Jogo:
    def __init__(self, gene1: Individuo, gene2: Individuo, tabuleiro: Tabuleiro):
        self.gene1 = gene1
        self.gene2 = gene2
        self.tabuleiro = tabuleiro
        self.jogador_atual = random.choice([1, 2])  # começa aleatório
        self.jogadas_restantes = tabuleiro.linhas * tabuleiro.colunas

    def posicao_para_linha_coluna(self, posicao: int):
        """Converte índice linear em (linha, coluna)."""
        linha = posicao // self.tabuleiro.colunas
        coluna = posicao % self.tabuleiro.colunas
        return linha, coluna

    def jogar(self):
        """Executa o jogo até alguém vencer ou não restarem jogadas.
           Retorna 0 para empate, 1 se gene1 venceu, 2 se gene2 venceu.
        """
        idx1, idx2 = 0, 0 
        while self.jogadas_restantes > 0:
            if self.jogador_atual == 1:
                jogador, genes, simbolo, idx = self.gene1, self.gene1.genes, "X", idx1
            else:
                jogador, genes, simbolo, idx = self.gene2, self.gene2.genes, "O", idx2

            while idx < len(genes):
                linha, coluna = self.posicao_para_linha_coluna(genes[idx])
                if self.tabuleiro.tabuleiro[linha][coluna] == " ":
                    self.tabuleiro.tabuleiro[linha][coluna] = simbolo
                    self.jogadas_restantes -= 1
                    if self.verificar_vitoria(simbolo):
                        self.atualizar_fitness(self.jogador_atual)
                        #self.tabuleiro.exibir_tabuleiro()
                        return self.jogador_atual
                    break
                idx += 1

            # atualiza ponteiro
            if self.jogador_atual == 1:
                idx1 = idx + 1
                self.jogador_atual = 2
            else:
                idx2 = idx + 1
                self.jogador_atual = 1

        #self.tabuleiro.exibir_tabuleiro()
        return 0

    def verificar_vitoria(self, simbolo: str) -> bool:
        """Verifica linhas, colunas e diagonais."""
        t = self.tabuleiro.tabuleiro
        n = self.tabuleiro.linhas

        # linhas e colunas
        for i in range(n):
            if all(t[i][j] == simbolo for j in range(n)):  # linha
                return True
            if all(t[j][i] == simbolo for j in range(n)):  # coluna
                return True

        # diagonais
        if all(t[i][i] == simbolo for i in range(n)):
            return True
        if all(t[i][n - 1 - i] == simbolo for i in range(n)):
            return True

        return False

    def atualizar_fitness(self, vencedor: int):
        """Atualiza o fitness dos indivíduos conforme o resultado do jogo."""
        """""
        if vencedor == 1:
            self.gene1.fitness +=1
            self.gene2.fitness -=1
        if vencedor == 2:
            self.gene2.fitness +=1
            self.gene1.fitness -=1
        """
        if vencedor == 1:
            self.gene1.fitness += 2
            self.gene2.fitness -= 0
        elif vencedor == 2:
            self.gene2.fitness += 2
            self.gene1.fitness -= 0
        else:
            self.gene1.fitness += 1
            self.gene2.fitness += 1