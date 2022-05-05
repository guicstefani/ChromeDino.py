import pygame 
import os
import random
import sys

pygame.init()#iniciamos o pygame

#definimos altura e largura da tela
TELA_ALTURA = 600
TELA_LARGURA = 1100
TELA = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))

#aqui carregaremos todas as imagens do jogo da pasta Imagens
CORRENDO = [pygame.image.load(os.path.join("Imagens/Dino", "DinoCorre1.png")),
           pygame.image.load(os.path.join("Imagens/Dino", "DinoCorre2.png"))]
PULANDO = pygame.image.load(os.path.join("Imagens/Dino", "DinoPula.png"))
AGACHANDO = [pygame.image.load(os.path.join("Imagens/Dino", "DinoAgachado1.png")),
           pygame.image.load(os.path.join("Imagens/Dino", "DinoAgachado2.png"))]

CACTUS_PEQUENO = [pygame.image.load(os.path.join("Imagens/Cactus", "CactusPequeno1.png")),
                pygame.image.load(os.path.join("Imagens/Cactus", "CactusPequeno2.png")),
                pygame.image.load(os.path.join("Imagens/Cactus", "CactusPequeno3.png"))]
CACTUS_GRANDE = [pygame.image.load(os.path.join("Imagens/Cactus", "CactusGrande1.png")),
                pygame.image.load(os.path.join("Imagens/Cactus", "CactusGrande2.png")),
                pygame.image.load(os.path.join("Imagens/Cactus", "CactusGrande3.png"))]

PASSARO = [pygame.image.load(os.path.join("Imagens/Passaro", "Passaro1.png")),
        pygame.image.load(os.path.join("Imagens/Passaro", "Passaro2.png"))]

NUVEM = pygame.image.load(os.path.join("Imagens/Outros", "Nuvem.png"))

PF = pygame.image.load(os.path.join("Imagens/Outros", "Chao.png"))


class Dinossauro:
    X_POS = 80 #x e y define a posicao fixa do dino
    Y_POS = 310
    Y_POS_AGACHADO = 340 # aqui a posicao do dino agachado
    PULA_VEL = 8.5  #velocidade pulo

