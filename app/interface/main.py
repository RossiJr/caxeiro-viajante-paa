### Integrantes do grupo:
###  - Joana Moreira Rezende Woldaynsky
###  - José Fernando Rossi Junior
###  - Thayris Gabriela Ferreira Rodrigues



import pygame
#COLORS SET
BRANCO = (255, 255, 255)
CINZA = (200, 200, 200)

pygame.init()

# SCREEN CONFIG
largura, altura = 400, 200
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Tela Inicial")

# BOTTONS CONFIG
largura_botao = 200
altura_botao = 50
posicao_botao1 = (int(largura * 0.3), int(altura * 0.25))
posicao_botao2 = (int(largura * 0.3), int(altura * 0.65))

# MAIN LOOP
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            posicao_mouse = pygame.mouse.get_pos()
            if posicao_botao1[0] <= posicao_mouse[0] <= posicao_botao1[0] + largura_botao \
                    and posicao_botao1[1] <= posicao_mouse[1] <= posicao_botao1[1] + altura_botao:
                import forca_bruta
            elif posicao_botao2[0] <= posicao_mouse[0] <= posicao_botao2[0] + largura_botao \
                    and posicao_botao2[1] <= posicao_mouse[1] <= posicao_botao2[1] + altura_botao:
                import branch_and_bound

    tela.fill(BRANCO)
    pygame.draw.rect(tela, CINZA, (posicao_botao1[0], posicao_botao1[1], largura_botao, altura_botao))
    texto_botao1 = pygame.font.SysFont(None, 24).render("Força Bruta", True, BRANCO)
    tela.blit(texto_botao1, (posicao_botao1[0] + 20, posicao_botao1[1] + 15))

    pygame.draw.rect(tela, CINZA, (posicao_botao2[0], posicao_botao2[1], largura_botao, altura_botao))
    texto_botao2 = pygame.font.SysFont(None, 24).render("Brach-and-Bound", True, BRANCO)
    tela.blit(texto_botao2, (posicao_botao2[0] + 20, posicao_botao2[1] + 15))

    pygame.display.flip()  #GO TO CODE

pygame.quit()