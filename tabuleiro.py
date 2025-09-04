class Tabuleiro:
    def __init__(self, linhas=3, colunas=3):
        self.linhas = linhas
        self.colunas = colunas
        self.tabuleiro = self.inicializar_tabuleiro()

    def inicializar_tabuleiro(self):
        tabuleiro = []
        for i in range(self.linhas):
            linha = []
            for j in range(self.colunas):
                linha.append(' ')
            tabuleiro.append(linha)
        return tabuleiro

    def exibir_tabuleiro(self):
        for linha in self.tabuleiro:
            print('|'.join(linha))
            print('-' * (self.colunas * 2 - 1))
