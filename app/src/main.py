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
                

    # Calculate the distance between two points 
def two_points_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    #calcula o consumo de combustivel 
def calcular_gasto_combustivel(distancia, num_produtos):
    rendimento = 10 - (num_produtos * 0.5)
    return distancia / rendimento


def encontrar_proxima_loja(loja_atual, lojas, rota):
    distancia_minima = math.inf
    proxima_loja = None 

    for loja in lojas:
        if loja not in rota:
            distancia = two_points_distance(loja_atual["x"], loja_atual["y"], loja["x"], loja["y"])
            if distancia < distancia_minima:
                distancia_minima = distancia
                proxima_loja = loja

    return proxima_loja, distancia_minima

def calcular_rota_caminhao(lojas, carga_caminhao):
    rota = []
    distancia_total = 0
    carga = 0 

    loja_atual = lojas[0]
    rota.append(loja_atual)
        
    while True:
        proxima_loja, distancia = encontrar_proxima_loja(loja_atual, lojas, rota)

        if proxima_loja is None:
            # Todas as lojas foram visitadas, retornar à matriz
            distancia_total += two_points_distance(loja_atual["x"], loja_atual["y"], lojas[0]["x"], lojas[0]["y"])
            rota.append(lojas[0])
            break
        
        distancia_total += distancia
        carga += len(loja_atual["destination_stores"])

        if carga >= carga_caminhao:
            distancia_total += two_points_distance(loja_atual["x"], loja_atual["y"], lojas[0]["x"], lojas[0]["y"])
            rota.append(lojas[0])
            carga = 0

        rota.append(proxima_loja)
        loja_atual = proxima_loja

    return rota, distancia_total

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

# Calcular rota do caminhão
rota, distancia_total = calcular_rota_caminhao(lojas, carga_caminhao)

# Calcular gasto de combustível
gasto_combustivel = calcular_gasto_combustivel(distancia_total, carga_caminhao)

# Imprimir resultados
print("Rota do caminhão:")
for loja in rota:
    print(loja["number"], loja["x"], loja["y"])

print("Distância total percorrida:", distancia_total)