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
    def two_points_distance(xA, xB, yA, yB):
        return (xB - xA) ** 2 + (yB - yA) ** 2

    #calcula o consumo de combustivel 
    def calcula_gasto_combustivel (distancia, num_produtos):
        rendimento = 10 - (num_produtos * 0.5 )
        return distancia / rendimento

    #rota do caminhão
     def rota_caminhao (matriz, carga_caminhao):
        rota = []
        distancia_total = 0
        carga = 0 

        loja_atual = matriz[0]
        rota.append(loja_atual)
        
    while True:
    distancia_minima = math.inf
    proxima_loja = None

        for loja in matriz:
            if loja not in rota:
                distancia_total = two_points_distance(loja_atual[0],loja_atual[1], loja[0], loja[1])


