#album.py

from entidades.agrupacion import Agrupacion

class Album(Agrupacion):
    def __init__(self, artista, nombre, año):
        # En un álbum, el creador siempre es el artista
        super().__init__(artista, nombre)
        self._año = año

    @property
    def artista(self):
        ##Alias para un album
        return self.creador

    @property
    def año(self):
        return self._año

    def añadir_cancion(self, cancion):
        #Solo permite añadir canciones si el artista de la cancion es el mismo que el del album
        if cancion.artista != self.creador:
            print(f"❌ '{cancion.titulo}' no pertenece a {self.artista}.")
            return self
        exito = self._insertar_item(cancion)
        if not exito:
            print(f"'{cancion.titulo}' ya está en '{self.nombre}'.")
        return self


    def eliminar_cancion(self, cancion):
        exito = self._extraer_item(cancion)
        if not exito:
            print(f"'{cancion.titulo}' no está en '{self.nombre}'.")
        return self

    #Definimos los metodos especiales
    def __eq__(self, other):
        #Dos albumes son iguales si tienen el mismo nombre y artista
        if not isinstance(other, Album):
            return NotImplemented
        return self.nombre == other.nombre and self.artista == other.artista

    def __lt__(self, other):
        #Ahora podemos ordenar albumes por año
        if not isinstance(other, Album):
            return NotImplemented
        return self.nombre < other.nombre and self.artista < other.artista

    def __str__(self):
        lineas = [f"💿 Album: {self.nombre} ({self._año}) — {self.artista}"]
        lineas.append(f'Pistas: {len(self)}')
        lineas.append(f'Duracion: {self.duracion_total}s')
        if self.lista_contenido:
            lineas.append('Canciones: ')
            for i, j in enumerate(self, 1):
                lineas.append(f'{i}. {j}')
        return '\n'.join(lineas)

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