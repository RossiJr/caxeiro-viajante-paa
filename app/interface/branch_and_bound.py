### Integrantes do grupo:
###  - Joana Moreira Rezende Woldaynsky
###  - José Fernando Rossi Junior
###  - Thayris Gabriela Ferreira Rodrigues



import math
import pygame
import time
import easygui

# Colors
BRANCO = (255, 255, 255)
VERDE = (0, 255, 0)
AZUL = (0, 127, 255)
VERMELHO = (255, 0, 0)
CINZA = (168, 168, 168)

pygame.init()


valor_input = easygui.enterbox("Insira a carga máxima do caminhão:", title="Entrada")
try:
   carga_caminhao = int(valor_input) # Use input to define 'carga_caminhao'
except ValueError:
    easygui.msgbox("Valor inválido. O programa será encerrado.", title="Erro")
    pygame.quit()
    exit()

tempo_inicial = time.time()  # Start timer


# Map if i is in the destination stores of lojas and i is in the carga_restantes
def is_in_destination_stores(lojas, i, carga_restantes):
    for loja in lojas:
        if i in loja['destination_stores']:
            if i in carga_restantes:
                return True
            else:
                return False
    return True


# Calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Calculate the fuel consumption for a given distance and number of products
def calculate_fuel_consumption(distancia, num_produtos):
    rendimento = 10 - (num_produtos * 0.5)
    return distancia / rendimento


# Calculate the lower bound cost for the remaining unvisited stores
def calculate_lower_bound(lojas, carga_atual, cargas_restantes):
    lower_bound = 0
    for loja in cargas_restantes:
        gasto = calculate_fuel_consumption(calculate_distance(lojas[loja]['x'], lojas[loja]['y'], lojas[0]['x'], lojas[0]['y']),carga_atual)
        #if gasto < lower_bound:
            #lower_bound = gasto
        lower_bound += gasto
    return lower_bound


# Branch and Bound algorithm
def calculate_route_bb(lojas, carga_caminhao):
    num_lojas = len(lojas)
    visited = [False] * num_lojas
    melhor_rota = None
    melhor_gasto_combustivel = math.inf
    visited[0] = True

    # Calculate the truck's route using Branch and Bound
    def branch_and_bound(index, rota_atual, gasto_atual, carga_atual, cargas_restantes):
        nonlocal melhor_rota, melhor_gasto_combustivel

        # Mark the current store as visited
        visited[index] = True

        # If the truck load is greater than the truck capacity, the store is not visited
        if carga_atual > carga_caminhao:
            visited[index] = False
            carga_atual -= len(lojas[index]["destination_stores"])
            return

        # If the actual route is complete, check if it is the best route
        if len(rota_atual) == num_lojas:
            gasto_atual += calculate_fuel_consumption(calculate_distance(lojas[rota_atual[len(rota_atual)-1]["index_loja"]]["x"], 
                                                                         lojas[rota_atual[len(rota_atual)-1]["index_loja"]]["y"], 
                                                                         lojas[0]["x"], lojas[0]["y"]), carga_atual)
            rota_atual.append({"index_loja": 0, "carga": carga_atual, "gasto": gasto_atual})
            if gasto_atual < melhor_gasto_combustivel and len(cargas_restantes) == 0:
                melhor_rota = rota_atual[:]
                melhor_gasto_combustivel = gasto_atual
        else:
            lower_bound = calculate_lower_bound(lojas, carga_atual, cargas_restantes)

            if lower_bound < melhor_gasto_combustivel:

                # Populate the list of unvisited stores
                lojas_nao_visitadas = []
                for i in range(1, num_lojas):
                    if not visited[i] and is_in_destination_stores(lojas, i, cargas_restantes):
                        lojas_nao_visitadas.append(lojas[i])

                # Calculate the distance between the current store to the other unvisited stores and choose the best one
                for loja in lojas_nao_visitadas:
                    removed = False

                    # Visit the store making the calculations and then call the function recursively
                    nova_distancia = calculate_distance(
                        lojas[rota_atual[len(rota_atual)-1]["index_loja"]]["x"],
                        lojas[rota_atual[len(rota_atual)-1]["index_loja"]]["y"],
                        loja["x"],
                        loja["y"],
                    )
                    nova_gasto_combustivel = (
                        gasto_atual
                        + calculate_fuel_consumption(
                            nova_distancia, carga_atual
                        )
                    )
                    carga_atual += len(loja["destination_stores"])
                    cargas_restantes += loja["destination_stores"]
                    if loja["number"] in cargas_restantes:
                        cargas_restantes.remove(loja["number"])
                        carga_atual -= 1
                        removed = True
                    

                    branch_and_bound(loja["number"],
                        rota_atual + [{"index_loja": loja["number"], "carga": carga_atual, "gasto": nova_gasto_combustivel}],
                        nova_gasto_combustivel,
                        carga_atual,
                        cargas_restantes,
                    )

                    # Do the traceback if the store is not going to be visited at this moment
                    carga_atual -= len(loja["destination_stores"])
                    for i in loja["destination_stores"]:
                        cargas_restantes.remove(i)
                    if removed:
                        carga_atual += 1
                        cargas_restantes.append(loja["number"])


        visited[index] = False
        carga_atual -= len(lojas[index]["destination_stores"])

    # First call of the recursive function, starting visiting the first store
    branch_and_bound(0, [{"index_loja": 0, "carga": 0, "gasto": 0}], 0, 0, [])

    return melhor_rota, melhor_gasto_combustivel

