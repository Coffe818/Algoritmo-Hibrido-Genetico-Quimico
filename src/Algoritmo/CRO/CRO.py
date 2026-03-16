import random

from Algoritmo.Models.Molecula import Molecula

buffer_central = 10000
KELossRate = 0.2
moleculas = []
matriz_distancias = {}
Ke_defult_descomposicion = 100


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
    global moleculas, buffer_central

    cantidad = random.randint(2, 3)

    grupo = random.sample(moleculas, cantidad)
    energia_total_entrada = sum(m.pe + m.ke for m in grupo)
    energia_total_requerida = 0
    porcion = len(grupo[1].ruta) // cantidad
    porcion_inicio = 0
    porcion_final = porcion
    nueva_ruta = []

    for molecula_actual in grupo:
        molecula_filtrada = [
            nodo for nodo in molecula_actual.ruta if nodo not in nueva_ruta
        ]

        for nodo in molecula_filtrada[0:porcion]:
            nueva_ruta.append(nodo)

        print(nueva_ruta)

    if nueva_ruta.count(None) > 0:

        molecula_rellenar = random.choice(grupo)
        nodos_rellenar = [
            nodo for nodo in molecula_rellenar.ruta if nodo not in nueva_ruta
        ]
        for i in range(len(nueva_ruta)):
            if nueva_ruta[i] is None:
                nueva_ruta[i] = nodos_rellenar.pop(0)

    energia_total_requerida = calcular_pe(nueva_ruta)

    if energia_total_requerida < energia_total_entrada:
        for molecula in grupo:
            moleculas.remove(molecula)

        ke_restante = energia_total_entrada - energia_total_requerida
        ke_restante_molecula = ke_restante // 4
        buffer_central += ke_restante - ke_restante_molecula

        molecula_nueva = Molecula(
            nueva_ruta, energia_total_requerida, ke_restante_molecula
        )
        moleculas.append(molecula_nueva)

    return "sintesis"


def colision_intermolecular():
    global moleculas

    cantidad = random.randint(2, 3)

    grupo = random.sample(moleculas, cantidad)
    energia_total_entrada = sum(m.pe + m.ke for m in grupo)
    nuevas_configuraciones = []
    energia_total_requerida = 0

    for molecula_actual in grupo:
        companeras = [m for m in grupo if m != molecula_actual]
        nueva_ruta = [None] * len(molecula_actual.ruta)
        pe_nueva = 0
        for companera in companeras:

            punto1 = random.randint(1, len(molecula_actual.ruta) - 2)
            punto2 = random.randint(1, len(molecula_actual.ruta) - 2)
            if punto1 == punto2:
                punto2 = (punto1 + 5) % len(molecula_actual.ruta)

            if punto1 > punto2:
                punto1, punto2 = punto2, punto1

            nueva_ruta[punto1:punto2] = molecula_actual.ruta[punto1:punto2]

            para_rellenar = [nodo for nodo in companera.ruta if nodo not in nueva_ruta]

            for i in range(len(nueva_ruta)):
                if nueva_ruta[i] is None:
                    nueva_ruta[i] = para_rellenar.pop(0)

            pe_nueva = calcular_pe(nueva_ruta)
            energia_total_requerida += pe_nueva
            if pe_nueva == float("inf"):
                energia_total_requerida = float("inf")
                break

            if energia_total_requerida > energia_total_entrada:
                break

        nuevas_configuraciones.append((nueva_ruta, pe_nueva))

    if energia_total_entrada > energia_total_requerida:
        ke_restante = energia_total_entrada - energia_total_requerida
        for i in range(len(grupo)):
            moleculas.remove(grupo[i])
            molecula_nueva = Molecula(
                nuevas_configuraciones[i][0],
                nuevas_configuraciones[i][1],
                ke_restante // len(grupo),
            )
            moleculas.append(molecula_nueva)
    return


def descomposicion():
    global buffer_central

    molecula_original = random.choice(moleculas)

    ruta1 = list(molecula_original.ruta)
    ruta2 = list(molecula_original.ruta)

    random.shuffle(ruta1)
    random.shuffle(ruta2)

    pe1 = calcular_pe(ruta1)
    pe2 = calcular_pe(ruta2)

    energia_requerida = pe1 + pe2

    energia_disponible = molecula_original.pe + molecula_original.ke

    diferenca_energia = energia_disponible - energia_requerida

    def guardar_moleculas(ke_restante):
        global moleculas
        moleculas.remove(molecula_original)
        molecula1 = Molecula(ruta1, pe1, ke_restante)
        molecula2 = Molecula(ruta2, pe2, ke_restante // 2)
        moleculas.append(molecula1)
        moleculas.append(molecula2)

    if diferenca_energia > 0:
        guardar_moleculas(diferenca_energia)
        return

    buffer_disponible = buffer_central // 2
    diferenca_energia = energia_disponible - (
        energia_requerida + 2 * Ke_defult_descomposicion
    )

    if diferenca_energia < 0 and (diferenca_energia + buffer_disponible) >= 0:
        buffer_central += diferenca_energia
        guardar_moleculas(Ke_defult_descomposicion * 2)
        return

    return


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


def ejecutar_algoritmo_cro(moleculas_cro, matriz_distancias_cro, cantidad_generaciones):
    global moleculas, matriz_distancias
    moleculas = moleculas_cro.copy()
    matriz_distancias = matriz_distancias_cro.copy()

    for generacion in range(cantidad_generaciones):

        print(f"antes ")
        for i, molecula in enumerate(moleculas):
            print(
                f"Molecula {i}: {molecula.ruta}, PE: {molecula.pe}, KE: {molecula.ke}"
            )

        decidir(procesos_multimoleculares, procesos_unimoleculares)

        print(f"despuues ")
        for i, molecula in enumerate(moleculas):
            print(
                f"Molecula {i}: {molecula.ruta}, PE: {molecula.pe}, KE: {molecula.ke}"
            )

    return moleculas
