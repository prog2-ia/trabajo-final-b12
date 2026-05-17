# main.py — Spotify Clone
# Punto de entrada del programa. Contiene toda la lógica de menús y
# coordina el uso de todas las clases del proyecto.
# No contiene lógica de negocio — eso está en entidades/ y servicios/

from entidades.cancion import Cancion, CalidadInsuficienteError
from entidades.podcast import Podcast
from entidades.album import Album
from entidades.playlist import Playlist
from data.catalogo import canciones
from servicios.reproductor import Reproductor
from servicios.buscador import Buscador
from auth.gestor_auth import GestorAuth
from datetime import datetime   # para marcar la fecha/hora en los ficheros
import os                       # para crear carpetas y comprobar si existen ficheros


# ── ESTADO GLOBAL ────────────────────────────────────────────────────────────
# Variables que viven durante toda la sesión del programa.
# Al cerrar el programa, todo esto desaparece de memoria — por eso usamos
# ficheros para guardar el historial y los errores de forma permanente.

biblioteca  = list(canciones)   # list() hace una COPIA del catálogo, no lo modifica
playlists   = []                 # se crean durante la sesión
albumes     = []                 # se crean durante la sesión
reproductor = Reproductor()      # una sola instancia — patrón de uso único
buscador    = Buscador(biblioteca)  # recibe la biblioteca como referencia viva
gestor_auth = GestorAuth()       # gestiona login/registro de usuarios


# ── RUTAS DE FICHEROS ─────────────────────────────────────────────────────────
# Centralizamos las rutas aquí arriba para cambiarlas en un solo sitio si hace falta.
# Temario T10: ficheros de texto con open(), modos 'r', 'w', 'a' y encoding utf-8.

RUTA_HISTORIAL = "data/historial.txt"    # append — acumula reproducciones
RUTA_ERRORES   = "persistencia/errores.txt"  # append — acumula errores de bitrate


# ── FUNCIONES AUXILIARES ──────────────────────────────────────────────────────
# Estas funciones resuelven problemas genéricos que se repiten en varios menús.
# No pertenecen a ninguna clase porque actúan sobre el flujo del programa,
# no sobre objetos concretos — por eso están aquí y no en servicios/.

def pedir_int(mensaje, minimo=None, maximo=None):
    """
    Pide un número entero por consola con validación de rango.
    El bucle while True repite hasta que el usuario introduce un valor válido.
    El try/except captura el ValueError que lanza int() si recibe letras.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Mínimo: {minimo}")
                continue        # vuelve al inicio del while sin salir
            if maximo is not None and valor > maximo:
                print(f"Máximo: {maximo}")
                continue
            return valor        # solo salimos si el valor pasa todas las validaciones
        except ValueError:
            print("Introduce un número entero.")

def pedir_float(mensaje):
    """Igual que pedir_int pero acepta decimales. Usado para la duración."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Introduce un número, ej.: 3.5")

def pedir_datos_comunes():
    """
    Recoge los 6 campos que comparten Cancion y Podcast.
    Centralizar esto evita duplicar código en aniadir_cancion() y aniadir_podcast().
    El 'or "default.jpg"' asigna un valor por defecto si el usuario pulsa Enter vacío.
    La list comprehension convierte "Bad Bunny, Shakira" en ["Bad Bunny", "Shakira"].
    """
    titulo        = input("Título: ").strip()
    autor         = input("Autor: ").strip()
    colabs_raw    = input("Colaboradores (coma o Enter para ninguno): ").strip()
    # Si colabs_raw está vacío, colaboradores = [] en vez de [""]
    colaboradores = [c.strip() for c in colabs_raw.split(",")] if colabs_raw else []
    portada       = input("Portada (archivo o URL): ").strip() or "default.jpg"
    duracion      = pedir_float("Duración (segundos): ")
    bitrate       = pedir_int("Bitrate (kbps): ", minimo=32, maximo=320)
    return titulo, autor, colaboradores, duracion, portada, bitrate

def separador(titulo=""):
    """
    Imprime una línea decorativa con título opcional.
    Hace el menú más legible visualmente sin lógica de negocio.
    """
    ancho = 44
    if titulo:
        print(f"\n{'─'*2} {titulo} {'─'*(ancho - len(titulo) - 4)}")
    else:
        print("─" * ancho)

