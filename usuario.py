"""Modulo con la clase usuario del sistema"""

class Usuario:
    def __init__(self):
        # Credenciales de usuario
        self.ci = None
        self.nombre_usuario = None
        self.tipo_usuario = None
    
    # Metodo para establecer las credenciales del usuario
    def establecer_credenciales(self, ci, nombre_usuario, tipo_usuario):
        self.ci = ci
        self.nombre_usuario = nombre_usuario
        self.tipo_usuario = tipo_usuario
    
    # Metodo para obtener la cedula del usuario
    def obtener_ci_usuario(self):
        return self.ci

    # Metodo para obtener el nombre de usuario
    def obtener_nombre_usuario(self):
        return self.nombre_usuario
    
    # Metodo para obtener el tipo de usuario
    def obtener_tipo_usuario(self):
        return self.tipo_usuario
    
    # Metodo para vaciar los atributos del objeto usuario
    def limpiar_credenciales(self):
        self.ci = None
        self.nombre_usuario = None
        self.tipo_usuario = None