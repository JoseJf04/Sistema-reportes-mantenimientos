"""Formulario de gestion de equipos"""

import flet as ft

from basedatos.funciones_manejo_db.querys import(OBTENER_DEP, OBTENER_EQUIPOS, BUSCAR_EQUIPO,
                                                 REGISTRAR_EQUIPO, BORRAR_EQUIPO, ACTUALIZAR_DATOS_EQUIPO)

from formularios.opciones_desplegables import opciones_tipos_equipos

# Creacion de clase para instanciar el formulario de gestion de equipos
class GestionEquipos:
    def __init__(self, page, mostrar_mensajes, conector):
        
        # Referencia del objeto page que contiene todos los elementos de la aplicacion
        self.page = page

        self.conn = conector

        # Texto de descripcion del formulario de registro de equipos
        self.texto_desc_formulario = ft.Text("Informacion de los Equipos", style="italic", size=20, color="#FFFFFF")


        """Creacion de los inputs del formulario de gestion de equipos"""
        
        # Campo de texto para el identificador del equipo
        self.identificador = ft.TextField(label="Identificador del equipo", bgcolor="#FFFFFF", border_color="#FFFFFF", 
                                          border_width=15, border_radius=10)

        # Campo de texto para la descripcion del equipo
        self.descripcion = ft.TextField(label="Descripcion del equipo", bgcolor="#FFFFFF", border_color="#FFFFFF", 
                                        border_width=15, border_radius=10)

        # Campo de texto para especificar la marca del equipo
        self.marca = ft.TextField(label="Marca", bgcolor="#FFFFFF", border_color="#FFFFFF", 
                                  border_width=15, border_radius=10)

        # Campo de texto para especificar el modelo del equipo
        self.modelo = ft.TextField(label="Modelo", bgcolor="#FFFFFF", border_color="#FFFFFF", 
                                   border_width=15, border_radius=10)

        # Combo de opciones para seleccionar el tipo de equipo
        self.tipo_equipo = ft.Dropdown(value="", label="Seleccionar Tipo de Equipo", bgcolor="#FFFFFF", 
                                       border_color="#FFFFFF", border_width=15, border_radius=10)
        
        self.tipo_equipo.options = opciones_tipos_equipos

        # Combo de opciones para seleccionar el departamento al que pertenece el equipo
        self.departamento = ft.Dropdown(value="", label="Departamento al que pertenece", border_width=15, 
                                        bgcolor="#FFFFFF", border_color="#FFFFFF", border_radius=10)

        """Creacion de los botones de registro, actualizacion y borrado de equipos"""
        
        # Creacion de los botones de gestion
        self.boton_guardar = ft.ElevatedButton(on_click=self.registrar_equipo, text="Registrar", 
                                               color="#00008B", width=90, height=40)
        
        self.boton_modificar = ft.ElevatedButton(on_click=self.actualizar_datos_equipo, text="Actualizar", 
                                                 color="#00008B", width=90, height=40)
        
        self.boton_borrar = ft.ElevatedButton(on_click=self.borrar_equipo, text="Borrar", 
                                              color="#00008B", width=90, height=40)


        """Creacion de los inputs para filtrado de datos y elementos de vizualizacion de datos"""
        
        # Texto de descripcion de la tabla de equipos registrados
        self.texto_desc_tabla = ft.Text("Equipos Registrados", style="italic", size=20, color="#FFFFFF")

        # Combo de opcioenes para seleccionar el departamento por el cual filtrar equipos
        self.filtrado_departamento =  ft.Dropdown(value="", label="Departamento", border_width=15, 
                                        bgcolor="#FFFFFF", border_color="#FFFFFF", border_radius=10,
                                        width=180)

        # Combo de opciones para seleccionar el tipo de equipo a filtrar
        self.filtrado_tipo_equipo = ft.Dropdown(value="", label="Tipo de Equipo", border_width=15, 
                                        bgcolor="#FFFFFF", border_color="#FFFFFF", border_radius=10,
                                        width=180)
        
        self.filtrado_tipo_equipo.options = opciones_tipos_equipos

        self.boton_buscar = ft.IconButton(on_click=self.filtrar_mostrar_equipos, icon="SEARCH", bgcolor="#FFFFFF", icon_color="#00008B")

        # Creacion de la tabla para mostrar los equipos registrados
        self.tabla_equipos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(value="ID")),
                ft.DataColumn(ft.Text(value="DESCRIPCION")),
                ft.DataColumn(ft.Text(value="MARCA")),
                ft.DataColumn(ft.Text(value="MODELO")),
                ft.DataColumn(ft.Text(value="TIPO")),
                ft.DataColumn(ft.Text(value="DEPARTAMENTO")),
            ],
            bgcolor="#FFFFFF",
            width=860,
            border_radius=15,
            expand=True
        )


        """Referencia de la funcion utilizada para mostrar mensajes al usuario"""

        self.mostrar_mensajes = mostrar_mensajes


        """Creacion de los elementos para colocar y ordenar los inputs del formulario de gestion"""
        
         # Fila para los botones de gestion
        self.fila_botones = ft.Row(
            controls=[
                self.boton_guardar,
                self.boton_modificar,
                self.boton_borrar
            ],
            alignment="Center"
        )
        
        # Columna para ordenar los elementos del formulario
        self.columna_elementos_formulario = ft.Column(
            controls=[
                self.texto_desc_formulario,
                self.identificador,
                self.descripcion,
                self.marca,
                self.modelo,
                self.tipo_equipo,
                self.departamento,
                self.fila_botones,
            ],
            spacing=20
        )

        # Container para el formulario de Gestion
        self.formulario = ft.Container(
            content=self.columna_elementos_formulario,
            bgcolor="#00008B",
            border_radius=10,
            col=4,
            padding=15
        )


        """Creacion de los elementos para colocar y ordenar los inputs de filtrado y las vizualizaciones"""
        
        # Fila para los elementos de filtrado
        self.fila_elementos_filtrado = ft.Row(
            controls=[
                self.filtrado_departamento,
                self.filtrado_tipo_equipo,
                self.boton_buscar
            ],
        )

        # Fila para la tabla de gestion de equipos
        self.fila_tabla_equipos = ft.Row(controls=[self.tabla_equipos])

        # Columna para los inputs de filtrado y tabla de vizualizacion de equipos
        self.columna_tabla_equipos = ft.Column(
            controls=[
                self.texto_desc_tabla,
                self.fila_elementos_filtrado,
                self.fila_tabla_equipos
            ],
            spacing=20,
            expand=True,
        )

        # Vista de lista para desplazarse de arriba a abajo en las tabla de equipos
        self.vista_de_lista = ft.ListView(controls=[self.columna_tabla_equipos])

        # Container para la tabla de equipos registrados
        self.tabla_gestion = ft.Container(
            content=self.vista_de_lista,
            bgcolor="#00008B",
            border_radius=10,
            col=8,
            padding=15
        )

        """Fila principal para contener todos los elementos del modulo de gestion de equipos"""
        # Fila principal
        self.content = ft.ResponsiveRow(
            controls=[
                self.formulario, 
                self.tabla_gestion
            ],
            expand=True
        )


    """Metodos para manejar la gestion de equipos"""

    # Metodo para obtener los departamentos registrados en la base de datos
    def obtener_departamentos_db(self):
        # Limpiar el combo de opciones de departamentos del formulario
        self.departamento.options.clear()

        # Limpiar el combo de opciones de departamentos para el filtrado
        self.filtrado_departamento.options.clear()

        # Obtener departamentos registrados
        departamentos = self.conn.ejecutar_sql_seleccion_total(OBTENER_DEP)
        
        # Establecer cada uno de los departamentos registrados en los combo de opciones
        for departamento in departamentos:
            self.departamento.options.append(ft.dropdown.Option(text=departamento[1], key=departamento[0]))
            self.filtrado_departamento.options.append(ft.dropdown.Option(text=departamento[1], key=departamento[0]))

    # Metodo para verificar si el campo de texto del id del equipo esta vacio
    def verificar_id_equipo(self):
        return bool(self.identificador.value)

    # Metodo para verificar si los campos de los campo de texto estan vacios
    def verificar_datos_equipo(self):
        return not (self.descripcion.value == "" or self.marca.value == "" or 
                    self.modelo.value == "" or self.departamento.value == "" or 
                    self.tipo_equipo.value == "")

    # Metodo para verificar si los inputs de filtrado estan vacios
    def verificar_datos_filtrado(self):
        return not(self.filtrado_departamento.value == "" 
                   or self.filtrado_tipo_equipo.value == "")

    # Metodo para obtener el valor ingresado en campo de texto identificador
    def obtener_id_equipo(self):
        return str(self.identificador.value)

    # Metodo para obtener los datos del equipo a regiustrar 
    def obteber_datos_registro(self):
        descripcion = str(self.descripcion.value)
        marca = str(self.marca.value)
        modelo = str(self.modelo.value)
        tipo_equipo = str(self.tipo_equipo.value)
        departamento = int(self.departamento.value)

        return descripcion, marca, modelo, tipo_equipo, departamento

    # Metodo para obtener los valores seleccionados para el filtrado equipos
    def obtener_datos_filtrado_equipos(self):
        departamento = self.filtrado_departamento.value
        tipo_equipo = self.filtrado_tipo_equipo.value

        return departamento, tipo_equipo
    
    # Metodo para limpiar los inputs del formulario
    def vaciar_inputs(self):
        self.identificador.value = ""
        self.descripcion.value = ""
        self.marca.value = ""
        self.modelo.value = ""
        self.tipo_equipo.value = ""
        self.tipo_equipo.hint_text = ""
        self.departamento.value = ""
        self.departamento.hint_text = ""

    # Metodo para limpiar los inputs de filtrado
    def vaciar_inputs_filtrado(self):
        self.filtrado_departamento.value = ""
        self.filtrado_departamento.hint_text = ""
        self.filtrado_tipo_equipo.value = ""
        self.filtrado_tipo_equipo.hint_text = ""
    
    # Metodo para vaciar la tabla de equipos registrados
    def vaciar_tabla_equipos(self):
        self.tabla_equipos.rows.clear()

    # Metodo para obtener los equipos registrados
    def obtener_equipos_registrados(self):
        # Obtener los ultimos 20 equipos registrados
        sql_obtener_equipos = OBTENER_EQUIPOS + " ORDER BY id_equipo DESC LIMIT 20"
        equipos_registrados = self.conn.ejecutar_sql_seleccion_total(sql_obtener_equipos)
        return equipos_registrados

    # Metodo para los equipos filtrados
    def filtrar_equipos_registrados(self):
        datos_filtrado = self.obtener_datos_filtrado_equipos()
        sql_filtrar_equipos = OBTENER_EQUIPOS + " WHERE d.id = ? AND e.tipo_equipo = ?"
        equipos_filtrados = self.conn.ejecutar_sql(sql_filtrar_equipos, (*datos_filtrado,))

        return equipos_filtrados

    # Metodo para mostrar todos los equipos registrados
    def mostrar_equipos_registrados(self, equipos_registrados):
        self.vaciar_tabla_equipos()

        for equipo in equipos_registrados:
            self.tabla_equipos.rows.append(
                ft.DataRow(
                    on_select_changed=self.obtener_datos_actualizacion,
                    cells=[
                        ft.DataCell(ft.Text(equipo[0])),
                        ft.DataCell(ft.Text(equipo[1])),
                        ft.DataCell(ft.Text(equipo[2])),
                        ft.DataCell(ft.Text(equipo[3])),
                        ft.DataCell(ft.Text(equipo[4])),
                        ft.DataCell(ft.Text(equipo[6])),
                    ]
                )
            )
        
        self.page.update()
    
    # Metodo para filtrar y mostrar los equipos mediante filtrado
    def filtrar_mostrar_equipos(self, e):
        if not self.verificar_datos_filtrado():
            self.mostrar_mensajes("Debe especificar cada uno de los parametros solicitados para filtrar", 
                                  "#212f3d")
        else:
            equipos_filtrados = self.filtrar_equipos_registrados()
            self.mostrar_equipos_registrados(equipos_filtrados)

    # Metodo para obtener los datos del equipo a registrar
    def obtener_datos_actualizacion(self, e):
        id_equipo = e.control.cells[0].content.value

        sql_obtener_equipo = OBTENER_EQUIPOS + " WHERE e.id_equipo = ?"

        equipo = self.conn.ejecutar_sql(sql_obtener_equipo, (id_equipo,))
        _, descripcion, marca, modelo, tipo, id_dep, departamento = equipo[0] 

        self.identificador.value = id_equipo
        self.descripcion.value = descripcion
        self.marca.value = marca
        self.modelo.value = modelo
        self.tipo_equipo.value = tipo
        self.tipo_equipo.hint_text = tipo
        self.departamento.value = id_dep
        self.departamento.hint_text = departamento

        self.page.update()

    # Metodo para registrar un nuevo equipo en la base de datos
    def registrar_equipo(self, e):
        if not self.verificar_id_equipo() or not self.verificar_datos_equipo():
            self.mostrar_mensajes("Debe ingresar todos los datos solicitado para registrar",
                                  "#212f3d")
        else:
            id_equipo = self.obtener_id_equipo()

            # Verificar la existencia del equipo en la base de datos
            equipo = self.conn.ejecutar_sql(BUSCAR_EQUIPO, (id_equipo,))

            if len(equipo) > 0:
                self.mostrar_mensajes("Cancelado: Esta intentando registrar un equipo que ya se encuentra registrado",
                                      "#C70039")
            else:
                datos_equipo = self.obteber_datos_registro()
                self.conn.ejecutar_sql(REGISTRAR_EQUIPO, (id_equipo, *datos_equipo))
                self.vaciar_inputs()
                self.mostrar_equipos_registrados(self.obtener_equipos_registrados())
                self.mostrar_mensajes("El Equipo ha sido registrado exitosamente", "#138d75")

    # Metodo para actualizar los datos de un equipo
    def actualizar_datos_equipo(self, e):
        if not self.verificar_id_equipo() or not self.verificar_datos_equipo():
            self.mostrar_mensajes("Debe ingresar cada uno de los datos solicitados para registrar",
                                  "#212f3d")
        else:
            id_equipo = self.obtener_id_equipo()
            equipo = self.conn.ejecutar_sql(BUSCAR_EQUIPO, (id_equipo,))

            if len(equipo) > 0:
                datos_equipo = self.obteber_datos_registro()
                self.conn.ejecutar_sql(ACTUALIZAR_DATOS_EQUIPO, (*datos_equipo, id_equipo))
                self.vaciar_inputs()
                self.mostrar_equipos_registrados(self.obtener_equipos_registrados())
                self.mostrar_mensajes("Datos del equipo actualizados exitosamente","#138d75")
            else:
                self.mostrar_mensajes("No se encontro equipo registrado con el id ingresado",
                                      "#C70039")

    # Metodo para borrar un equipo de la base de datos
    def borrar_equipo(self, e):
        if not self.verificar_id_equipo():
            self.mostrar_mensajes("Debe ingresar el identificador del equipo para poder borrarlo",
                                  "#212f3d")
        else:
            id_equipo = self.obtener_id_equipo()

            # Verificar la existencia del equipo en la base de datos
            equipo = self.conn.ejecutar_sql(BUSCAR_EQUIPO, (id_equipo,))

            if len(equipo) > 0:
                self.conn.ejecutar_sql(BORRAR_EQUIPO, (id_equipo,))
                self.vaciar_inputs()
                self.mostrar_equipos_registrados(self.obtener_equipos_registrados())
                self.mostrar_mensajes("Equipo borrado Exitosamente", "#138d75")
            else:
                self.mostrar_mensajes("No se encontro equipo registrado con el id ingresado",
                                      "#C70039")

    # Metodo para limpiar los elementos del modulo al salir
    def limpiar_datos_cerrar_sesion(self):
        self.vaciar_inputs()
        self.vaciar_inputs_filtrado()
        self.vaciar_tabla_equipos()