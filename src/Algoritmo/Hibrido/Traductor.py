from Algoritmo.Models.Molecula import Molecula
from Algoritmo.Models.Celula import Celula


class TraductorHibrido:
    def celula_a_molecula(celula, ke_inicial=1000):
        """
        Convierte una Célula del AG en una Molécula del CRO.
        El fitness de la célula se convierte en la PE (Energía Potencial).
        """
        return Molecula(celula.ruta, celula.fitness, ke_inicial)

    def molecula_a_celula(molecula):
        """
        Convierte una Molécula del CRO de vuelta a Célula del AG.
        Extrae la mejor estructura encontrada (MinStruct) durante el proceso.
        """
        nueva_celula = Celula(molecula.min_struct)
        nueva_celula.fitness = molecula.min_pe
        return nueva_celula