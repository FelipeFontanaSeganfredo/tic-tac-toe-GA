import random
from individuo import Individuo

class Crossover:
    def __init__(self):
        pass

    def fazer_crossover(self, gene1: Individuo, gene2: Individuo):
        corte = random.randint(1, 8)
        influencia_gene1 = gene1.genes[:corte]
        influencia_gene2 = [gene for gene in gene2.genes if gene not in influencia_gene1]
        novo_gene = Individuo(gene1.tabuleiro, genes=influencia_gene1 + influencia_gene2)
        return novo_gene