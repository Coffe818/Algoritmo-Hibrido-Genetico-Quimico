from time import time

import pandas as pd
import random
from Algoritmo.Models.Celula import Celula

poblacion_size = 100
matriz_distancias = {}
porcentaje_elitismo = 0.1
torneo_size = 5


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


def seleccionar_padres(celulas):
    cantidad_elitismo = int(len(celulas) * porcentaje_elitismo)
    elitaria = seleccion_elitaria(celulas, cantidad_elitismo)
    torneo = seleccion_torneo(celulas, cantidad_elitismo)
    return [elitaria, torneo]


def seleccion_elitaria(celulas, cantidad_elitismo):
    sorted_celulas = sorted(celulas, key=lambda c: c.fitness)
    return sorted_celulas[:cantidad_elitismo]


def seleccion_torneo(celulas, cantidad_elitismo):
    padres = []
    cantidad_torneo = len(celulas) // 2 - (cantidad_elitismo // 2)
    for _ in range(cantidad_torneo):
        torneo = random.sample(celulas, torneo_size)
        ganador = min(torneo, key=lambda c: c.fitness)
        padres.append(ganador)
    return padres


def ejecutar_algoritmo():
    celulas = generar_poblacion()
    elitismo, torneo = seleccionar_padres(celulas)

    for celula in elitismo:
        print(
            f"RutaElitista: {' -> '.join(celula.ruta)} | Distancia Total: {celula.fitness}"
        )

    for celula in torneo:
        print(
            f"RutaTorneo: {' -> '.join(celula.ruta)} | Distancia Total: {celula.fitness}"
        )

    print("celulas", len(celulas))
    print("PadresTorneo", len(torneo))
