#agrupacion.py

class Agrupacion:
    def __init__(self, creador, nombre):
        self.creador = creador
        self.nombre = nombre
        self.lista_contenido = []

    def _insertar_item(self, item):
        #Devuelve True si se ha podido introducir y False si ya existía
        if item not in self.lista_contenido:
            self.lista_contenido.append(item)
            return True
        return False

    def _extraer_item(self, item):
       #Para eliminar elementos, True si se ha eliminado y False si no
        if item in self.lista_contenido:
            self.lista_contenido.remove(item)
            return True
        return False


    @property
    def duracion_total(self):
        """Acceso como atributo: album.duracion_total"""
        return sum(item._duracion for item in self.lista_contenido)

    #Implementación de metodos especiales
    def __len__(self):
        return len(self.lista_contenido) #Ahora len(album) devuelve el num de elementos

    def __iter__(self):
        return iter(self.lista_contenido) #for cancion in album, iteramos sobre el contenido

    def __eq__(self, other):
        #Podemos decir que dos agrupaciones son iguales si tienen el mismo nombre y creador
        if not isinstance(other, Agrupacion):
            return NotImplemented
        return self.nombre == other.nombre and self.creador == other.creador

    def __repr__(self):
        #Gracias a esto, se obtiene una representación técnica para depurar
        return f"{self.__class__.__name__}(nombre='{self.nombre}', creador='{self.creador}', elementos={len(self)})"

    def __str__(self):
        #Obtenemos una representación legible
        return f'{self.nombre} - {self.creador} ({len(self)} elementos {self.duracion_total}s)'