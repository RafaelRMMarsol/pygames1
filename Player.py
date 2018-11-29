import pygame
import random

class Rect(object):
    def __init__(self, numeroinicial):
        self.lista = [] #Guarda na lista cada retangulo feito
        for x in range(numeroinicial):
            esquerdaRandom = random.randrange(2, 480) #Dimençoes
            cimaRandom = random.randrange(-480, -10)#-10 Valor negativo para que nasce antes da tela
            largura = random.randrange(10, 30)
            altura = random.randrange(15, 30)
            self.lista.append(pygame.Rect(esquerdaRandom, cimaRandom, largura, altura))#add obj na lista

    def mover(self):
        for retangulo in self.lista:#movimentação dos retangulos
            retangulo.move_ip(0, 2)

    def cor(self, superficie):
        for retangulo in self.lista:
            cor_azul = (3, 28, 124)
            pygame.draw.rect(superficie, (cor_azul), retangulo)

    def recriar(self):#Para que sempre desça retangulos
        for x in range(len(self.lista)): #len captura tamanho de uma lista
            if self.lista[x].top > 481: #Assim quando top desce, ele volta em uma posição randomica
                esquerdaRandom = random.randrange(2, 480) #Dimençoes
                cimaRandom = random.randrange(-480, -10)#-10 Valor negativo para que nasce antes da tela
                largura = random.randrange(10, 30)
                altura = random.randrange(15, 30)
                self.lista[x] = (pygame.Rect(esquerdaRandom, cimaRandom, largura, altura))#lista[x] apenas para que nao lote a tela


class Player(pygame.sprite.Sprite):
    def __init__(self, imagem):
        self.imagem = imagem
        self.rect = self.imagem.get_rect()
        self.rect.top, self.rect.left = (100, 200)

    def mover(self, vx, vy):
        self.rect.move_ip(vx, vy)

    def update(self, superfice):
        superfice.blit(self.imagem, self.rect)#Atualização da tela, imagem e objeto

def colisao(player, recs):
    for rec in recs.lista:
        if player.rect.colliderect(rec):
            return True
    return False



def main():
    #Declaração dos obejetos
    import pygame
    pygame.init()
    tela = pygame.display.set_mode((480, 300))
    sair = False
    relogio = pygame.time.Clock()  # clock de atualização na tela
    cor_branca = (255, 255, 255)

    imgNave = pygame.image.load("nave.png").convert_alpha()  # Trazer Imagem e definir como Jogador
    naveImagem = pygame.transform.scale(imgNave, (50, 50))  # Alterar escala da imagem
    jogador = Player(naveImagem)

    imagem_fundo = pygame.image.load("space.png")
    imagem_explosao = pygame.image.load("explosao.png").convert_alpha()
    explosaoImagem = pygame.transform.scale(imagem_explosao, (50, 50))

    pygame.mixer.music.load("somFundo.mp3")
    pygame.mixer.music.play(3)

    som_explosao = pygame.mixer.Sound("somExplosao.ogg")

    vx, vy = 0, 0
    velocidade = 7
    esquerdaPress, direitaPress, cimaPress, baixoPress = False, False, False, False

    texto = pygame.font.SysFont("Arial", 30, True, False)#Pontos



    ret = Rect(30)
    colidiu = False

    while sair != True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Evento para fechar janela
                sair = True

            if colidiu == False:


                 if event.type == pygame.KEYDOWN: #Trata se alguma tecla esta pressionada
                    if event.key == pygame.K_LEFT:
                        esquerdaPress = True
                        vx = - velocidade
                    if event.key == pygame.K_RIGHT:
                        direitaPress = True
                        vx = velocidade
                    if event.key == pygame.K_UP:
                        cimaPress = True
                        vy = - velocidade
                    if event.key == pygame.K_DOWN:
                        baixoPress = True
                        vy = velocidade
                 if event.type == pygame.KEYUP:#Tecla solta
                    if event.key == pygame.K_LEFT:
                        esquerdaPress = False
                        if direitaPress:vx = velocidade
                        else:vx = 0
                    if event.key == pygame.K_RIGHT:
                        direitaPress = False
                        if esquerdaPress:vx = velocidade
                        else:vx = 0
                    if event.key == pygame.K_DOWN:
                         baixoPress = False
                         if cimaPress:vy = velocidade
                         else:vy = 0
                    if event.key == pygame.K_UP:
                        cimaPress = False
                        if baixoPress:vy = velocidade
                        else:vy = 0


        if colisao(jogador, ret):
            colidiu = True #se houver colisão jogador com retangulo
            jogador.imagem = explosaoImagem
            pygame.mixer.music.stop()
            som_explosao.play()


        if colidiu == False:
            ret.mover()
            jogador.mover(vx, vy)

            tela.fill((cor_branca))
            tela.blit(imagem_fundo, (0, 0))
            segundos = pygame.time.get_ticks() / 1000
            segundos = str(segundos)
            contador = texto.render(segundos, 0, cor_branca)
            tela.blit(contador, (350, 10))


#chamada
        relogio.tick(20)  # frames
        ret.cor(tela)
        ret.recriar()
        jogador.update(tela)



        pygame.display.update()

    pygame.quit()
main()