def pausar():
    """
    Espera a que el usuario pulse Enter antes de volver al menú.
    Sin esto, el menú aparecería inmediatamente y el usuario no podría
    leer el resultado de la operación anterior.
    """
    input("\n  [Enter para continuar]")


# ── BIBLIOTECA ────────────────────────────────────────────────────────────────

def aniadir_cancion():
    separador("Nueva Canción")
    genero = input("Género: ").strip()
    titulo, autor, colaboradores, duracion, portada, bitrate = pedir_datos_comunes()
    try:
        cancion = Cancion(titulo, autor, colaboradores, duracion, portada, bitrate, genero)
        biblioteca.append(cancion)
        print(f"\n✅ '{titulo}' añadida a la biblioteca.")
    except CalidadInsuficienteError as e:
        # CalidadInsuficienteError es nuestra excepción personalizada (hereda de ValueError)
        # Se lanza en Cancion.__init__() si el bitrate < 64kbps
        # Además de mostrar el error, lo guardamos en fichero para tener registro
        print(f"\n❌ No se pudo añadir: {e}")
        registrar_error(titulo, bitrate, str(e))

def aniadir_podcast():
    separador("Nuevo Podcast")
    tema = input("Tema: ").strip()
    titulo, autor, colaboradores, duracion, portada, bitrate = pedir_datos_comunes()
    # Podcast no lanza excepción — capa el bitrate a 98kbps internamente en su __init__
    podcast = Podcast(titulo, autor, colaboradores, duracion, portada, bitrate, tema)
    biblioteca.append(podcast)
    print(f"\n✅ Podcast '{titulo}' añadido.")

def ver_biblioteca():
    separador(f"BIBLIOTECA — {len(biblioteca)} elemento(s)")
    if not biblioteca:
        print("  📭 Tu biblioteca está vacía.")
        pausar()
        return
    for i, item in enumerate(biblioteca, 1):
        # print(item) llama automáticamente al __str__ de cada objeto
        # Polimorfismo: Cancion y Podcast tienen __str__ distinto pero el bucle es el mismo
        print(f"\n[{i}] {item}")
        print("─" * 40)
    pausar()


# ── BUSCADOR ──────────────────────────────────────────────────────────────────

def menu_busqueda():
    while True:
        separador("BUSCADOR")
        print("  1. Buscar por título / autor")
        print("  2. Buscar por género")
        print("  3. Buscar por artista (incluye colaboraciones)")
        print("  4. Buscar por duración")
        print("  5. Filtrar solo canciones")
        print("  6. Filtrar solo podcasts")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == "0":
            break
        elif op == "1":
            texto = input("  Buscar: ").strip()
            resultados = buscador.buscar(texto)
            buscador.mostrar_resultados(resultados, texto)
        elif op == "2":
            genero = input("  Género: ").strip()
            resultados = buscador.buscar_por_genero(genero)
            buscador.mostrar_resultados(resultados, genero)
        elif op == "3":
            artista = input("  Artista: ").strip()
            resultados = buscador.buscar_por_artista(artista)
            buscador.mostrar_resultados(resultados, artista)
        elif op == "4":
            min_s = pedir_int("  Duración mínima (seg): ", minimo=0)
            max_s = pedir_int("  Duración máxima (seg): ", minimo=min_s)
            resultados = buscador.buscar_por_duracion(min_s, max_s)
            buscador.mostrar_resultados(resultados, f"{min_s}-{max_s}s")
        elif op == "5":
            resultados = buscador.buscar_por_tipo(Cancion)
            buscador.mostrar_resultados(resultados, "Canciones")
        elif op == "6":
            resultados = buscador.buscar_por_tipo(Podcast)
            buscador.mostrar_resultados(resultados, "Podcasts")
        else:
            print("⚠️  Opción no válida.")

        pausar()


# ── PLAYLISTS ─────────────────────────────────────────────────────────────────

