#multimedia.py
from abc import ABC, abstractmethod

class Multimedia(ABC):
    def __init__(self, titulo, autor, duracion, portada, colaboradores=None):
        # Usamos UN guion bajo para indicar que son PROTEGIDOS (todos, a causa de ser una clase base)
        self._titulo = titulo
        self._autor = autor
        self._duracion = duracion
        self._portada = portada
        self._colaboradores = colaboradores if colaboradores else []
        # nos aseguramos que no se enlacen colaboradores de diferentes multimedia, al contrario
        # que si hiciéramos def __self......., colaboradores=[]),
        # ademas da pie a añadir después de ser creada

    @abstractmethod
    def reproducir(self):
        """
        No se podra crear una clase multimedia directamanete, este métodó es una PROMESA.
        Obliga a cualquier clase que herede de Multimedia a escribir su propia forma de reproducir.(crear esta funcion)
        porq hay diferentes tipos de reproduccion; anuncios(insaltables), video(mp4), audio(mp3)
        """
        pass

    def get_info(self):
        # Devolvemos un diccionario con la información del comtenido multimedia
        return {
            "titulo": self._titulo,
            "autor": self._autor,
            "duracion": self._duracion,
        }

    def __str__(self):
        #Representación informal — para el usuario final (print, f-strings).
        colabs = f" feat. {', '.join(self._colaboradores)}" if self._colaboradores else ""
        return f"{self._titulo}{colabs} - {self._autor} ({self._duracion} min)"

    def __repr__(self):
        """
        Representación formal — para el desarrollador.
        Devuelve algo que parezca código Python válido para recrear el objeto.
        Se ve en la consola interactiva o al hacer repr(objeto).
        """
        colabs = self._colaboradores if self._colaboradores else []
        return (f"{type(self).__name__}("
                f"titulo={self._titulo!r}, "
                f"autor={self._autor!r}, "
                f"duracion={self._duracion!r}, "
                f"colaboradores={colabs!r})")
        #!r añade las comillas automáticamente alrededor de strings

    def __bool__(self):
        """
        Valor de verdad del objeto.
        Un Multimedia es válido (True) si tiene título y autor no vacíos.
        Permite hacer: if cancion: reproducir() en vez de if cancion._titulo != '':
        """
        return bool(self._titulo and self._autor)

    def __eq__(self, otro):
        """
        Igualdad entre dos objetos Multimedia.
        Dos objetos son 'el mismo' si tienen el mismo título y autor (ignorando mayúsculas).
        Esto hace que _insertar_item() de Agrupacion detecte duplicados correctamente,
        porque 'not in' y 'in' usan __eq__ internamente.
        """
        if not isinstance(otro, Multimedia):
            return NotImplemented  # <- NotImplemented, no False, es la forma correcta
        return (self._titulo.lower() == otro._titulo.lower() and
                self._autor.lower() == otro._autor.lower())
    @property
    def titulo(self):
        return self._titulo

    @property
    def artista(self):
        #Alias de autor, compatibilidad con Album
        return self._autor

    @property
    def autor(self):
        return self._autor