from time import time

import pandas as pd
import random
from Algoritmo.Models.Celula import Celula

matriz_distancias = {}
cantidad_generaciones = 10
poblacion_size = 20
porcentaje_elitismo = 0.1
torneo_size = 5
tasa_mutacion = 0.1
ciculos_mutacion = 5


def cargar_datos():
    global matriz_distancias
    df = pd.read_csv("Grafo/Grafo.txt")

    for _, fila in df.iterrows():
        origen = str(fila["Origen"])
        destino = str(fila["Destino"])
        distancia = float(fila["Distancia"])
        matriz_distancias[(origen, destino)] = distancia

    nodos = pd.unique(df[["Origen", "Destino"]].values.ravel()).tolist()
    return nodos


def evaluar_ruta(ruta):
    distancia_total = 0

    for i in range(len(ruta)):
        punto_a = ruta[i]
        punto_b = ruta[(i + 1) % len(ruta)]
        conexion = (punto_a, punto_b)
        if conexion in matriz_distancias:
            distancia_total += matriz_distancias[conexion]
        else:
            distancia_total += float("inf")

    return distancia_total


def generar_poblacion():
    celulas = set()
    nodos_unicos = cargar_datos()

    while len(celulas) < poblacion_size:
        ruta_aleatoria = random.sample(nodos_unicos, len(nodos_unicos))
        nueva_celula = Celula(ruta_aleatoria)

        if nueva_celula not in celulas:
            nueva_celula.fitness = evaluar_ruta(nueva_celula.ruta)
            celulas.add(nueva_celula)
    return celulas


def seleccionar_cruzar_mutar_evaluar(celulas):
    cantidad_elitismo = int(len(celulas) * porcentaje_elitismo)
    celulas_elitistas = seleccion_elitista(celulas, cantidad_elitismo)

    nueva_generacion = set(celulas_elitistas)

    rutas_torneo = seleccion_torneo_cruza(celulas, nueva_generacion)

    # print("Rutas elitistas seleccionadas:")
    # for i, celula in enumerate(nueva_generacion):
    #     print(f"Ruta {i+1}: {' -> '.join(celula.ruta)} - Distancia: {celula.fitness}")

    # print("Rutas seleccionadas para torneo:")
    # for i, ruta in enumerate(rutas_torneo):
    #     print(f"Ruta {i+1}: {' -> '.join(ruta)}")

    mutar(rutas_torneo, nueva_generacion)

    nuevas_celulas_torneo = []
    for ruta in rutas_torneo:
        nueva = Celula(ruta)
        nueva.fitness = evaluar_ruta(ruta)
        nuevas_celulas_torneo.append(nueva)

    return celulas_elitistas + nuevas_celulas_torneo


def seleccion_elitista(celulas, cantidad_elitismo):
    celulas_ordenadas = sorted(celulas, key=lambda c: c.fitness)
    return celulas_ordenadas[:cantidad_elitismo]


def seleccion_torneo_cruza(celulas, rutas_existentes):

    rutas_torneo = set()
    while len(rutas_existentes) + len(rutas_torneo) < poblacion_size:
        torneo1 = random.sample(list(celulas), torneo_size)
        padre1 = min(torneo1, key=lambda c: c.fitness)
        torneo2 = random.sample(list(celulas), torneo_size)
        padre2 = min(torneo2, key=lambda c: c.fitness)

        hijo1, hijo2 = cruzar(padre1, padre2)
        t1, t2 = tuple(hijo1), tuple(hijo2)

        agregar_hijo1 = t1 not in rutas_existentes and t1 not in rutas_torneo
        agregar_hijo2 = t2 not in rutas_existentes and t2 not in rutas_torneo
        diferentes_hijos = t1 != t2

        if agregar_hijo1 and agregar_hijo2 and diferentes_hijos:
            rutas_torneo.add(t1)
            rutas_torneo.add(t2)
            # print(f"nueva longitud de rutas torneo: {len(rutas_torneo)}")

        # print("padres")
        # print(f"Ruta: {' -> '.join(padre1.ruta)} - Distancia: {padre1.fitness}")
        # print(f"Ruta: {' -> '.join(padre2.ruta)} - Distancia: {padre2.fitness}")

        # print("hijos")
        # print(f"Ruta: {' -> '.join(hijo1)}")
        # print(f"Ruta: {' -> '.join(hijo2)}")
    return rutas_torneo


def cruzar(padre1, padre2):
    ruta1, ruta2 = padre1.ruta, padre2.ruta
    size = len(ruta1)
    punto1 = size // 3
    punto2 = 2 * size // 3

    def generar_hijo(p1, p2):
        hijo = [None] * size

        hijo[punto1:punto2] = p1[punto1:punto2]

        nodos_restantes = [nodo for nodo in p2 if nodo not in hijo[punto1:punto2]]
        for i in range(punto1):
            hijo[i] = nodos_restantes.pop(0)

        for i in range(punto2, size):
            hijo[i] = nodos_restantes.pop(0)

        return hijo

    hijo1 = generar_hijo(ruta1, ruta2)
    hijo2 = generar_hijo(ruta2, ruta1)

    return hijo1, hijo2


def mutar(rutas_torneo, nueva_generacion):

    ruta_size = len(list(rutas_torneo)[0])
    rutas_torneo_copia = list(rutas_torneo)

    for ruta in rutas_torneo_copia:
        if random.random() < tasa_mutacion:
            ruta_original = list(ruta)
            rutas_torneo.remove(ruta)

            while len(rutas_torneo) + len(nueva_generacion) < poblacion_size:
                ruta_mutar = list(ruta_original)

                for _ in range(ciculos_mutacion):
                    idx1, idx2 = random.sample(range(ruta_size), 2)
                    ruta_mutar[idx1], ruta_mutar[idx2] = (
                        ruta_mutar[idx2],
                        ruta_mutar[idx1],
                    )
                if (
                    tuple(ruta_mutar) not in rutas_torneo
                    and tuple(ruta_mutar) not in nueva_generacion
                ):
                    rutas_torneo.add(tuple(ruta_mutar))


def ejecutar_algoritmo():
    celulas = generar_poblacion()
    i = 0
    while True:
        i += 1

        print(f"Generacion {i}")
        timer = time()
        celulas = seleccionar_cruzar_mutar_evaluar(celulas)
        timer = time() - timer
        print(f"Tiempo de generacion: {timer:.10f} segundos")
        print("Promiedio de fitness: ", sum(c.fitness for c in celulas) / len(celulas))
        for celula in celulas:
            print(f"Ruta: {' -> '.join(celula.ruta)} - Distancia: {celula.fitness}")
