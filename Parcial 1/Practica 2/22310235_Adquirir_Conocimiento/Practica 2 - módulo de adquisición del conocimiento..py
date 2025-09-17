#Su objetivo es demostrar un módulo de adquisición de conocimiento,
#la capacidad de aprender nuevas respuestas durante la interacción.

import json
import os

# Archivo donde se guarda el conocimiento
DB_FILE = "conocimiento_tienda.json"

# Base de conocimiento inicial
conocimiento_base = {
    "hola": "Dependiente: Hola, bienvenido a la tienda. ¿En qué puedo ayudarle?",
    "tienes ofertas": "Dependiente: Sí, hoy tenemos descuentos en frutas y productos de limpieza.",
    "gracias": "Dependiente: Gracias a usted por visitarnos."
}

# Cargar base de datos (si existe)
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        conocimiento = json.load(f)
else:
    conocimiento = conocimiento_base.copy()

def guardar_conocimiento():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(conocimiento, f, indent=4, ensure_ascii=False)

print("Chat Dependiente - Cliente")
print("Escriba 'salir' para terminar.\n")

while True:
    pregunta = input("Cliente: ").strip().lower()
    if pregunta == "salir":
        print("Dependiente: Gracias por su visita. Que tenga un buen día.")
        break

    if pregunta in conocimiento:
        print(conocimiento[pregunta])
    else:
        print("Dependiente: Puede repetirlo.")
        nueva_respuesta = input("Dependiente: ¿Qué debería responder en este caso? ")
        conocimiento[pregunta] = "Dependiente: " + nueva_respuesta
        guardar_conocimiento()
        print("Dependiente: Gracias, ahora lo recordaré.")
