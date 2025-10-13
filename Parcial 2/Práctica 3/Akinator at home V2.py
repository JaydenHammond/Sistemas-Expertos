import json
import os

DATA_FILE = "personajes.json"

class Personaje:
    def __init__(self, nombre, genero, serie, atributos, veces_elegido=0):
        self.nombre = nombre
        self.genero = genero
        self.serie = serie
        self.atributos = atributos
        self.veces_elegido = veces_elegido

    def coincide(self, respuestas):
        """Cuenta cuántas respuestas coinciden con este personaje."""
        return sum(
            1 for k, v in respuestas.items()
            if k in self.atributos and self.atributos[k] == v
        )


class JuegoAdivinaQuien:
    def __init__(self):
        self.personajes = self.cargar_personajes()
        self.preguntas, self.caracteristicas = self.generar_preguntas_existentes()

    def generar_preguntas_existentes(self):
        """Crea listas de preguntas y claves a partir de los personajes cargados."""
        claves = set()
        for p in self.personajes:
            claves.update(p.atributos.keys())

        traducciones = {
            "cabello_oscuro": "¿Tiene cabello oscuro?",
            "usa_lentes": "¿Usa lentes?",
            "es_heroe": "¿Es un héroe o heroína?",
            "es_animado": "¿Pertenece a una serie animada?",
            "tiene_poderes": "¿Tiene poderes sobrenaturales?",
            "es_humano": "¿Es humano?",
            "tiene_traje": "¿Tiene un traje icónico?",
            "es_villano": "¿Es villano o villana?"
        }

        preguntas = []
        caracteristicas = {}
        for clave in claves:
            pregunta = traducciones.get(clave, f"¿{clave.replace('_', ' ')}?")
            preguntas.append(pregunta)
            caracteristicas[pregunta] = clave

        return preguntas, caracteristicas

    def cargar_personajes(self):
        """Carga personajes desde archivo o crea iniciales."""
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Personaje(**p) for p in data]
        else:
            personajes_iniciales = [
                Personaje("Iron Man", "Masculino", "Marvel",
                          {"cabello_oscuro": True, "usa_lentes": False, "es_heroe": True,
                           "es_animado": False, "tiene_poderes": False, "es_humano": True,
                           "tiene_traje": True, "es_villano": False}),
                Personaje("Batman", "Masculino", "DC Comics",
                          {"cabello_oscuro": True, "usa_lentes": False, "es_heroe": True,
                           "es_animado": False, "tiene_poderes": False, "es_humano": True,
                           "tiene_traje": True, "es_villano": False}),
                Personaje("Homero Simpson", "Masculino", "Los Simpson",
                          {"cabello_oscuro": False, "usa_lentes": False, "es_heroe": False,
                           "es_animado": True, "tiene_poderes": False, "es_humano": True,
                           "tiene_traje": False, "es_villano": False}),
                Personaje("Darth Vader", "Masculino", "Star Wars",
                          {"cabello_oscuro": False, "usa_lentes": False, "es_heroe": False,
                           "es_animado": False, "tiene_poderes": True, "es_humano": False,
                           "tiene_traje": True, "es_villano": True}),
                Personaje("Harry Potter", "Masculino", "Harry Potter",
                          {"cabello_oscuro": True, "usa_lentes": True, "es_heroe": True,
                           "es_animado": False, "tiene_poderes": True, "es_humano": True,
                           "tiene_traje": False, "es_villano": False}),
                Personaje("Wonder Woman", "Femenino", "DC Comics",
                          {"cabello_oscuro": True, "usa_lentes": False, "es_heroe": True,
                           "es_animado": False, "tiene_poderes": True, "es_humano": True,
                           "tiene_traje": True, "es_villano": False}),
                Personaje("Elsa", "Femenino", "Frozen",
                          {"cabello_oscuro": False, "usa_lentes": False, "es_heroe": True,
                           "es_animado": True, "tiene_poderes": True, "es_humano": True,
                           "tiene_traje": True, "es_villano": False}),
                Personaje("Harley Quinn", "Femenino", "DC Comics",
                          {"cabello_oscuro": False, "usa_lentes": False, "es_heroe": False,
                           "es_animado": False, "tiene_poderes": False, "es_humano": True,
                           "tiene_traje": True, "es_villano": True}),
                Personaje("Hermione Granger", "Femenino", "Harry Potter",
                          {"cabello_oscuro": True, "usa_lentes": False, "es_heroe": True,
                           "es_animado": False, "tiene_poderes": True, "es_humano": True,
                           "tiene_traje": False, "es_villano": False}),
                Personaje("Lisa Simpson", "Femenino", "Los Simpson",
                          {"cabello_oscuro": False, "usa_lentes": False, "es_heroe": False,
                           "es_animado": True, "tiene_poderes": False, "es_humano": True,
                           "tiene_traje": False, "es_villano": False})
            ]
            self.guardar_personajes(personajes_iniciales)
            return personajes_iniciales

    def guardar_personajes(self, personajes=None):
        """Guarda todos los personajes."""
        if personajes is None:
            personajes = self.personajes
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([p.__dict__ for p in personajes], f, indent=4, ensure_ascii=False)

    def hacer_preguntas(self):
        """Realiza preguntas y guarda respuestas del usuario."""
        respuestas = {}
        for pregunta in self.preguntas:
            while True:
                r = input(f"{pregunta} (si/no/nose): ").strip().lower()
                if r in ["si", "no", "nose"]:
                    break
                print("Respuesta inválida. Usa 'si', 'no' o 'nose'.")
            if r != "nose":
                respuestas[self.caracteristicas[pregunta]] = (r == "si")
        return respuestas

    def adivinar(self, respuestas):
        """Trata de adivinar el personaje según las respuestas."""
        candidatos = sorted(
            self.personajes,
            key=lambda p: (-p.coincide(respuestas), -p.veces_elegido)
        )
        mejor = candidatos[0]
        print(f"\nCreo que tu personaje es... ¡{mejor.nombre} de {mejor.serie}!")
        conf = input("¿Adiviné correctamente? (si/no): ").strip().lower()

        if conf == "si":
            mejor.veces_elegido += 1
            self.guardar_personajes()
            print("¡Excelente! 😎\n")
        else:
            self.agregar_personaje(respuestas)

        # 🔁 Reiniciar el juego automáticamente
        self.reiniciar_juego()

    def agregar_personaje(self, respuestas):
        """Agrega un nuevo personaje usando las respuestas anteriores."""
        print("\nParece que tu personaje no está en la base de datos.")
        nombre = input("¿Cuál era el personaje?: ").strip()
        serie = input("¿De qué serie/película proviene?: ").strip()
        genero = input("¿Cuál es su género (Masculino/Femenino)?: ").strip().capitalize()

        atributos = respuestas.copy()

        # Nueva característica
        nueva_pregunta = input("\nAgrega una nueva característica para distinguirlo (ej. 'Tiene alas', 'Usa sombrero'): ").strip()
        clave_nueva = nueva_pregunta.lower().replace(" ", "_").replace("¿", "").replace("?", "")
        valor = input(f"¿{nueva_pregunta}? (si/no): ").strip().lower() == "si"

        atributos[clave_nueva] = valor

        # Guardar nueva pregunta
        self.preguntas.append(f"¿{nueva_pregunta}?")
        self.caracteristicas[f"¿{nueva_pregunta}?"] = clave_nueva

        nuevo = Personaje(nombre, genero, serie, atributos)
        self.personajes.append(nuevo)
        self.guardar_personajes()

        print(f"\nPersonaje '{nombre}' agregado correctamente y el sistema ha aprendido una nueva pregunta.\n")

    def reiniciar_juego(self):
        """Permite reiniciar o salir del juego."""
        while True:
            opcion = input("¿Quieres jugar otra vez? (si/no): ").strip().lower()
            if opcion in ["si", "no"]:
                break
        if opcion == "si":
            print("\n🔄 Reiniciando el juego...\n")
            self.jugar()
        else:
            print("\n👋 ¡Gracias por jugar Adivina Quién - Cultura POP!\n")

    def jugar(self):
        print("🎯 Bienvenido al juego Adivina Quién - Cultura POP 🎯\n")
        respuestas = self.hacer_preguntas()
        self.adivinar(respuestas)


if __name__ == "__main__":
    juego = JuegoAdivinaQuien()
    juego.jugar()
