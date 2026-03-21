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

    def obtener_duracion_total(self):
        """Suma la duración de todos los elementos en la lista."""
        return sum(item.duracion for item in self.lista_contenido)