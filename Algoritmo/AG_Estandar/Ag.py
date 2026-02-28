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
    celulas = []
    nodos_unicos = cargar_datos()

    for i in range(poblacion_size):
        ruta_aleatoria = random.sample(nodos_unicos, len(nodos_unicos))
        nueva_celula = Celula(ruta_aleatoria)
        nueva_celula.fitness = evaluar_ruta(nueva_celula.ruta)
        celulas.append(nueva_celula)
    return celulas


def seleccionar_cruzar_mutar_evaluar(celulas):
    cantidad_elitismo = int(len(celulas) * porcentaje_elitismo)
    celulas_elitistas = seleccion_elitista(celulas, cantidad_elitismo)
    rutas_torneo = seleccion_torneo_cruza(celulas, cantidad_elitismo)

    mutar(rutas_torneo)

    nuevas_celulas_torneo = []
    for ruta in rutas_torneo:
        nueva = Celula(ruta)
        nueva.fitness = evaluar_ruta(ruta)
        nuevas_celulas_torneo.append(nueva)

    return celulas_elitistas + nuevas_celulas_torneo


def seleccion_elitista(celulas, cantidad_elitismo):
    celulas_ordenadas = sorted(celulas, key=lambda c: c.fitness)
    return celulas_ordenadas[:cantidad_elitismo]


def seleccion_torneo_cruza(celulas, cantidad_elitismo):
    resultado_cruza = []
    cantidad_torneo = (len(celulas) - cantidad_elitismo) // 2
    for _ in range(cantidad_torneo):
        torneo1 = random.sample(celulas, torneo_size)
        padre1 = min(torneo1, key=lambda c: c.fitness)
        torneo2 = random.sample(celulas, torneo_size)
        padre2 = min(torneo2, key=lambda c: c.fitness)

        hijo1, hijo2 = cruzar(padre1, padre2)
        # print("padres")
        # print(f"Ruta: {' -> '.join(padre1.ruta)} - Distancia: {padre1.fitness}")
        # print(f"Ruta: {' -> '.join(padre2.ruta)} - Distancia: {padre2.fitness}")

        # print("hijos")
        # print(f"Ruta: {' -> '.join(hijo1)}")
        # print(f"Ruta: {' -> '.join(hijo2)}")

        resultado_cruza.append(hijo1)
        resultado_cruza.append(hijo2)

    return resultado_cruza


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


def mutar(rutas):

    size = len(rutas[0])

    for ruta in rutas:
        if random.random() < tasa_mutacion:
            for _ in range(ciculos_mutacion):
                idx1, idx2 = random.sample(range(size), 2)
                ruta[idx1], ruta[idx2] = ruta[idx2], ruta[idx1]


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
