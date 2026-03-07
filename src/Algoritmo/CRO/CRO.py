def ejecutar_algoritmo_cro(moleculas, matriz_distancias, cantidad_generaciones):
    for generacion in range(cantidad_generaciones):
        print(f"Generación {generacion + 1}")

        for i, molecula in enumerate(moleculas):
            print(f"Molécula {i + 1}: Ruta: {' -> '.join(molecula.ruta)}, PE: {molecula.pe}, KE: {molecula.ke}")
    return moleculas