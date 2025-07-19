"""Formulario para la gestion de Departamentos"""

import flet as ft
from basedatos.funciones_manejo_db.querys import (
    REGISTER_DEP, OBTENER_DEP, ACTUALIZAR_DEP, BUSCAR_DEP
)

class GestionDepartamentos:
    def __init__(self, page, mostrar_mensajes, conector):
        # Se referencia el objeto pagina que contiene los elementos de la aplicacion
        self.page = page
        self.conn = conector

        # Creacion del texto de descripcion del formulario
        self.texto_descripcion = ft.Text("Registro de Departamentos de la Empresa", style="italic",
                                         size=20, color="#FFFFFF")

        # ID de departamento seleccionado
        self.id_dep_seleccionado = None

        # Creacion del campo de texto para el nombre del departamento
        self.nombre = ft.TextField(bgcolor="#FFFFFF", label="Nombre del departamento",
                                   border_color="#FFFFFF", border_width=15,
                                   max_length=100, border_radius=10, width=600,
                                   expand=True)

        # Creacion de los botones de accion
        self.boton_registrar = ft.ElevatedButton(text="Registar", bgcolor="#FFFFFF",
                                               color="#00008B", width=120, height=40,
                                               on_click=self.registrar_dep)

        self.boton_actualizar = ft.ElevatedButton(text="Actualizar", bgcolor="#34495e",
                                                color="#00008B", width=120, height=40,
                                                on_click=self.actualizar_datos_dep)
        self.boton_actualizar.disabled = True

        # Creacion de la tabla de datos para los departamentos registrados
        self.tabla_departamentos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID"), numeric=True),
                ft.DataColumn(ft.Text("Nombre del Departamento"))
            ],
            bgcolor="#FFFFFF",
            width=860,
            border_radius=5,
            expand=True,
        )

        # Referencia de la funcion utilizada para mostrar mensajes al usuario
        self.mostrar_mensajes = mostrar_mensajes

        # Fila para colocar los elementos de accion
        self.fila_acciones = ft.Row(
            controls=[
                self.nombre, self.boton_registrar, self.boton_actualizar
            ],
            alignment="Center"
        )

        # Fila para colocar la tabla de departamentos
        self.fila_tabla_departamentos = ft.Row(
            controls=[
                self.tabla_departamentos
            ],
            alignment="Center"
        )

        # Columna para organizar los elementos de manera vertical
        self.columna_elementos = ft.Column(
            controls=[
                self.texto_descripcion,
                self.fila_acciones,
                self.fila_tabla_departamentos
            ],
            spacing=25
        )

        # vista de lista
        self.vista_lista = ft.ListView(controls=[self.columna_elementos])

        # Container principal de todos los elementos
        self.form = ft.Container(
            bgcolor="#00008B",
            border_radius=10,
            content=self.vista_lista,
            padding=25
        )

        # Fila principal
        self.content = ft.ResponsiveRow(
            controls=[
                self.form,
            ],
            expand=True
        )

    # Metodo para bloquear el boton de registro
    def bloquear_registro(self):
        self.boton_registrar.disabled = True
        self.boton_registrar.bgcolor = "#34495e"

    # Metodo para desbloquear el boton de registro
    def desbloquear_registro(self):
        self.boton_registrar.disabled = False
        self.boton_registrar.bgcolor = "#FFFFFF"

    # Metodo para bloquear el boton de actualizacion
    def bloquear_actualizacion(self):
        self.boton_actualizar.disabled = True
        self.boton_actualizar.bgcolor = "#34495e"

    # Metodo para desbloquear el boton de actualizacion
    def desbloquear_actualizacion(self):
        self.boton_actualizar.disabled = False
        self.boton_actualizar.bgcolor = "#FFFFFF"

    # Metodo para verificar si el textfield de nombre de departamento esta vacio
    def verificar_departamento(self):
        return bool(self.nombre.value)

    # Metodo para establecer el atributo id_dep_seleccionado en None
    def vaciar_id_dep_seleccionado(self):
        self.id_dep_seleccionado = None

    # Metodo para vaciar los campos de texto
    def vaciar_textfield(self):
        self.nombre.value = ""

    # Metodo para vaciar la tabla de departamentos
    def vaciar_tabla_departamentos(self):
        self.tabla_departamentos.rows.clear()

    # Metodo para obtener el nombre del departamento a registrar
    def obt_nombre_dep(self):
        nombre = str(self.nombre.value)
        return nombre
    
    # Metodo para registrar departamento en la base de datos
    def registrar_dep(self, e):
        if not self.verificar_departamento():
            self.mostrar_mensajes(
                "Debe ingresar el nombre de un departamento para poder registrar",
                "#212f3d"
            )
            return
        else:
            nombre = self.obt_nombre_dep()
            deps = self.conn.ejecutar_sql(BUSCAR_DEP, (nombre,))
            if len(deps) > 0:
                self.mostrar_mensajes(
                    "Esta intentando registrar un departamento ya existente en la base de datos",
                    "#C70039"
                )
            else:
                self.conn.ejecutar_sql(REGISTER_DEP, (nombre,))
                self.vaciar_textfield()
                self.mostrar_dep_registrados()
                self.mostrar_mensajes("Departamento registrado exitosamente", "#138d75")

    # Metodo para obtener en la tabla todos los departamentos registrados
    def mostrar_dep_registrados(self):
        self.vaciar_tabla_departamentos()
        departamentos = self.conn.ejecutar_sql_seleccion_total(OBTENER_DEP)

        for departamento in departamentos:
            self.tabla_departamentos.rows.append(
                ft.DataRow(
                    on_select_changed=self.obtner_dato_departamento,
                    cells=[
                        ft.DataCell(ft.Text(departamento[0])),
                        ft.DataCell(ft.Text(departamento[1])),
                    ]
                )
            )

        self.page.update()

    # Metodo para obtener los datos del departamento seleccionado desde la tabla
    def obtner_dato_departamento(self, e):
        self.id_dep_seleccionado = e.control.cells[0].content.value
        self.nombre.value = e.control.cells[1].content.value
        self.bloquear_registro()
        self.desbloquear_actualizacion()
        self.page.update()

    # Metodo para actualizar los datos de un departamento seleccionado en la tabla
    def actualizar_datos_dep(self, e):
        if not self.verificar_departamento():
            self.mostrar_mensajes("Debe ingresar el nuevo nombre del departamento para actualizar",
                                  "#212f3d")
        else:
            nuevo_nombre = self.obt_nombre_dep()
            self.conn.ejecutar_sql(ACTUALIZAR_DEP, (nuevo_nombre, self.id_dep_seleccionado))
            self.bloquear_actualizacion()
            self.desbloquear_registro()
            self.mostrar_dep_registrados()
            self.vaciar_textfield()
            self.mostrar_mensajes("Departamento actualizado exitosamente", "#138d75")
            self.vaciar_id_dep_seleccionado()

    # Metodo para limpiar los elementos del modulo al cerrar sesion
    def limpiar_datos_cerrar_sesion(self):
        self.vaciar_id_dep_seleccionado()
        self.vaciar_textfield()
        self.bloquear_actualizacion()
        self.desbloquear_registro()
        self.vaciar_tabla_departamentos()