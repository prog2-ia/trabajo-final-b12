from entidades.cancion import Cancion
from entidades.podcast import Podcast

biblioteca = []

def pedir_datos_comunes():
    """Pide los campos que comparten Cancion y Podcast"""
    titulo = input("Título: ")
    autor = input("Autor: ")
    colaboradores_raw = input("Colaboradores (separados por coma, o Enter para ninguno): ")
    colaboradores = [c.strip() for c in colaboradores_raw.split(",")] if colaboradores_raw else []
    portada = input("Portada (URL o nombre del archivo): ")

    while True:
        try:
            duracion = float(input("Duración (en minutos): "))
            break
        except ValueError:
            print("⚠️  Escribe un número, por ejemplo: 3.5")

    while True:
        try:
            bitrate = int(input("Bitrate del archivo (kbps): "))
            break
        except ValueError:
            print("⚠️  Escribe un número entero, por ejemplo: 128")

    return titulo, autor, colaboradores, duracion, portada, bitrate


def aniadir_cancion():
    print("\n--- Nueva Canción ---")
    genero = input("Género: ")
    titulo, autor, colaboradores, duracion, portada, bitrate = pedir_datos_comunes()

    try:
        cancion = Cancion(titulo, autor, colaboradores, duracion, portada, bitrate, genero)
        biblioteca.append(cancion)
        print(f"✅ '{titulo}' añadida a la biblioteca.")
    except ValueError as e:
        print(f"❌ No se pudo añadir: {e}")


def aniadir_podcast():
    print("\n--- Nuevo Podcast ---")
    tema = input("Tema del podcast: ")
    titulo, autor, colaboradores, duracion, portada, bitrate = pedir_datos_comunes()

    podcast = Podcast(titulo, autor, colaboradores, duracion, portada, bitrate, tema)
    biblioteca.append(podcast)
    print(f"✅ Podcast '{titulo}' añadido a la biblioteca.")


def ver_biblioteca():
    if not biblioteca:
        print("\n📭 Tu biblioteca está vacía.")
        return

    print(f"\n{'='*40}")
    print(f"  BIBLIOTECA — {len(biblioteca)} elemento(s)")
    print(f"{'='*40}")

    for i, elemento in enumerate(biblioteca, start=1):
        print(f"\n[{i}] {elemento}")       # llama a __str__ de cada clase
        elemento.reproducir()              # polimorfismo: cada clase lo hace distinto
        print("-" * 40)


def menu():
    while True:
        print("\n🎵 SPOTIFY CLONE")
        print("1. Añadir Canción")
        print("2. Añadir Podcast")
        print("3. Ver Biblioteca")
        print("4. Salir")

        opcion = input("\nElige una opción: ").strip()

        if opcion == "1":
            aniadir_cancion()
        elif opcion == "2":
            aniadir_podcast()
        elif opcion == "3":
            ver_biblioteca()
        elif opcion == "4":
            print("👋 ¡Hasta luego!")
            break
        else:
            print("⚠️  Opción no válida. Elige entre 1 y 4.")


if __name__ == "__main__":
    menu()