def _seleccionar_item_biblioteca(mensaje="Número de elemento"):
    """
    Muestra la biblioteca numerada y devuelve el objeto elegido.
    El guion bajo inicial (_) indica que es una función de uso interno
    de este módulo — convención Python para 'privado a nivel de módulo'.
    Devuelve None si el usuario cancela (elige 0).
    """
    if not biblioteca:
        print(" La biblioteca está vacía.")
        return None
    for i, item in enumerate(biblioteca, 1):
        print(f"  {i:>3}. {item._titulo} — {item._autor}")
    idx = pedir_int(f"  {mensaje} (0 para cancelar): ", minimo=0, maximo=len(biblioteca))
    return biblioteca[idx - 1] if idx else None  # idx-1 porque las listas empiezan en 0

def _seleccionar_playlist():
    """Igual que _seleccionar_item_biblioteca pero para la lista de playlists."""
    if not playlists:
        print("  No tienes playlists creadas.")
        return None
    for i, pl in enumerate(playlists, 1):
        # len(pl) funciona porque Playlist implementa __len__ — temario T06
        print(f"  {i}. {pl.nombre} ({len(pl)} elementos)")
    idx = pedir_int("  Número de playlist (0 cancelar): ", minimo=0, maximo=len(playlists))
    return playlists[idx - 1] if idx else None

def menu_playlists():
    while True:
        separador("PLAYLISTS")
        print("  1. Crear nueva playlist")
        print("  2. Añadir canción a playlist")
        print("  3. Ver playlist")
        print("  4. Cambiar visibilidad (pública / privada)")
        print("  5. Fusionar dos playlists")
        print("  6. Eliminar canción de playlist")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == "0":
            break
        elif op == "1":
            nombre = input("  Nombre de la playlist: ").strip()
            estado = input("  Visibilidad (publica/privada) [publica]: ").strip() or "publica"
            # Si hay sesión activa usamos el username real, si no "Invitado"
            creador = gestor_auth.usuario_actual.username if gestor_auth.hay_sesion else "Invitado"
            pl = Playlist(creador, nombre, estado)
            playlists.append(pl)
            print(f"  ✅ Playlist '{nombre}' creada.")
        elif op == "2":
            pl = _seleccionar_playlist()
            if pl:
                item = _seleccionar_item_biblioteca("Elemento a añadir")
                if item:
                    pl.añadir_contenido(item)
                    print(f"  ✅ Añadido '{item._titulo}' a '{pl.nombre}'.")
        elif op == "3":
            pl = _seleccionar_playlist()
            if pl:
                print(f"\n{pl}")    # llama a Playlist.__str__()
        elif op == "4":
            pl = _seleccionar_playlist()
            if pl:
                pl.cambiar_visibilidad()
                print(f"  ✅ Playlist ahora es {pl.estado}.")
        elif op == "5":
            if len(playlists) < 2:
                print("  ℹ️  Necesitas al menos dos playlists para fusionar.")
            else:
                print("  Primera playlist:")
                pl1 = _seleccionar_playlist()
                print("  Segunda playlist:")
                pl2 = _seleccionar_playlist()
                if pl1 and pl2 and pl1 is not pl2:
                    # pl1 + pl2 funciona porque Playlist implementa __add__ — temario T06
                    nueva = pl1 + pl2
                    playlists.append(nueva)
                    print(f"  ✅ Creada '{nueva.nombre}' con {len(nueva)} elementos.")
        elif op == "6":
            pl = _seleccionar_playlist()
            if pl and pl.lista_contenido:
                print(f"\n  Contenido de '{pl.nombre}':")
                for i, item in enumerate(pl.lista_contenido, 1):
                    print(f"    {i}. {item._titulo}")
                idx = pedir_int("  Número a eliminar (0 cancelar): ", minimo=0, maximo=len(pl.lista_contenido))
                if idx:
                    item = pl.lista_contenido[idx - 1]
                    pl.eliminar_contenido(item)
        else:
            print("⚠️  Opción no válida.")

        pausar()


# ── ÁLBUMES ───────────────────────────────────────────────────────────────────

def _seleccionar_album():
    """Muestra los álbumes creados y devuelve el elegido. None si cancela."""
    if not albumes:
        print("  No hay álbumes creados.")
        return None
    for i, al in enumerate(albumes, 1):
        print(f"  {i}. {al.nombre} — {al.artista} ({al.año})")
    idx = pedir_int("  Número de álbum (0 cancelar): ", minimo=0, maximo=len(albumes))
    return albumes[idx - 1] if idx else None

