import math

if __name__ == '__main__':
    stores = []
    stores_obj = [] 
    truck_products = []
    
    # Open and read file
    with open("lojas.txt", "r") as file:
        for line in file:
            stores.append(line.replace("\n", ""))
    
    # Create a list of stores with their attributes
    for store in stores:
        store_aux = store.split(" ")
        stores_obj.append({"number": store_aux[0], "x": int(store_aux[1]), "y": int(store_aux[2]), "destination_stores": store_aux[3:] if len(store_aux) > 2 else []})

    
    origin_store = stores_obj[0]
    route = [].append(stores_obj.filter(lambda store: store.get("destination_stores") > 0)[0])
    print(route)
for i in range(1, len(stores_obj)):
    for j in range(1, len(stores_obj)):
        if i != j:
            pass
        
    # Calculate the distance between two points
def calcular_distancia(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    # calcula o consumo de combustivel
def calcular_gasto_combustivel(distancia, num_produtos):
    rendimento = 10 - (num_produtos * 0.5)
    return distancia / rendimento


def encontrar_proxima_loja(loja_atual, lojas, rota):
    distancia_minima = math.inf
    proxima_loja = None

    # Iterar sobre todas as lojas para calcular a rota do caminhão
    for loja in lojas:
        # Verificar se a loja atual não está presente na rota percorrida
        if loja not in rota:
            # Verificar se a distância calculada é menor que a distância mínima encontrada até agora
            distancia = calcular_distancia(
                loja_atual["x"], loja_atual["y"], loja["x"], loja["y"]
            )
            if distancia < distancia_minima:
                distancia_minima = distancia
                proxima_loja = loja

    return proxima_loja, distancia_minima

def calcular_rota_caminhao(lojas, carga_caminhao, distancia_atual, rota_atual, melhor_distancia, melhor_rota):
    # Obter a loja atual e a carga atual com base na rota atual
    loja_atual = rota_atual[-1]
    carga_atual = sum(len(loja["destination_stores"]) for loja in rota_atual)

    # Verificar se a carga atual excede a capacidade do caminhão
    if carga_atual >= carga_caminhao:
        # Adicionar a distância de retorno ao ponto de partida à distância atual
        distancia_atual += calcular_distancia(loja_atual["x"], loja_atual["y"], lojas[0]["x"], lojas[0]["y"])
        # Adicionar a loja inicial à rota atual
        rota_atual.append(lojas[0])

        # Verificar se a distância atual é menor que a melhor distância encontrada até agora
        if distancia_atual < melhor_distancia:
            melhor_distancia = distancia_atual
            melhor_rota = rota_atual.copy()

        # Retornar a melhor distância e a melhor rota
        return melhor_distancia, melhor_rota

    # Iterar sobre todas as lojas para encontrar a próxima loja a ser visitada
    for loja in lojas:
        if loja not in rota_atual:
            # Criar uma nova rota com a loja atual
            nova_rota = rota_atual.copy()
            nova_rota.append(loja)
            # Calcular a nova distância considerando a loja atual
            nova_distancia = distancia_atual + calcular_distancia(loja_atual["x"], loja_atual["y"], loja["x"], loja["y"])

            # Verificar se a nova distância é menor que a melhor distância encontrada até agora
            if nova_distancia < melhor_distancia:
                # Chamada recursiva da função para continuar construindo a rota
                nova_melhor_distancia, nova_melhor_rota = calcular_rota_caminhao(
                    lojas, carga_caminhao, nova_distancia, nova_rota, melhor_distancia, melhor_rota
                )

                # Verificar se a nova melhor distância é menor que a melhor distância encontrada até agora
                if nova_melhor_distancia < melhor_distancia:
                    melhor_distancia = nova_melhor_distancia
                    melhor_rota = nova_melhor_rota

    return melhor_distancia, melhor_rota


# Ler informações das lojas do arquivo
lojas = []
with open("lojas.txt", "r") as file:
    for line in file:
        store_info = line.split()
        loja = {
            "number": int(store_info[0]),
            "x": int(store_info[1]),
            "y": int(store_info[2]),
            "destination_stores": [int(dest) for dest in store_info[3:]]
        }
        lojas.append(loja)

# Parâmetros do caminhão
carga_caminhao = 5

# Inicialização das variáveis
distancia_inicial = 0
rota_inicial = [lojas[0]]
melhor_distancia = math.inf
melhor_rota = []

# Calcular rota do caminhão utilizando branch-and-bound
melhor_distancia, melhor_rota = calcular_rota_caminhao(
    lojas, carga_caminhao, distancia_inicial, rota_inicial, melhor_distancia, melhor_rota
)

# Calcular gasto de combustível
gasto_combustivel = calcular_gasto_combustivel(melhor_distancia, carga_caminhao)

# Imprimir resultados
print("Rota do caminhão:")
for loja in melhor_rota:
    print(loja["number"], loja["x"], loja["y"])

print("Distância total percorrida:", melhor_distancia)
print("Gasto de combustível:", gasto_combustivel)
