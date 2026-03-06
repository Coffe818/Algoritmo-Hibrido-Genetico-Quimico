class Molecula:
    def __init__(self, ruta, pe_inicial, ke_inicial):

        self.ruta = list(ruta)

        self.pe = pe_inicial
        self.ke = ke_inicial

        self.min_struct = list(ruta)
        self.min_pe = pe_inicial
        self.num_hit = 0
        self.min_hit = 0

    def actualizar_memoria(self, nueva_pe, nueva_ruta):
        self.num_hit += 1
        if nueva_pe < self.min_pe:
            self.min_pe = nueva_pe
            self.min_struct = list(nueva_ruta)
            self.min_hit = self.num_hit
