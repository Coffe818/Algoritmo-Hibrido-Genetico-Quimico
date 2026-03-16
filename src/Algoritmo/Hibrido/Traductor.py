from Algoritmo.Models.Molecula import Molecula
from Algoritmo.Models.Celula import Celula


def celula_a_molecula(celula, ke_inicial):
    return Molecula(celula.ruta, celula.fitness, ke_inicial)


def molecula_a_celula(molecula):
    nueva_celula = Celula(molecula.ruta)
    nueva_celula.fitness = molecula.pe
    return nueva_celula


def celulas_a_moleculas(celulas, ke_inicial=100):
    return [celula_a_molecula(celula, ke_inicial) for celula in celulas]


def moleculas_a_celulas(moleculas):
    return [molecula_a_celula(molecula) for molecula in moleculas]