#metodo init: iclui todas as imagens do dino
    def __init__(self):
        self.agacha_img = AGACHANDO
        self.corre_img = CORRENDO
        self.pula_img = PULANDO

        self.dino_agacha = False
        self.dino_corre = True #aqui deixamos apenas correndo como verdade pq o dino começa assim.
        self.dino_pula = False

        self.passo_indice = 0 #para fazer a animação do dino
        self.pula_vel = self.PULA_VEL #velocidade q o dino salta do chao
        self.image = self.corre_img[0] #inicializar a 1º imagem
        self.dino_rect = self.image.get_rect() #vai ser a área de contato do dino, para quando ele tocar nos obstáculos o jogo sinalizar
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def atualizar(self, inputUsuario):
        if self.dino_agacha:
            self.agacha() #cria-se uma função diferente para cada ação o dino
        if self.dino_corre:
            self.corre()
        if self.dino_pula:
            self.pula()

        if self.passo_indice >= 10:
            self.passo_indice = 0 #a cada 10 passos é resetado para facilicar a animação do dino

    #esses if/elif ajudam a descobrir o estado do dino, tradzuindo o 1º if, se apertamos a seta pra cima e o dino não estiver pulando então...
        if inputUsuario[pygame.K_UP] and not self.dino_pula:
            self.dino_agacha = False
            self.dino_corre = False
            self.dino_rect.y = self.Y_POS #isso aqui é necesário pro dino não pular infinitamente pra cima, se quiser entender na prática teste sem o comando.
            self.dino_pula = True #...ativamos o comando do dino pular colocando ele como verdade
        elif inputUsuario[pygame.K_DOWN] and not self.dino_pula:
            self.dino_agacha = True #seta pra abaixo faz com que o dino agache
            self.dino_corre = False
            self.dino_pula = False
        elif not (self.dino_pula or inputUsuario[pygame.K_DOWN]):
            self.dino_agacha = False
            self.dino_corre = True  #se não tiver nem pulando nem agachado, dino continua correndo
            self.dino_pula = False

    def agacha(self):
        self.image = self.agacha_img[self.passo_indice // 5] #a variável de passo faz alternar entre as 2 imagens do dino correndo para parecer que ele está animado
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_AGACHADO
        self.passo_indice += 1

    def corre(self):
        self.image = self.corre_img[self.passo_indice // 5] 
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.passo_indice += 1

    def pula(self):
        self.image = self.pula_img
        if self.dino_pula:
            self.dino_rect.y -= self.pula_vel * 4
            self.pula_vel -= 0.8
        if self.pula_vel < - self.PULA_VEL:
            self.dino_pula = False
            self.pula_vel = self.PULA_VEL

    def desenhar(self, TELA):
        TELA.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Nuvem:
    def __init__(self):
        self.x = TELA_LARGURA + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = NUVEM
        self.largura = self.image.get_width()

    def atualizar(self):
        self.x -= jogo_velocidade
        if self.x < -self.largura:
            self.x = TELA_LARGURA + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def desenhar(self, TELA):
        TELA.blit(self.image, (self.x, self.y))


class Obstaculo:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = TELA_LARGURA

    def atualizar(self):
        self.rect.x -= jogo_velocidade
        if self.rect.x < -self.rect.width:
            obstaculos.pop() #remove o obstáculo assim que ele sai da tela

    def desenhar(self, TELA):
        TELA.blit(self.image[self.type], self.rect)


class CactusPequeno(Obstaculo):
    def __init__(self, image):
        self.type = random.randint(0, 2) # aqui vai escolher aleatoriamente entre os 3 tipos de cactus
        super().__init__(image, self.type)
        self.rect.y = 325


class CactusGrande(Obstaculo):
    def __init__(self, image):
        self.type = random.randint(0, 2) # aqui vai escolher aleatoriamente entre os 3 tipos de cactu
        super().__init__(image, self.type)
        self.rect.y = 300


class Passaro(Obstaculo):
    def __init__(self, image):
        self.type = 0 #aqui so alterna pra entre imagem 1 e 2 pra parecer que o passaro está animado
        super().__init__(image, self.type)
        self.rect.y = 250
        self.indice = 0

    def desenhar(self, TELA):
        if self.indice >= 9:
            self.indice = 0
        TELA.blit(self.image[self.indice//5], self.rect) #isso faz com que o passaro aparente ser animado
        self.indice += 1


def main():
    global jogo_velocidade, x_pos_pf, y_pos_pf, pontos, obstaculos
    rodando = True
    clock = pygame.time.Clock()
    jogador = Dinossauro()
    nuvem = Nuvem()
    jogo_velocidade = 20
    x_pos_pf = 0
    y_pos_pf = 380
    pontos = 0
    font = pygame.font.Font('freesansbold.ttf', 20) #aqui a fonte usada para os textos do jogo
    obstaculos = []
    morte_contador = 0

    def placar():
        global pontos, jogo_velocidade
        pontos += 1
        if pontos % 100 == 0:
            jogo_velocidade += 1

        texto = font.render("Points: " + str(pontos), True, (0, 0, 0))
        textoRect = texto.get_rect()
        textoRect.center = (1000, 40)
        TELA.blit(texto, textoRect)

    def planoDeFundo():
        global x_pos_pf, y_pos_pf
        image_largura = PF.get_width()
        TELA.blit(PF, (x_pos_pf, y_pos_pf))
        TELA.blit(PF, (image_largura + x_pos_pf, y_pos_pf))
        if x_pos_pf <= -image_largura:
            TELA.blit(PF, (image_largura + x_pos_pf, y_pos_pf))
            x_pos_pf = 0
        x_pos_pf -= jogo_velocidade

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False #aqui colocamos se o jogador clicar no "x" ele fecha o jogo enquanto está rodando
                pygame.quit()
                quit()
                sys.exit()

        TELA.fill((255, 255, 255))
        inputUsuario = pygame.key.get_pressed()

        jogador.desenhar(TELA)
        jogador.atualizar(inputUsuario)

        if len(obstaculos) == 0:
            if random.randint(0, 2) == 0:
                obstaculos.append(CactusPequeno(CACTUS_PEQUENO))  #nessa parte é escolhido aleatoriamente o tipo de obstáculo que vai aparecer
            elif random.randint(0, 2) == 1:
                obstaculos.append(CactusGrande(CACTUS_GRANDE))
            elif random.randint(0, 2) == 2:
                obstaculos.append(Passaro(PASSARO))

        for obstaculo in obstaculos:
            obstaculo.desenhar(TELA)
            obstaculo.atualizar()
            if jogador.dino_rect.colliderect(obstaculo.rect):
                pygame.time.delay(1500)
                morte_contador += 1
                menu(morte_contador)

        planoDeFundo()

        nuvem.desenhar(TELA)
        nuvem.atualizar()

        placar()

        clock.tick(30)
        pygame.display.update()


def menu(morte_contador):
    global pontos
    rodando = True
    while rodando:
        TELA.fill((255, 255, 255)) #cor do fundo do jogo, será branco
        font = pygame.font.Font('freesansbold.ttf', 30)

        if morte_contador == 0:
            texto = font.render("Pressione qualquer tecla para começar :)", True, (0, 0, 0)) #  esse aqui como é 0,0,0 a cor será preta
        elif morte_contador > 0:
            texto = font.render("Pressione qualquer tecla para recomeçar :P", True, (0, 0, 0))
            placar = font.render("Seu Placar: " + str(pontos), True, (0, 0, 0))
            placarRect = placar.get_rect()
            placarRect.center = (TELA_LARGURA // 2, TELA_ALTURA // 2 + 50)
            TELA.blit(placar, placarRect)
        textoRect = texto.get_rect()
        textoRect.center = (TELA_LARGURA // 2, TELA_ALTURA // 2)
        TELA.blit(texto, textoRect)
        TELA.blit(CORRENDO[0], (TELA_LARGURA // 2 - 20, TELA_ALTURA // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False #aqui colocamos se o jogador clicar no "x" ele fecha o jogo na tela de menu
                pygame.quit()
                quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()


menu(morte_contador=0)