# Read store infos from file
lojas = []
with open(".\\lojas.txt", "r") as file:
    for line in file:
        store_info = line.split()
        loja = {
            "number": int(store_info[0]),
            "x": int(store_info[1]),
            "y": int(store_info[2]),
            "destination_stores": [int(dest) for dest in store_info[3:]],
        }
        lojas.append(loja)

# Calculate route and fuel cost using Branch and Bound
melhor_rota, melhor_gasto_combustivel = calculate_route_bb(lojas, carga_caminhao)

# Print results
print("Rota do caminhão:")
for ponto in melhor_rota:
    rota = lojas[ponto['index_loja']]
    print(rota["number"], rota['x'], rota['y'])

print("Melhor gasto de combustível:", melhor_gasto_combustivel)

tempo_final = (time.time()) # End timer

print(f"{tempo_final - tempo_inicial} segundos") # Print executing time

####### FRONT-END #######

# Screen configurations
largura, altura = 800, 800   
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Branch and Bound")

# Load truck image
imagem_caminhao = pygame.image.load(".\\caminhao.png")
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
        x = lojas[ponto["index_loja"]]['x'] * size
        y = lojas[ponto["index_loja"]]['y'] * size
        
        if i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga'] == melhor_rota[i]['carga']:
            cor = VERDE
            pygame.draw.circle(tela, cor, (x, y), 10)
        elif i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga'] < melhor_rota[i]['carga']:
            cor = AZUL
            pygame.draw.circle(tela, cor, (x, y), 10)
        elif i < len(melhor_rota) - 1 and melhor_rota[i-1]['carga'] > melhor_rota[i]['carga']:
            cor = VERMELHO
            pygame.draw.circle(tela, cor, (x, y), 10)

        texto = f"Loja {ponto['index_loja']}"  # Print store number/name
        fonte = pygame.font.Font(None, 18)
        texto_renderizado = fonte.render(texto, True, (0, 0, 0))
        tela.blit(texto_renderizado, (x, y - 20))

        if initial_point > 0 :
            pygame.draw.lines(tela, VERDE, False, [(lojas[ponto["index_loja"]]['x'] * size, lojas[ponto["index_loja"]]['y'] * size) for ponto in melhor_rota[:initial_point + 1]], 2) # Draw the lines


    # Update truck position based on scale
    x_caminhao = lojas[melhor_rota[initial_point]["index_loja"]]['x'] * size
    y_caminhao = lojas[melhor_rota[initial_point]["index_loja"]]['y'] * size

    caminhao_rect = imagem_caminhao.get_rect(center=(x_caminhao, y_caminhao))
    tela.blit(imagem_caminhao, caminhao_rect) # Show truck

    # Update initial point 
    initial_point += 1
    if initial_point >= len(melhor_rota):
        initial_point = 0

    pygame.display.flip()
    time.sleep(tempo_atraso)

pygame.quit() # Close front-end