"""Formulario para la gestion de Usuarios"""

import flet as ft
from basedatos.funciones_manejo_db.querys import (REGISTRAR_USAURIO, SELECCIONAR_USUARIO,
                                                  ACTUALIZAR_DATOS_USUARIO, BORRAR_USUARIO)


class GestionUsuarios:
    def __init__(self, page, mostrar_mensaje, conector):
        # Referencia del objeto page que contiene los elementos de la interfaz grafica
        self.page = page
        
        # Referencia del objeto conector a base de datos
        self.conn = conector

        # Atributo para almacenar temporalmente la cedula de un usuario a actualizar
        self.ci_usuario_seleccionado = None

        # Texto de descripcion para el usuario
        self.texto_descripcion = ft.Text("Gestion de Usuarios del Sistema", style="italic", size=20, color="#FFFFFF")

        # Creacion del campo de texto para cedula
        self.ci = ft.TextField(label="Cedula", width=250, bgcolor="#FFFFFF", border_color="#FFFFFF", 
                               border_width=15, border_radius=10, input_filter=ft.NumbersOnlyInputFilter())

        # Creacion del campo de texto para nombres
        self.nombres = ft.TextField(label="Nombres", width=400, bgcolor="#FFFFFF", expand=True, 
                                    border_color="#FFFFFF", border_width=15, border_radius=10)

        # Creacion del campo de texto para nombre de usuario
        self.nombre_usuario = ft.TextField(label="Nombre de usuario", width=600, bgcolor="#FFFFFF", 
                                           expand=True, border_color="#FFFFFF", border_width=15, 
                                           border_radius=10)

        # Creacion del campo de texto para clave de acceso
        self.clave = ft.TextField(label="Clave de acceso", width=400, bgcolor="#FFFFFF", expand=True, 
                                  border_color="#FFFFFF", border_width=15, border_radius=10)

        # Creacion del combo de seleccion para los tipos de usuario
        self.tipo_usuario = ft.Dropdown(value="", label="Tipo de Usuario", width=250, bgcolor="#FFFFFF",
                                         border_color="#FFFFFF", border_width=15, border_radius=10)
        self.tipo_usuario.options = [
            ft.dropdown.Option("Administrador"),
            ft.dropdown.Option("Estandar")
        ]

        # Creacion del boton de registro
        self.boton_regisrar = ft.ElevatedButton(text="Registar Usuario", width=135, height=40, 
                                              color="#00008B", on_click=self.registrar_usuario)

        # Creacion del boton de consulta
        self.boton_buscar = ft.ElevatedButton(text="Buscar Usuario", width=135, height=40, 
                                            color="#00008B", on_click=self.consultar_datos_usuario)

        # Creacion del boton de actualizacion de datos
        self.boton_actualizar = ft.ElevatedButton("Actualizar Usaurio", width=145, height=40, bgcolor= "#34495e", 
                                                color="#00008B", on_click=self.actualizar_datos_usuario)
        self.boton_actualizar.disabled = True

        # Creacion del boton de borrar datos
        self.boton_borrar = ft.ElevatedButton("Borrar Usuario", width=135, height=40, bgcolor="#34495e", 
                                            color="#00008B", on_click=self.borrar_usuario)
        self.boton_borrar.disabled = True

        # Referencia de la funcion utilizada para mostrar mensajes al usuario
        self.mostrar_mensaje = mostrar_mensaje

        # Creacion de la fila para elementos numero 1
        self.fila_datos_usuario_uno = ft.Row(controls=[self.ci, self.nombres])

        # Creacion de fila para elementos numero 2
        self.fila_datos_usuario_dos = ft.Row(controls=[self.nombre_usuario])

        # Creacion de fila para elementos numero 3
        self.fila_datos_usuario_tres = ft.Row(controls=[self.clave, self.tipo_usuario])

        # Creacion de fila de botones
        self.fila_botones = ft.Row(controls=[self.boton_regisrar, self.boton_buscar, self.boton_actualizar, self.boton_borrar])
        self.fila_botones.spacing = 15

        # Creacion de columna para la organizacion de los elementos en el formulario
        self.columna_elementos = ft.Column(
            controls=[
                self.texto_descripcion,
                self.fila_datos_usuario_uno,
                self.fila_datos_usuario_dos,
                self.fila_datos_usuario_tres,
                self.fila_botones
            ],
            spacing=20
        )

        # Creacion de container para la columna de elementos
        self.form = ft.Container(
            content=self.columna_elementos,
            bgcolor="#00008B",
            border_radius=10,
            padding=50
        )

        # Fila principal
        self.content = ft.ResponsiveRow(controls=[self.form], expand=True)
    
    # Metodo para bloquear el boton de registro
    def bloquear_registro(self):
        self.boton_regisrar.disabled = True
        self.boton_regisrar.bgcolor = "#34495e"

    # Metodo para desbloquear el boton de registro
    def desbloquear_registro(self):
        self.boton_regisrar.disabled = False
        self.boton_regisrar.bgcolor = "#FFFFFF"

    # Metodo para bloquear los botones de registro y actualizacion
    def bloquear_actualizacion_borrar(self):
        self.boton_actualizar.disabled = True
        self.boton_actualizar.bgcolor = "#34495e"

        self.boton_borrar.disabled = True
        self.boton_borrar.bgcolor = "#34495e"
    
    # Metodo para desbloquear los botones de registro y actualizacion
    def desbloquear_actualizacion_borrar(self):
        self.boton_actualizar.disabled = False
        self.boton_actualizar.bgcolor = "#FFFFFF"

        self.boton_borrar.disabled = False
        self.boton_borrar.bgcolor = "#FFFFFF"

    # Metodo para vaciar los inputs del formulario
    def vaciar_inputs(self):
        self.ci.value = ""
        self.nombres.value = ""
        self.nombre_usuario.value = ""
        self.clave.value = ""
        self.tipo_usuario.value = ""
        self.tipo_usuario.hint_text = ""

    # Metodo para verificar si el campo cedula esta vacio
    def verificar_ci(self):
        return bool(self.ci.value)

    # Metodo para verificar si alguno de los campos de datos estan vacios
    def verificar_datos(self):
        return not (self.nombres.value == "" or self.nombre_usuario.value == "" 
                    or self.clave.value == "" or self.tipo_usuario.value == "")

    # Metodo para obtener el valor ingresado en el campo cedula
    def obtener_ci(self):
        ci = int(self.ci.value)
        return ci

    # Metodo para obtener cada uno de los datos del usuario
    def obtener_datos_usuario(self):
        nombres = str(self.nombres.value)
        nombre_usurio = str(self.nombre_usuario.value)
        clave = str(self.clave.value)
        tipo_usuario = str(self.tipo_usuario.value)

        return nombres, nombre_usurio, clave, tipo_usuario

    # Metodo para registrar usuario
    def registrar_usuario(self, e):
        if not self.verificar_ci() or not self.verificar_datos():
            self.mostrar_mensaje("Debe ingresar todos los datos solicitados para registrar", "#212f3d")
        else:
            ci = self.obtener_ci()

            # Consultar existencia de usuario
            verificacion_usuario = self.conn.ejecutar_sql(SELECCIONAR_USUARIO, (ci,))

            if len(verificacion_usuario) > 0:
                self.mostrar_mensaje("Registro cancelado: esta intentando registrar un usuario ya existente", "#C70039")
            else:
                datos_usuario = self.obtener_datos_usuario()
                self.conn.ejecutar_sql(REGISTRAR_USAURIO, (ci, *datos_usuario))
                self.vaciar_inputs()
                self.page.update()
                self.mostrar_mensaje("Usuario registrado de forma exitosa", "#138d75")

    # Metodo para traer y mostrar los datos de un usuario
    def consultar_datos_usuario(self, e):
        if not self.verificar_ci():
            self.mostrar_mensaje("Debe ingresar la cedula del usuario para consultar sus datos", "#212f3d")
        else:
            ci = self.obtener_ci()
            usuario = self.conn.ejecutar_sql(SELECCIONAR_USUARIO, (ci,))

            if len(usuario) > 0:
                ci, nombres, nombre_u, clave, tipo_u = usuario[0]

                self.ci_usuario_seleccionado = ci
                self.nombres.value = nombres
                self.nombre_usuario.value = nombre_u
                self.clave.value = clave
                self.tipo_usuario.value = tipo_u
                self.tipo_usuario.hint_text = tipo_u

                self.bloquear_registro()
                self.desbloquear_actualizacion_borrar()

                self.page.update()
            else:
                self.vaciar_inputs()
                self.mostrar_mensaje("No existe usuario registrado con el numero de cedula ingresado", "#C70039")
                self.page.update()

    # Metodo para actualizar la informacion de un usuario
    def actualizar_datos_usuario(self, e):
        if not self.verificar_ci() or not self.verificar_datos():
            self.mostrar_mensaje("Debe ingresar cada uno de los datos solicitados para actualizar", "#212f3d")
        else:
            ci_usuario_actualizar = self.ci_usuario_seleccionado
            nueva_ci = self.obtener_ci()

            datos_usuario = self.obtener_datos_usuario()
            self.conn.ejecutar_sql(ACTUALIZAR_DATOS_USUARIO, (nueva_ci, *datos_usuario, ci_usuario_actualizar))
            self.vaciar_inputs()
            self.ci_usuario_seleccionado = None

            self.bloquear_actualizacion_borrar()
            self.desbloquear_registro()

            self.mostrar_mensaje("Datos actualizados de forma exitosa", "#138d75")

    # Metodo para borrar usuario de la base de datos
    def borrar_usuario(self, e):
        if not self.verificar_ci():
            self.mostrar_mensaje("Debe ingresar la cedula del usuario a eliminar", "#212f3d")
        else:
            ci = self.obtener_ci()
            verificacion_usuario = self.conn.ejecutar_sql(SELECCIONAR_USUARIO, (ci,))

            if len(verificacion_usuario) > 0:
                self.conn.ejecutar_sql(BORRAR_USUARIO, (ci,))
                self.vaciar_inputs()
                self.ci_usuario_seleccionado = None
                
                self.bloquear_actualizacion_borrar()
                self.desbloquear_registro()

                self.mostrar_mensaje("Usuario eliminado de forma exitosa", "#138d75")
            else:
                self.mostrar_mensaje("No se encontro usuario con el numero de cedula ingresado", "#C70039")

    # Metodo para limpiar los elementos del modulo al cerrar sesion
    def limpiar_datos_cerrar_sesion(self):
        self.vaciar_inputs()