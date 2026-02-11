import string


def generar_grafo():
    ciudades = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    n = len(ciudades)
    print(f"Generando grafo para {n} ciudades: {ciudades}")
    with open("Grafo/Grafo.txt", "w") as f:
        f.write("Origen,Destino,Distancia\n")

        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
            po = i
            pf = j

            d = pf - po

            if d < 0:
                distancia_final = d + n
            else:
                distancia_final = d

            f.write(f"{ciudades[i]},{ciudades[j]},{distancia_final}\n")

    print("Archivo 'Grafo.txt' generado con exito")


if __name__ == "__main__":
    generar_grafo()
