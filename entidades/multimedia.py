#multimedia.py

class Multimedia:
    def __init__(self, titulo, autor, duracion, portada, colaboradores=None):
        # Usamos UN guion bajo para indicar que son PROTEGIDOS (todos, a causa de ser una clase base
        self._titulo = titulo
        self._autor = autor
        self._duracion = duracion
        self._portada = portada
        self._duracion = duracion
        self._colaboradores = colaboradores if colaboradores else []
        # nos aseguramos que no se enlacen colaboradores de diferentes multimedia, al contrario q si hicieramos
        # def __self......., colaboradores=[]), ademas da pie a añadir despues de ser creada

    @abstractmethod
    def reproducir(self):
        """
        No se podra crear una clase multimedia directamanete
        Este método es una PROMESA.
        Obliga a cualquier clase que herede de Multimedia a
        escribir su propia forma de reproducir.(crear esta funcion)
        porq hay diferentes tipos de reproduccion; anuncios(insaltables), video(mp4), audio(mp3)
        """
        pass

    def get_info(self):
        # Devolvemos un diccionario con la información
        return {
            "titulo": self._titulo,
            "autor": self._autor,
            "duracion": self._duracion,
        }

    def __str__(self):
        # el print() de esta clase
        return f"{self._titulo} - {self._autor} ({self._duracion} min)"