def menu_albumes():
    while True:
        separador("ÁLBUMES")
        print("  1. Crear nuevo álbum")
        print("  2. Añadir canción al álbum")
        print("  3. Ver álbum")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == "0":
            break
        elif op == "1":
            artista = input("  Artista: ").strip()
            nombre  = input("  Nombre del álbum: ").strip()
            año     = pedir_int("  Año: ", minimo=1900, maximo=2100)
            al = Album(artista, nombre, año)
            albumes.append(al)
            print(f"  ✅ Álbum '{nombre}' creado.")
        elif op == "2":
            al = _seleccionar_album()
            if al:
                # Buscamos solo canciones del artista del álbum para mantener coherencia
                canciones_artista = buscador.buscar_por_artista(al.artista)
                if not canciones_artista:
                    print(f"  ℹ️  No hay canciones de '{al.artista}' en la biblioteca.")
                else:
                    print(f"\n  Canciones de '{al.artista}':")
                    for i, c in enumerate(canciones_artista, 1):
                        print(f"    {i}. {c._titulo}")
                    idx = pedir_int("  Número a añadir (0 cancelar): ", minimo=0, maximo=len(canciones_artista))
                    if idx:
                        al.añadir_cancion(canciones_artista[idx - 1])
        elif op == "3":
            al = _seleccionar_album()
            if al:
                print(f"\n{al}")    # llama a Album.__str__()
        else:
            print("⚠️  Opción no válida.")

        pausar()


# ── REPRODUCTOR ───────────────────────────────────────────────────────────────

def menu_reproductor():
    while True:
        separador("REPRODUCTOR")
        print("  1. Reproducir canción de la biblioteca")
        print("  2. Añadir canción a la cola")
        print("  3. Siguiente pista")
        print("  4. Cargar playlist en cola")
        print("  5. Cargar álbum en cola")
        print("  6. Ver cola")
        print("  7. Vaciar cola")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == "0":
            break
        elif op == "1":
            item = _seleccionar_item_biblioteca("Elemento a reproducir")
            if item:
                reproductor.cargar_pista(item)
                # Registramos en fichero DESPUÉS de reproducir, no antes
                # Si cargar_pista() fallase, no querríamos registrar nada
                registrar_en_historial(item)
        elif op == "2":
            item = _seleccionar_item_biblioteca("Elemento a añadir a la cola")
            if item:
                reproductor.agregar_a_cola(item)
        elif op == "3":
            reproductor.siguiente()
        elif op == "4":
            pl = _seleccionar_playlist()
            if pl:
                reproductor.cargar_agrupacion(pl)
        elif op == "5":
            al = _seleccionar_album()
            if al:
                reproductor.cargar_agrupacion(al)
        elif op == "6":
            reproductor.ver_cola()
        elif op == "7":
            reproductor.vaciar_cola()
        else:
            print("⚠️  Opción no válida.")

        pausar()


# ── AUTENTICACIÓN ─────────────────────────────────────────────────────────────

def menu_auth():
    while True:
        separador("CUENTA")
        if gestor_auth.hay_sesion:
            print(f"  Sesión activa: {gestor_auth.usuario_actual.username}")
            print("  1. Cerrar sesión")
        else:
            print("  1. Iniciar sesión")
            print("  2. Registrarse")
        print("  0. Volver")
        op = input("\n  Opción: ").strip()

        if op == "0":
            break
        elif op == "1":
            if gestor_auth.hay_sesion:
                gestor_auth.logout()
            else:
                username = input("  Usuario: ").strip()
                password = input("  Contraseña: ").strip()
                gestor_auth.login(username, password)
        elif op == "2" and not gestor_auth.hay_sesion:
            username = input("  Nuevo usuario: ").strip()
            password = input("  Contraseña: ").strip()
            gestor_auth.registrar(username, password)
        else:
            print("⚠️  Opción no válida.")

        pausar()


# ── FICHEROS — HISTORIAL ──────────────────────────────────────────────────────
# Temario T10: lectura y escritura de ficheros de texto.
# Usamos 'with open()' siempre — garantiza el cierre aunque haya un error.
# Usamos encoding='utf-8' siempre — evita problemas con tildes y ñ en Linux/Windows.

