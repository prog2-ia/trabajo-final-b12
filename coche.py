class Coche:
    kilometros_recorridos = 0
    gasolina = 0
    def __init__(self, matricula, marca):
        self.matricula = matricula
        self.marca = marca

class Persona:
    def __init__(self, dni, nombre, apellido, coche):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.coche = coche