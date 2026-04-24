class GestorAuth:
    def __init__(self):
        self.usuarios_registrados = {} # {username: objeto_usuario}

    def registrar(self, usuario):
        if usuario.username not in self.usuarios_registrados:
            self.usuarios_registrados[usuario.username] = usuario
            return True
        return False

    def login(self, username, password):
        # Aquí iría la validación lógica
        pass