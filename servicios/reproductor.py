class Reproductor:
    def __init__(self):
        self.cola_reproduccion = []
        self.pista_actual = None

    def cargar_pista(self, contenido):
        self.pista_actual = contenido
        print(self.pista_actual.reproducir())

    def agregar_a_cola(self, contenido):
        self.cola_reproduccion.append(contenido)
        print(f"Añadido a la cola: {contenido.titulo}")

    def siguiente(self):
        if self.cola_reproduccion:
            self.pista_actual = self.cola_reproduccion.pop(0)
            return self.pista_actual.reproducir()
        return "Fin de la cola."