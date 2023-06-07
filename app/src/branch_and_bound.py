import math
import pygame
import time

BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (0,127,255)
VERMELHO = (255,0, 0)
CINZA = (168, 168, 168)

pygame.init()

# Calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Calculate the fuel consumption for a given distance and number of products
def calculate_fuel_consumption(distancia, num_produtos):
    rendimento = 10 - (num_produtos * 0.5)
    return distancia / rendimento

# Calculate the lower bound cost for the remaining unvisited stores
def calculate_lower_bound(lojas, carga_caminhao, visited):
    # Calcula a carga restante no caminhão subtraindo a soma dos itens na lista "visited" da capacidade do caminhão
    carga_restante = carga_caminhao - sum(visited)
    lower_bound = 0       # Amazenara o valor do limite inferior do consumo de combustivel

    for i, loja in enumerate(lojas):
        if not visited[i]:
            distancia = calculate_distance(lojas[0]['x'], lojas[0]['y'],loja['x'], loja['y']) 
            lower_bound += calculate_fuel_consumption(distancia, carga_restante)  # Se a loja atual não tiver sido visitada, o consumo de combustível é calculado chamando a função calculate_fuel_consumption.
    return lower_bound  # Limite inferior do consumo de combustivel 

# Calculate the truck's route using Branch and Bound
def calculate_route_bb(lojas, carga_caminhao):
    num_lojas = len(lojas)
    visited = [False] * num_lojas
    rota_atual = [0]
    carga_atual = 0
    gasto_atual = 0
    melhor_rota = None
    melhor_gasto_combustivel = math.inf

    def branch_and_bound(index):
        nonlocal rota_atual, carga_atual, gasto_atual, melhor_rota, melhor_gasto_combustivel

        visited[index] = True
        carga_atual += len(lojas[index]["destination_stores"])

        if carga_atual > carga_caminhao:
            visited[index] = False
            carga_atual -= len(lojas[index]["destination_stores"])
            return

        rota_atual.append(index)

        if len(rota_atual) == num_lojas:
            distancia = calculate_distance(lojas[rota_atual[-1]]['x'], lojas[rota_atual[-1]]['y'], lojas[0]['x'], lojas[0]['y'])
            gasto_combustivel = calculate_fuel_consumption(distancia, carga_atual)

            if gasto_combustivel < melhor_gasto_combustivel:
                melhor_rota = rota_atual[:]
                melhor_gasto_combustivel = gasto_combustivel

        else:
            lower_bound = calculate_lower_bound(lojas, carga_caminhao, visited)

            if gasto_atual + lower_bound < melhor_gasto_combustivel:
                for i in range(1, num_lojas):
                    if not visited[i]:
                        distancia = calculate_distance(lojas[rota_atual[-1]]['x'], lojas[rota_atual[-1]]['y'], lojas[i]['x'], lojas[i]['y'])
                        gasto_combustivel = calculate_fuel_consumption(distancia, carga_atual)

                        if gasto_atual + gasto_combustivel + lower_bound < melhor_gasto_combustivel:
                            branch_and_bound(i)

        visited[index] = False
        carga_atual -= len(lojas[index]["destination_stores"])
        rota_atual.pop()

    branch_and_bound(0)
    rota = [lojas[i] for i in melhor_rota]

    return rota, melhor_gasto_combustivel

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

# Truck parameters
carga_caminhao = 5

# Calculate route and fuel cost using Branch and Bound
melhor_rota, melhor_gasto_combustivel = calculate_route_bb(lojas, carga_caminhao)

# Print results
print("Rota do caminhão:")
for ponto in melhor_rota:
    rota = ponto['loja']
    print(rota["number"], rota['x'], rota['y'], ponto['carga_atual'])

print("Melhor gasto de combustível:", gasto_total)

####### FRONT-END #######

# Screen configurations
largura, altura = 800, 800   
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Branch and Bound")

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
        
        if i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga_atual'] == melhor_rota[i]['carga_atual']:
            cor = VERDE
            pygame.draw.circle(tela, cor, (x, y), 10)
        elif i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga_atual'] < melhor_rota[i]['carga_atual']:
            cor = AZUL
            pygame.draw.circle(tela, cor, (x, y), 10)
        elif i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga_atual'] > melhor_rota[i]['carga_atual']:
            cor = VERMELHO
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