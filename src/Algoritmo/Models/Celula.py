class Celula:
    def __init__(self, ruta):
        self.ruta = list(ruta)
        self.fitness = 0

    def __eq__(self, otro):
        if not isinstance(otro, Celula):
            return False
        return self.ruta == otro.ruta

    def __hash__(self):
        return hash(tuple(self.ruta))
