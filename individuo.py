import random
from tabuleiro import Tabuleiro

class Individuo:
    def __init__(self, tabuleiro: Tabuleiro, genes=None):
        self.tabuleiro = tabuleiro
        self.fitness = 0
        if genes is None:
            self.gerar_genes()
        else:
            self.genes = genes

    def gerar_genes(self):
        tabuleiro_size = self.tabuleiro.linhas * self.tabuleiro.colunas
        self.genes = random.sample(range(tabuleiro_size), tabuleiro_size)