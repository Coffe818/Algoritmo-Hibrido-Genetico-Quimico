import pandas as pd
import googlemaps
import os
import time
from dotenv import load_dotenv

# --- CARGAR CONFIGURACIÓN ---
# load_dotenv busca el archivo .env automáticamente
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY:
    raise ValueError("No se encontró la clave de Google Maps en el archivo .env")

# Inicializamos el cliente de Google
gmaps = googlemaps.Client(key=API_KEY)

# Rutas de archivos usando la ubicación del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CSV = os.path.join(BASE_DIR, "poblacion.csv")
ARCHIVO_SALIDA = os.path.join(BASE_DIR, "Grafo_Coahuila_Final.txt")


def cargar_progreso():
    """Revisa el archivo de salida para no repetir cálculos y ahorrar dinero."""
    procesados = set()
    if os.path.exists(ARCHIVO_SALIDA):
        with open(ARCHIVO_SALIDA, "r", encoding="utf-8") as f:
            next(f, None)  # Saltar encabezado
            for linea in f:
                parts = linea.strip().split(",")
                if len(parts) >= 3:
                    procesados.add((parts[0], parts[2]))
    return procesados


def ejecutar_proceso():
    # 1. Cargar datos de Coahuila
    print(f"Cargando datos desde {ARCHIVO_CSV}...")
    df = pd.read_csv(ARCHIVO_CSV, dtype={"clave_entidad": str, "clave_municipio": str})
    df_coah = df[df["clave_entidad"] == "05"]

    municipios = []
    for _, r in df_coah.iterrows():
        municipios.append(
            {
                "cve": r["clave_municipio"],
                "nom": r["municipio"],
                "loc": f"{r['latitud']},{r['longitud']}",  # Formato para Google
            }
        )

    # 2. Preparar el archivo de salida y cargar progreso
    ya_hechos = cargar_progreso()
    if not os.path.exists(ARCHIVO_SALIDA):
        with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
            f.write("ID_Org,Nom_Org,ID_Dest,Nom_Dest,Dist_KM\n")

    # 3. Bucle de cálculo
    n = len(municipios)
    print(f"Iniciando cálculo para {n} municipios (Coahuila)...")

    # Usamos un bucle tradicional para tener control total sobre las pausas y errores
    for i in range(n):
        for j in range(n):
            m1, m2 = municipios[i], municipios[j]

            # Saltamos si es el mismo o si ya existe en el archivo
            if i == j or (m1["cve"], m2["cve"]) in ya_hechos:
                continue

            try:
                # Llamada a la Distance Matrix API
                # Google maneja el tráfico de maravilla, no necesitamos concurrencia compleja aquí
                res = gmaps.distance_matrix(m1["loc"], m2["loc"], mode="driving")
                if res["status"] == "OK":
                    elemento = res["rows"][0]["elements"][0]

                    if elemento["status"] == "OK":
                        dist_km = elemento["distance"]["value"] / 1000.0

                        # Guardado inmediato (Append mode)
                        with open(ARCHIVO_SALIDA, "a", encoding="utf-8") as f:
                            f.write(
                                f"{m1['cve']},{m1['nom']},{m2['cve']},{m2['nom']},{dist_km:.4f}\n"
                            )

                        print(
                            f"[GOOGLE OK] {m1['nom']} -> {m2['nom']}: {dist_km:.2f} km"
                        )
                    else:
                        print(
                            f"[AVISO] Sin ruta: {m1['nom']} a {m2['nom']} ({elemento['status']})"
                        )

                # Pausa mínima para ser "buen ciudadano" con la API
                time.sleep(0.05)

            except Exception as e:
                print(f"[ERROR] Falló la petición: {e}")
                time.sleep(2)  # Pausa larga si hay error de red

    print(f"\n--- PROCESO TERMINADO ---")
    print(f"Grafo guardado en: {ARCHIVO_SALIDA}")


if __name__ == "__main__":
    ejecutar_proceso()
