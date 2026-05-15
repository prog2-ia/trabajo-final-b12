from entidades.cancion import Cancion
# main.py — Spotify Clone
# Punto de entrada principal. Conecta todos los módulos del proyecto.

from entidades.cancion import Cancion, CalidadInsuficienteError
from entidades.podcast import Podcast
from entidades.album import Album
from entidades.playlist import Playlist
from data.catalogo import canciones
from servicios.reproductor import Reproductor
from servicios.buscador import Buscador
from auth.gestor_auth import GestorAuth

# ── ESTADO GLOBAL ─────────────────────────────────────────────────────────────

biblioteca = list(canciones)   # cargamos el catálogo inicial
playlists = []                  # playlists creadas durante la sesión
albumes = []                    # álbumes creados durante la sesión
reproductor = Reproductor()
buscador = Buscador(biblioteca)
gestor_auth = GestorAuth()


# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS DE ENTRADA
# ══════════════════════════════════════════════════════════════════════════════

def pedir_int(mensaje, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo is not None and valor < minimo:
                print(f"Mínimo: {minimo}")
                continue
            if maximo is not None and valor > maximo:
                print(f"Máximo: {maximo}")
                continue
            return valor
        except ValueError:
            print("Introduce un número entero.")

def pedir_float(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Introduce un número, ej.: 3.5")

def pedir_datos_comunes():
    titulo      = input("Título: ").strip()
    autor       = input("Autor: ").strip()
    colabs_raw  = input("Colaboradores (coma o Enter para ninguno): ").strip()
    colaboradores = [c.strip() for c in colabs_raw.split(",")] if colabs_raw else []
    portada     = input("Portada (archivo o URL): ").strip() or "default.jpg"
    duracion    = pedir_float("Duración (segundos): ")
    bitrate     = pedir_int("Bitrate (kbps): ", minimo=32, maximo=320)
    return titulo, autor, colaboradores, duracion, portada, bitrate

def separador(titulo=""):
    ancho = 44
    if titulo:
        print(f"\n{'─'*2} {titulo} {'─'*(ancho - len(titulo) - 4)}")
    else:
        print("─" * ancho)

def pausar():
    input("\n  [Enter para continuar]")


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO: CONTENIDO (Canciones y Podcasts)
# ══════════════════════════════════════════════════════════════════════════════

def aniadir_cancion():
    separador("Nueva Canción")
    genero = input("Género: ").strip()
    titulo, autor, colaboradores, duracion, portada, bitrate = pedir_datos_comunes()
    try:
        cancion = Cancion(titulo, autor, colaboradores, duracion, portada, bitrate, genero)
        biblioteca.append(cancion)
        print(f"\n✅ '{titulo}' añadida a la biblioteca.")
    except CalidadInsuficienteError as e:
        print(f"\n❌ No se pudo añadir: {e}")

def aniadir_podcast():
    separador("Nuevo Podcast")
    tema = input("Tema: ").strip()
    titulo, autor, colaboradores, duracion, portada, bitrate = pedir_datos_comunes()
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
        print(f"\n[{i}] {item}")
        print("─" * 40)
    pausar()


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO: BUSCADOR
# ══════════════════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO: PLAYLISTS
# ══════════════════════════════════════════════════════════════════════════════

def _seleccionar_item_biblioteca(mensaje="Número de elemento"):
    """Muestra la biblioteca numerada y devuelve el item elegido."""
    if not biblioteca:
        print("  📭 La biblioteca está vacía.")
        return None
    for i, item in enumerate(biblioteca, 1):
        print(f"  {i:>3}. {item._titulo} — {item._autor}")
    idx = pedir_int(f"  {mensaje} (0 para cancelar): ", minimo=0, maximo=len(biblioteca))
    return biblioteca[idx - 1] if idx else None

def _seleccionar_playlist():
    if not playlists:
        print("  ℹ️  No tienes playlists creadas.")
        return None
    for i, pl in enumerate(playlists, 1):
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
                print(f"\n{pl}")
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


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO: ÁLBUMES
# ══════════════════════════════════════════════════════════════════════════════

def _seleccionar_album():
    if not albumes:
        print("  ℹ️  No hay álbumes creados.")
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
                print(f"\n{al}")
        else:
            print("⚠️  Opción no válida.")

        pausar()


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO: REPRODUCTOR
# ══════════════════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════════════════
#  MÓDULO: AUTENTICACIÓN
# ══════════════════════════════════════════════════════════════════════════════

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


# ══════════════════════════════════════════════════════════════════════════════
#  MENÚ PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

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
        else: print("⚠️  Opción no válida. Elige entre 0 y 8.")


if __name__ == "__main__":
    menu()