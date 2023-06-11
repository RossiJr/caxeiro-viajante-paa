import math
import itertools
import pygame
import time
import easygui

BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (0,127,255)
VERMELHO = (255,0, 0)
CINZA = (168, 168, 168)

pygame.init()



valor_input = easygui.enterbox("Insira a carga máxima do caminhão:", title="Entrada")
try:
   carga_caminhao = int(valor_input) # Use input to define 'carga_caminhao'
except ValueError:
    easygui.msgbox("Valor inválido. O programa será encerrado.", title="Erro")
    pygame.quit()
    exit()

# Calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Calculate the fuel consumption for a given distance and number of products
def calculate_fuel_consumption(distancia, num_produtos):
    rendimento = 10 - (num_produtos * 0.5)
    return distancia / rendimento

# Calculate the truck's route
def calculate_route(lojas, carga_caminhao):
    
    rota = []
    gastoTotal = 0
    carga = 0
    destinos = []

    loja_atual = lojas[0]
    for dest in loja_atual['destination_stores']:
        destinos.append(dest)
    rota.append({'loja': loja_atual, 'carga_atual': carga})

    for loja in lojas[1:]:
        distancia = calculate_distance(loja_atual['x'], loja_atual['y'], loja['x'], loja['y'])
        gasto_combustivel = calculate_fuel_consumption(distancia, carga)

        if loja['number'] in destinos:
            # Remove stores from destination list
            destinos.remove(loja['number'])
            carga -= 1
        for dest in loja['destination_stores']:
            destinos.append(dest)
        gastoTotal += gasto_combustivel
        carga += len(loja["destination_stores"]) # Update truck load with number of current store destinations

        # Truck load exceeded the maximum capacity, so the route is invalid
        if carga >= carga_caminhao:
            break
        
        # Add next store to the route
        rota.append({'loja': loja, 'carga_atual': carga})
        # Update current store to next
        loja_atual = loja
    rota += [{'loja': lojas[0], 'carga_atual': carga}]
    gastoTotal += calculate_fuel_consumption(calculate_distance(loja_atual['x'], loja_atual['y'], lojas[0]['x'], lojas[0]['y']), carga)
    return rota, gastoTotal, carga

# Read store infos from file
lojas = []
with open("d:\\PAA\\trab2\\caxeiro2\\caxeiro-viajante-paa\\app\\src\\lojas.txt", "r") as file:
    for line in file:
        store_info = line.split()
        loja = {
            "number": int(store_info[0]),
            "x": int(store_info[1]),
            "y": int(store_info[2]),
            "destination_stores": [int(dest) for dest in store_info[3:]],
        }
        lojas.append(loja)


# Generate all permutations of destinations
tempo_inicial = (time.time()) # Start timer
destinos = lojas[1:]  # Exclui a matriz
permutacoes = list(itertools.permutations(destinos))

melhor_rota = None
melhor_gasto_combustivel = math.inf

# Calculate route and fuel cost for each permutation
for permutacao in permutacoes:
    destinos_permutados = [lojas[0]] + list(permutacao)
    rota, gasto_total, carga = calculate_route(destinos_permutados, carga_caminhao)

    if carga == 0 and gasto_total < melhor_gasto_combustivel:
        melhor_rota = rota
        melhor_gasto_combustivel = gasto_total

# Print results
gasto = 0
print("Rota do caminhão:")
for i in range(1, len(melhor_rota)):
    gasto += calculate_fuel_consumption(calculate_distance(melhor_rota[i-1]['loja']['x'], melhor_rota[i-1]['loja']['y'], 
                                                           melhor_rota[i]['loja']['x'], melhor_rota[i]['loja']['y']), melhor_rota[i-1]['carga_atual'])
    #rota = ponto['loja']
    print(f"{melhor_rota[i]['loja']['number']} {gasto:.2f}")

print("Melhor gasto de combustível:", gasto)


tempo_final = (time.time()) # End timer
print(f"{tempo_final - tempo_inicial} segundos") # Print executing time

####### FRONT-END #######

# Screen configurations
largura, altura = 800, 800   
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Força Bruta")

# Load truck image
imagem_caminhao = pygame.image.load("d:\\PAA\\trab2\\caxeiro2\\caxeiro-viajante-paa\\app\\src\\caminhao.png")
largura_caminhao = int(5 * tela.get_width() / 100)
altura_caminhao = int(5 * tela.get_height() / 100)
imagem_caminhao = pygame.transform.scale(imagem_caminhao, (largura_caminhao, altura_caminhao))

#Add delay for the route
tempo_atraso = 0.8

#Main loop
executing = True
initial_point = 0
while executing:
    for evento in pygame.event.get(): # Start front-end
        if evento.type == pygame.QUIT:
            executing = False

    tela.fill(BRANCO) # Set background color

    size = 1.8 # Chance scale

    # Draw ponits and route based on results
    for i, ponto in enumerate(melhor_rota):
        ponto = ponto['loja']

        x = ponto['x'] * size
        y = ponto['y'] * size
        
        if i < initial_point:
            if i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga_atual'] == melhor_rota[i]['carga_atual']:
                cor = VERDE
                pygame.draw.circle(tela, cor, (x, y), 10)
            elif i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga_atual'] < melhor_rota[i]['carga_atual']:
                cor = AZUL
                pygame.draw.circle(tela, cor, (x, y), 10)
            elif i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga_atual'] > melhor_rota[i]['carga_atual']:
                cor = VERMELHO
                pygame.draw.circle(tela, cor, (x, y), 10)
        else:
            cor = CINZA
            pygame.draw.circle(tela, cor, (x, y), 10)

        texto = f"Loja {ponto['number']}"  # Print store number/name
        fonte = pygame.font.Font(None, 18)
        texto_renderizado = fonte.render(texto, True, (0, 0, 0))
        tela.blit(texto_renderizado, (x, y - 20))

        if initial_point > 0 :
            pygame.draw.lines(tela, VERDE, False, [(ponto['loja']['x'] * size, ponto['loja']['y'] * size) for ponto in melhor_rota[:initial_point + 1]], 2) # Draw the lines


    # Update truck position based on scale
    x_caminhao = melhor_rota[initial_point]['loja']['x'] * size
    y_caminhao = melhor_rota[initial_point]['loja']['y'] * size

    caminhao_rect = imagem_caminhao.get_rect(center=(x_caminhao, y_caminhao))
    tela.blit(imagem_caminhao, caminhao_rect) # Show truck

    # Update initial point 
    initial_point += 1
    if initial_point >= len(melhor_rota):
        initial_point = 0

    pygame.display.flip()
    time.sleep(tempo_atraso)


pygame.quit() # Close front-end