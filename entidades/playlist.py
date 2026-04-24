#playlist.py

from entidades.agrupacion import Agrupacion

class Playlist(Agrupacion):
    def __init__(self, creador, nombre, estado="publica"):
        super().__init__(creador, nombre)
        self._estado = estado #Atributo privado

    @property
    def estado(self):
        return self._estado

    @property
    def es_publica(self):
        #Comprobamos la visibilidad
        return self._estado == "publica"

    def añadir_contenido(self, contenido):
        #Llama al metodo del padre
        exito = self._insertar_item(contenido)
        if not exito:
            print(f"'{contenido.titulo}' ya está en '{self.nombre}'.")
        return self # permite: playlist.añadir_contenido(c1).añadir_contenido(c2)

    def eliminar_contenido(self, contenido):
        #Llama al metodo del padre
        exito = self._extraer_item(contenido)
        if not exito:
            print(f"'{contenido.titulo}' no está en '{self.nombre}'.")
        return self

    def cambiar_visibilidad(self):
        #Alterna el estado entre publica y privada.
        self._estado = 'privada' if self.es_publica else 'publica'
        return self

    def __add__(self, other):
        #Fusiona dos playlists: nuevaP = P1 + P2
        if not(isinstance(other, Playlist)):
            return NotImplemented
        nueva = Playlist(self.creador, f'{self.nombre} + {other.nombre}')
        for i in self:
            nueva._insertar_item(i)
        for i in other:
            nueva._insertar_item(i)
        return nueva

    def __str__(self):
        icono = "🌍" if self.es_publica else "🔒" #Agregamos un emoji para hacerlo mas visual
        lineas = [f'{icono} Playlist: {self.nombre} — {self.creador}']
        lineas.append(f'Estado: {self._estado}')
        lineas.append(f'Elementos: {len(self)}')
        lineas.append(f'Duracion: {self.duracion_total}s')
        if self.lista_contenido:
            lineas.append('Contenido: ')
            for i, j in enumerate(self, 1):
                lineas.append(f'{i}. {j}')
        return '\n'.join(lineas)

