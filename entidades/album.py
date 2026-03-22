#album.py

from entidades.agrupacion import Agrupacion

class Album(Agrupacion):
    def __init__(self, artista, nombre, año):
        # En un álbum, el creador siempre es el artista
        super().__init__(artista, nombre)
        self.año = año

    def añadir_cancion(self, cancion):
        #Solo permite añadir canciones si el artista de la cancion es el mismo que el del album
        if cancion.artista == self.creador:
            exito = self._insertar_item(cancion)
            if exito:
                print(f"Cancion '{cancion.titulo}' añadida al album '{self.nombre}'.")
            else:
                print(f"La cancion '{cancion.titulo}' ya existe en este album.")
        else:
            print(f"Error: No se puede añadir '{cancion.titulo}'. El artista no coincide con {self.creador}.")

    def eliminar_cancion(self, cancion):
        exito = self._extraer_item(cancion)
        if exito:
            print(f"Cancion '{cancion.titulo}' eliminada del album '{self.nombre}'.")
        else:
            print(f"La cancion '{cancion.titulo}' no se encuentra en este album.")

    def mostrar_lista_canciones(self):
        print(f"--- Lista de canciones: {self.nombre} ({self.año}) ---")
        if not self.lista_contenido:
            print("El album esta vacio.")
        else:
            for i, cancion in enumerate(self.lista_contenido, 1):
                print(f"{i}. {cancion.titulo} - {cancion.duracion}s")
        print("-" * 30)

    def mostrar_info(self):
        #Mostramos la ficha técnica del album
        print(f"--- Album: {self.nombre} ---")
        print(f"Artista: {self.creador}")
        print(f"Año de lanzamiento: {self.año}")
        print(f"Numero de pistas: {len(self.lista_contenido)}")
        print(f"Duracion total: {self.obtener_duracion_total()} segundos")
        print("-" * 30)