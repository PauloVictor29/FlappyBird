import pygame
import os
import random

# Constantes
TELA_LARGURA = 500
TELA_ALTURA = 800

# Carregar imagens
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

# Inicializar fonte e fonte de pontos
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)
FONTE_FIM_JOGO = pygame.font.SysFont('arial', 70)


# Classe Passaro
class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        self.y += deslocamento

    def desenhar(self, tela):
        self.contagem_imagem += 1
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.TEMPO_ANIMACAO * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        tela.blit(self.imagem, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


# Classe Cano
class Cano:
    DISTANCIA = 250  # Aumentar o espaço entre os canos
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if topo_ponto or base_ponto:
            return True
        else:
            return False


# Classe Chao
class Chao:
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(IMAGEM_CHAO, (self.x1, self.y))
        tela.blit(IMAGEM_CHAO, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos, fim_jogo):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    # Exibir mensagem de fim de jogo
    if fim_jogo:
        mensagem_fim = FONTE_FIM_JOGO.render("Fim de Jogo", 1, (255, 255, 255))
        tela.blit(mensagem_fim,
                  (TELA_LARGURA / 2 - mensagem_fim.get_width() / 2, TELA_ALTURA / 2 - mensagem_fim.get_height() / 2))

    # Exibir pontuação
    texto_pontos = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto_pontos, (TELA_LARGURA - 10 - texto_pontos.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    pygame.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Flappy Bird")

    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    pontos = 0
    relogio = pygame.time.Clock()
    fim_jogo = False

    rodando = True
    while rodando:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN and not fim_jogo:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        if not fim_jogo:
            for passaro in passaros:
                passaro.mover()
            chao.mover()

            adicionar_cano = False
            remover_canos = []
            for cano in canos:
                for i, passaro in enumerate(passaros):
                    if cano.colidir(passaro):
                        passaros.pop(i)
                        fim_jogo = True  # Indica que o jogo acabou
                    if not cano.passou and passaro.x > cano.x:
                        cano.passou = True
                        adicionar_cano = True
                cano.mover()
                if cano.x + cano.CANO_TOPO.get_width() < 0:
                    remover_canos.append(cano)

            if adicionar_cano:
                pontos += 1
                canos.append(Cano(600))
            for cano in remover_canos:
                canos.remove(cano)

            for i, passaro in enumerate(passaros):
                if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                    passaros.pop(i)
                    fim_jogo = True  # Indica que o jogo acabou ao cair

        desenhar_tela(tela, passaros, canos, chao, pontos, fim_jogo)

    pygame.quit()
    quit()


if __name__ == '__main__':
    main()
