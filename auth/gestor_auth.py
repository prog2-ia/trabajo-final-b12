# gestor_auth.py

class Usuario:
    """Usuario mínimo para el sistema de autenticación."""
    def __init__(self, username, password):
        self.username = username
        self._password = password
        self.playlists = []   # playlists propias del usuario

    def verificar_password(self, password):
        return self._password == password

    def __str__(self):
        return f"👤 {self.username} ({len(self.playlists)} playlist(s))"


class GestorAuth:
    def __init__(self):
        self.usuarios_registrados = {}  # {username: objeto_usuario}
        self.usuario_actual = None      # sesión activa

    # ── REGISTRO ─────────────────────────────────────────────────────────────

    def registrar(self, username, password):
        """Registra un nuevo usuario. Devuelve True si tuvo éxito."""
        if username in self.usuarios_registrados:
            print(f"❌ El usuario '{username}' ya existe.")
            return False
        usuario = Usuario(username, password)
        self.usuarios_registrados[username] = usuario
        print(f"✅ Usuario '{username}' registrado correctamente.")
        return True

    # ── LOGIN / LOGOUT ────────────────────────────────────────────────────────

    def login(self, username, password):
        """Inicia sesión. Devuelve el objeto Usuario si tiene éxito."""
        usuario = self.usuarios_registrados.get(username)
        if usuario and usuario.verificar_password(password):
            self.usuario_actual = usuario
            print(f"✅ Bienvenido, {username}!")
            return usuario
        print("❌ Usuario o contraseña incorrectos.")
        return None

    def logout(self):
        if self.usuario_actual:
            print(f"👋 Sesión cerrada para '{self.usuario_actual.username}'.")
        self.usuario_actual = None

    # ── ESTADO ────────────────────────────────────────────────────────────────

    @property
    def hay_sesion(self):
        return self.usuario_actual is not None

    def __str__(self):
        if self.hay_sesion:
            return f"Sesión activa: {self.usuario_actual.username}"
        return "Sin sesión activa"