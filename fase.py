# -*- coding: utf-8 -*-
from itertools import chain
from atores import ATIVO


VITORIA = 'VITORIA'
DERROTA = 'DERROTA'
EM_ANDAMENTO = 'EM_ANDAMENTO'


class Ponto():
    def __init__(self, x, y, caracter):
        self.caracter = caracter
        self.x = round(x)
        self.y = round(y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.caracter == other.caracter

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self, *args, **kwargs):
        return "Ponto(%s,%s,'%s')" % (self.x, self.y, self.caracter)


class Fase():
    def __init__(self, intervalo_de_colisao=1):
        """
        Método que inicializa uma fase.

        :param intervalo_de_colisao:
        """
        self.intervalo_de_colisao = intervalo_de_colisao
        self._passaros = []
        self._porcos = []
        self._obstaculos = []


    def adicionar_obstaculo(self, *obstaculos):
        self ._obstaculos.extend(obstaculos)
        
        """
        Adiciona obstáculos em uma fase

        :param obstaculos:
        """
        pass

    def adicionar_porco(self, *porcos):
        self ._porcos.extend(porcos)
        """
        Adiciona porcos em uma fase

        :param porcos:
        """
        pass

    def adicionar_passaro(self, *passaros):
        self._passaros.extend(passaros)
        """
        Adiciona pássaros em uma fase

        :param passaros:
        """
        pass

    def status(self):
        """
        Método que indica com mensagem o status do jogo

        Se o jogo está em andamento (ainda tem porco ativo e pássaro ativo), retorna essa mensagem.

        Se o jogo acabou com derrota (ainda existe porco ativo), retorna essa mensagem

        Se o jogo acabou com vitória (não existe porco ativo), retorna essa mensagem

        :return:
        """
        porco, passaro = False, False
        porco = [True for i in self._porcos if i.status == ATIVO]
        passaro = [True for i in self._passaros if i.status == ATIVO]
        if not porco:
            return VITORIA
        elif not passaro:
            return DERROTA
        return EM_ANDAMENTO


    def lancar(self, angulo, tempo):
        """
        Método que executa lógica de lançamento.

        Deve escolher o primeiro pássaro não lançado da lista e chamar seu método lançar

        Se não houver esse tipo de pássaro, não deve fazer nada

        :param angulo: ângulo de lançamento
        :param tempo: Tempo de lançamento
        """
        # [i.lancar(angulo,tempo) for i in self._passaros if i.status == ATIVO and not i.foi_lancado()]
        for i in self._passaros:
            if i.status == ATIVO and not i.foi_lancado():
                i.lancar(angulo, tempo)
                break

    def calcular_pontos(self, tempo):
        """
        Lógica que retorna os pontos a serem exibidos na tela.

        Cada ator deve ser transformado em um Ponto.

        :param tempo: tempo para o qual devem ser calculados os pontos
        :return: objeto do tipo Ponto
        """
        boo = True
        pontos = []
        # 1.0 Calcular a posição de cada passaro.
        # 1.1 Mandar Calcular a posição passando o tempo.
        for passaro in self._passaros:
            passaro.calcular_posicao(tempo)
        # 2.0 Verificar se colidiu com porcos ou obstaculo
            for ator in self._porcos + self._obstaculos:
                passaro.colidir(ator, self.intervalo_de_colisao)
                passaro.colidir_com_chao()
        # 3.0 Transformar tudo em pontos (atores, obstaculos e passaros)
        # 3.1 Passar tudo para a lista e retorna-la
        for ator in self._porcos + self._obstaculos + self._passaros:
            pontos.append(self._transformar_em_ponto(ator))
        return pontos

    def _transformar_em_ponto(self, c):
        return Ponto(c.x, c.y, c.caracter())