def registrar_en_historial(item):
    """
    Añade UNA línea al historial cada vez que se reproduce algo.
    Modo 'a' (append): añade al final sin borrar lo anterior.
    type(item).__name__ devuelve 'Cancion' o 'Podcast' según el objeto real
    — usa type() del temario T03 para inspección de objetos.
    :<8 y :<25 son formato de alineación — rellena con espacios hasta N caracteres.
    """
    tipo  = type(item).__name__
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    linea = f"{fecha} | {tipo:<8} | {item._titulo:<25} | {item._autor}\n"

    # exist_ok=True evita error si la carpeta ya existe
    os.makedirs(os.path.dirname(RUTA_HISTORIAL), exist_ok=True)

    with open(RUTA_HISTORIAL, 'a', encoding='utf-8') as f:
        f.write(linea)

def ver_historial():
    """
    Lee el historial completo y lo muestra línea a línea.
    Modo 'r' (lectura): solo lee, no modifica el fichero.
    .readlines() devuelve una lista con cada línea como elemento — temario T10.
    .strip() elimina el \\n del final de cada línea antes de imprimir.
    """
    separador("HISTORIAL DE REPRODUCCIONES")

    if not os.path.exists(RUTA_HISTORIAL):
        # os.path.exists() comprueba si el fichero existe antes de intentar abrirlo
        # Evita el FileNotFoundError en la primera ejecución
        print("  📭 Aún no hay reproducciones registradas.")
        pausar()
        return

    with open(RUTA_HISTORIAL, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    if not lineas:
        print("  📭 El historial está vacío.")
    else:
        print(f"  Total reproducciones: {len(lineas)}\n")
        for linea in lineas:
            print(f"  {linea.strip()}")

    pausar()


# ── FICHEROS — ERRORES ────────────────────────────────────────────────────────

def registrar_error(titulo, bitrate, motivo):
    """
    Guarda en fichero cada intento fallido de añadir una canción.
    Se llama desde aniadir_cancion() cuando salta CalidadInsuficienteError.
    Modo 'a': acumula errores sin sobreescribir — igual que el historial.
    Útil para detectar patrones: si siempre falla el mismo bitrate, hay un bug.
    """
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
    linea = f"{fecha} | [ERROR] '{titulo}' — {bitrate}kbps — {motivo}\n"

    os.makedirs(os.path.dirname(RUTA_ERRORES), exist_ok=True)

    with open(RUTA_ERRORES, 'a', encoding='utf-8') as f:
        f.write(linea)


# ── MENÚ PRINCIPAL ────────────────────────────────────────────────────────────
# Punto de entrada real del programa.
# El bloque if __name__ == "__main__" asegura que menu() solo se ejecuta
# si lanzamos este archivo directamente (python main.py),
# no si otro archivo lo importa como módulo.

def menu():
    print("\n" + "═" * 44)
    print("   🎵  SPOTIFY CLONE  —  Artur & Pepe")
    print(f"   Catálogo cargado: {len(biblioteca)} canciones")
    print("═" * 44)

    while True:
        sesion_str = f"[{gestor_auth.usuario_actual.username}]" if gestor_auth.hay_sesion else "[Invitado]"
        print(f"\n  {sesion_str}")
        print("  1. 📚 Biblioteca")
        print("  2. ➕ Añadir canción")
        print("  3. 🎙️  Añadir podcast")
        print("  4. 🔍 Buscar")
        print("  5. 🎵 Playlists")
        print("  6. 💿 Álbumes")
        print("  7. 🎧 Reproductor")
        print("  8. 👤 Cuenta")
        print("  9. 📋 Historial")
        print("  0. Salir")

        op = input("\n  Elige una opción: ").strip()

        if   op == "0": print("\n👋 ¡Hasta luego!\n"); break
        elif op == "1": ver_biblioteca()
        elif op == "2": aniadir_cancion()
        elif op == "3": aniadir_podcast()
        elif op == "4": menu_busqueda()
        elif op == "5": menu_playlists()
        elif op == "6": menu_albumes()
        elif op == "7": menu_reproductor()
        elif op == "8": menu_auth()
        elif op == "9": ver_historial()
        else: print("⚠️  Opción no válida. Elige entre 0 y 9.")


if __name__ == "__main__":
    menu()