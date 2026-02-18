from time import time

import pandas as pd
import random
from Algoritmo.Models.Celula import Celula

poblacion_size = 100
matriz_distancias = {}


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

    tiempo_inicio = time()
    for i in range(poblacion_size):
        ruta_aleatoria = random.sample(nodos_unicos, len(nodos_unicos))
        nueva_celula = Celula(ruta_aleatoria)
        nueva_celula.fitness = evaluar_ruta(nueva_celula.ruta)
        celulas.append(nueva_celula)

    for celula in celulas:
        print(f"Ruta: {' -> '.join(celula.ruta)} | Distancia Total: {celula.fitness}")
    tiempo_fin = time()
    print(f"Tiempo de ejecución: {tiempo_fin - tiempo_inicio:.4f} segundos")
