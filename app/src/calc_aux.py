import math


# Calculate the distance between two points
def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# Calculate the fuel consumption for a given distance and number of products
def calculate_fuel_consumption(distancia, num_produtos):
    rendimento = 10 - (num_produtos * 0.5)
    return distancia / rendimento


if __name__ == '__main__':
    lojas = []
    rota = [(0, 0), (1, 2), (2, 1), (3, 1), (5, 2), (4, 1), (9, 2), (7, 2), (8, 1), (6,0)]
    rota2 = [(0, 0), (1, 2), (2, 1), (3, 1), (5, 2), (4, 1), (9, 2), (7, 2), (6, 1), (8,0)]
    gasto = 0
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
    for i in range(1, len(rota)):
        loja_ant = rota[i-1]
        loja_at = rota[i]
        # Calculate the fuel consumption for the rota variable, which is a list of number of store and the number of products
        gasto += calculate_fuel_consumption(calculate_distance(lojas[loja_ant[0]]['x'], lojas[loja_ant[0]]['y'], lojas[loja_at[0]]['x'], lojas[loja_at[0]]['y']), loja_ant[1])
        print(gasto, loja_at)
    print(gasto)
    print(" --- xx ---")
    gasto = 0
    for i in range(1, len(rota2)):
        loja_ant = rota2[i-1]
        loja_at = rota2[i]
        # Calculate the fuel consumption for the rota variable, which is a list of number of store and the number of products
        gasto += calculate_fuel_consumption(calculate_distance(lojas[loja_ant[0]]['x'], lojas[loja_ant[0]]['y'], lojas[loja_at[0]]['x'], lojas[loja_at[0]]['y']), loja_ant[1])
        print(gasto, loja_at)
    print(gasto)