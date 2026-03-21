#playlist.py

from agrupacion import Agrupacion

class Playlist(Agrupacion):
    def __init__(self, creador, nombre, estado="publica"):
        super().__init__(creador, nombre)
        self.estado = estado

    def añadir_contenido(self, contenido):
        #Llama al metodo del padre
        exito = self._insertar_item(contenido)
        if exito:
            print(f"Contenido '{contenido.titulo}' añadido a la playlist {self.nombre}.")
        else:
            print(f"El contenido '{contenido.titulo}' ya se encuentra en esta playlist.")

    def eliminar_contenido(self, contenido):
        #Llama al metodo del padre
        exito = self._extraer_item(contenido)
        if exito:
            print(f"Contenido '{contenido.titulo}' eliminado de la playlist {self.nombre}.")
        else:
            print(f"No se pudo eliminar: '{contenido.titulo}' no esta en la playlist.")

    def cambiar_visibilidad(self):
        """Alterna el estado entre publica y privada."""
        self.estado = "privada" if self.estado == "publica" else "publica"
        print(f"La playlist '{self.nombre}' ahora es {self.estado}.")

    def mostrar_info(self):
        """Muestra un resumen detallado de la playlist."""
        print(f"--- Playlist: {self.nombre} ---")
        print(f"Creador: {self.creador}")
        print(f"Estado: {self.estado}")
        print(f"Total elementos: {len(self.lista_contenido)}")
        print(f"Duracion total: {self.obtener_duracion_total()} segundos")
        print("-" * 30)

