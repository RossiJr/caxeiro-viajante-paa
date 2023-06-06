import math
import itertools


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
    rota.append(loja_atual)

    for loja in lojas[1:]:
        distancia = calculate_distance(loja_atual['x'], loja_atual['y'], loja['x'], loja['y'])
        gasto_combustivel = calculate_fuel_consumption(distancia, carga)

        if loja['number'] in destinos:
            # Remover loja da lista de destinos
            destinos.remove(loja['number'])
            carga -= 1
        for dest in loja['destination_stores']:
            destinos.append(dest)
        gastoTotal += gasto_combustivel
        carga += len(loja["destination_stores"]) # Atualiza a carga do caminhão com o número de destinos da loja atual

        # A carga do caminhão excedeu a capacidade, retornar ao ponto de partida
        if carga >= carga_caminhao:
            break
        
        # Adiciona a próxima loja à rota
        rota.append(loja)
        # Atualiza a loja atual para a próxima loja
        loja_atual = loja

    return rota, gastoTotal, carga

# Ler informações das lojas do arquivo
lojas = []
with open("D:\\PAA\\trab2\\caxeiro2\\caxeiro-viajante-paa\\app\\src\\lojas.txt", "r") as file:
    for line in file:
        store_info = line.split()
        loja = {
            "number": int(store_info[0]),
            "x": int(store_info[1]),
            "y": int(store_info[2]),
            "destination_stores": [int(dest) for dest in store_info[3:]],
        }
        lojas.append(loja)

# Parâmetros do caminhão
carga_caminhao = 5

# Gerar todas as permutações dos destinos
destinos = lojas[1:]  # Exclui a matriz
permutacoes = list(itertools.permutations(destinos))

melhor_rota = None
melhor_gasto_combustivel = math.inf

# Calcular rota e gasto de combustível para cada permutação
for permutacao in permutacoes:
    destinos_permutados = [lojas[0]] + list(permutacao)
    rota, gasto_total, carga = calculate_route(destinos_permutados, carga_caminhao)

    if carga == 0 and gasto_total < melhor_gasto_combustivel:
        melhor_rota = rota
        melhor_gasto_combustivel = gasto_total
# Imprimir resultados
print("Rota do caminhão:")
for loja in melhor_rota:
    print(loja["number"], loja["x"], loja["y"])

print("Melhor gasto de combustível:", gasto_total)
