import random

buffer_central = 100
KELossRate = 0.2
moleculas = []
matriz_distancias = {}


def calcular_pe(ruta):
    pe = 0
    for i in range(len(ruta)):
        punto_a = ruta[i]
        punto_b = ruta[(i + 1) % len(ruta)]
        conexion = (punto_a, punto_b)
        if conexion in matriz_distancias:
            pe += matriz_distancias[conexion]
        else:
            pe += float("inf")

    return pe


def decidir(func_a, func_b):
    if random.random() < 0.5:
        func_a()
    else:
        func_b()


def procesos_multimoleculares():
    decidir(sintesis, colision_intermolecular)


def procesos_unimoleculares():
    decidir(descomposicion, colision_pared)


def sintesis():
    return "sintesis"


def colision_intermolecular():
    return "colision_intermolecular"


def descomposicion():
    return "descomposicion"


def colision_pared():
    global buffer_central

    molecula_original = random.choice(moleculas)
    nueva_ruta = list(molecula_original.ruta)

    for _ in range(10):
        idx1, idx2 = random.sample(range(len(nueva_ruta)), 2)
        nueva_ruta[idx1], nueva_ruta[idx2] = (
            nueva_ruta[idx2],
            nueva_ruta[idx1],
        )

    nuevo_pe = calcular_pe(nueva_ruta)
    diferencia_pe = molecula_original.pe - nuevo_pe

    if diferencia_pe == 0:
        return

    if diferencia_pe > 0:
        molecula_original.ruta = nueva_ruta
        molecula_original.pe = nuevo_pe
        molecula_original.ke += abs(diferencia_pe) * (1 - KELossRate)
        buffer_central += abs(diferencia_pe) * KELossRate
        return

    if (diferencia_pe + molecula_original.ke) > 0:
        molecula_original.ruta = molecula_original.ruta
        molecula_original.pe = nuevo_pe
        molecula_original.ke += diferencia_pe
        return

    return "colision_pared"


def ejecutar_algoritmo_cro(moleculas_cro, matriz_distancias_cro, cantidad_generaciones):
    global moleculas, matriz_distancias
    moleculas = moleculas_cro.copy()
    matriz_distancias = matriz_distancias_cro.copy()

    for generacion in range(cantidad_generaciones):
        decidir(procesos_multimoleculares, procesos_unimoleculares)

    return moleculas
