import json
import os
import random

# =====================
# Funciones auxiliares
# =====================

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def cargar_personajes():
    if os.path.exists("personajesPOP.json"):
        with open("personajesPOP.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # Base inicial de personajes ficticios (5 hombres, 5 mujeres)
        personajes = [
            {"nombre": "Iron Man", "serie": "Marvel", "genero": "masculino", "atributos": {"tiene_armadura": True, "vuela": True, "villano": False, "cabello_rojo": False, "cabello_azul": False, "heroe": True}, "puntuacion": 1},
            {"nombre": "Batman", "serie": "DC", "genero": "masculino", "atributos": {"tiene_armadura": True, "vuela": False, "villano": False, "cabello_negro": True, "heroe": True}, "puntuacion": 1},
            {"nombre": "Darth Vader", "serie": "Star Wars", "genero": "masculino", "atributos": {"villano": True, "tiene_armadura": True, "usa_espada": True, "heroe": False}, "puntuacion": 1},
            {"nombre": "Goku", "serie": "Dragon Ball", "genero": "masculino", "atributos": {"vuela": True, "cabello_negro": True, "villano": False, "heroe": True}, "puntuacion": 1},
            {"nombre": "Spider-Man", "serie": "Marvel", "genero": "masculino", "atributos": {"vuela": False, "usa_mascara": True, "villano": False, "heroe": True}, "puntuacion": 1},
            {"nombre": "Wonder Woman", "serie": "DC", "genero": "femenino", "atributos": {"heroe": True, "vuela": True, "villano": False, "cabello_negro": True}, "puntuacion": 1},
            {"nombre": "Harley Quinn", "serie": "DC", "genero": "femenino", "atributos": {"villano": True, "cabello_rubio": True, "arma": True, "heroe": False}, "puntuacion": 1},
            {"nombre": "Elsa", "serie": "Frozen", "genero": "femenino", "atributos": {"poder_hielo": True, "villano": False, "cabello_rubio": True, "heroe": True}, "puntuacion": 1},
            {"nombre": "Hermione", "serie": "Harry Potter", "genero": "femenino", "atributos": {"magia": True, "villano": False, "cabello_castaño": True, "heroe": True}, "puntuacion": 1},
            {"nombre": "Black Widow", "serie": "Marvel", "genero": "femenino", "atributos": {"heroe": True, "villano": False, "cabello_rojo": True, "arma": True}, "puntuacion": 1}
        ]
        guardar_personajes(personajes)
        return personajes

def guardar_personajes(personajes):
    with open("personajesPOP.json", "w", encoding="utf-8") as f:
        json.dump(personajes, f, indent=4, ensure_ascii=False)

def obtener_todas_caracteristicas(personajes):
    caracteristicas = set()
    for p in personajes:
        caracteristicas.update(p["atributos"].keys())
    return list(caracteristicas)

# =====================
# Lógica del juego
# =====================

def jugar():
    personajes = cargar_personajes()
    todas_caracteristicas = obtener_todas_caracteristicas(personajes)
    respuestas = {}
    negaciones = set()  # Para registrar características excluidas

    print("Bienvenido al juego de 'Adivina Quién' (versión cultura POP)")
    print("Responde con: si / no / nose")
    input("Presiona Enter para comenzar...")

    # Selección dinámica de preguntas
    random.shuffle(todas_caracteristicas)
    for caracteristica in todas_caracteristicas:
        # Si una característica contradictoria ya fue afirmada, no la preguntamos
        if caracteristica in negaciones:
            continue

        respuesta = input(f"¿Tu personage - '{caracteristica.replace('_', ' ')}'? ").lower()

        if respuesta == "si":
            respuestas[caracteristica] = True
            # Elimina atributos opuestos (ej: si dijo "cabello_rojo", quita otros colores)
            if "cabello" in caracteristica:
                negaciones.update([c for c in todas_caracteristicas if "cabello" in c and c != caracteristica])
            if caracteristica == "heroe":
                negaciones.add("villano")
            if caracteristica == "villano":
                negaciones.add("heroe")
        elif respuesta == "no":
            respuestas[caracteristica] = False
        elif respuesta == "nose":
            continue

    # Intentar adivinar
    posibles = []
    for p in personajes:
        coincidencias = all(
            p["atributos"].get(k) == v for k, v in respuestas.items() if k in p["atributos"]
        )
        if coincidencias:
            posibles.append(p)

    if posibles:
        posibles.sort(key=lambda x: -x["puntuacion"])
        print("\nCreo que tu personaje es...")
        print(f"🎯 {posibles[0]['nombre']} ({posibles[0]['serie']})")
        acierto = input("¿He adivinado correctamente? (si/no): ").lower()
        if acierto == "si":
            posibles[0]["puntuacion"] += 1
        else:
            agregar_personaje(personajes, respuestas)
    else:
        print("\nNo pude encontrar a tu personaje 😔")
        agregar_personaje(personajes, respuestas)

    guardar_personajes(personajes)

    # Reiniciar juego
    input("\nPresiona Enter para jugar de nuevo...")
    limpiar_pantalla()
    jugar()

# =====================
# Agregar nuevo personaje
# =====================

def agregar_personaje(personajes, respuestas):
    print("\nAgregar tu personaje al sistema.")
    nombre = input("Nombre del personaje: ")
    serie = input("Serie o universo al que pertenece: ")
    genero = input("Género (masculino/femenino): ").lower()

    # Agregar una nueva característica que el usuario elija
    nueva_caract = input("Agrega una nueva característica que lo describa (ej: usa_gorra, canta, etc.): ").strip().lower()
    respuestas[nueva_caract] = True

    nuevo = {
        "nombre": nombre,
        "serie": serie,
        "genero": genero,
        "atributos": respuestas,
        "puntuacion": 1
    }
    personajes.append(nuevo)
    print(f"✅ {nombre} ha sido agregado correctamente al sistema.")

# =====================
# Ejecutar
# =====================
if __name__ == "__main__":
    limpiar_pantalla()
    jugar()
