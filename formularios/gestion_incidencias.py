"""Formulario de gestion de incidencias en equipos"""

import flet as ft

from basedatos.funciones_manejo_db.querys import (REGISTRAR_INCIDENCIA, OBTENER_INCIDENCIAS, 
                                                  BUSCAR_EQUIPO, ACTUALIZAR_DATOS_INCIDENCIA,
                                                  BORRAR_INCIDENCIA, OBTENER_DEP)

from formularios.opciones_desplegables import opciones_estado_equipo, opciones_tipos_equipos

from PDF.generador_reportes_pdf import PDF

from utilidades.validar_fechas import validar_fecha
from utilidades.convertir_fechas import transformar_fecha_DD_MM_AAAA
from utilidades.convertir_fechas import transformar_fecha_AAAA_MM_DD

class GestionIncidencias:
    def __init__(self, page, usuario, mostrar_mensajes, conector):
        
        # Referencia al objeto page que contiene todas los elementos de la interfaz 
        self.page = page
        
        # Referenciua del objeto usuario del sistema
        self.usuario = usuario

        # Referencia del objeto conector de base de datos
        self.conn = conector

        # ID de la incidencia seleccionado para actualizacion
        self.id_incidencia_seleccionada = None


        """Creacion de los inputs del formulario de gestion de incidencias"""

        # Texto de descripcion del formulario de gestion de incidencias
        self.text_desc_formulario = ft.Text(value="Reporte de Incidencias", style="italic", size=20, color="#FFFFFF")

        # campo de texto para el identificador del equipo afectado
        self.id_equipo = ft.TextField(label="Identificador del equipo afectado", bgcolor="#FFFFFF", border_color="#FFFFFF", 
                                      border_width=15, border_radius=10)
        
        # Campo de texto para la fecha de reporte (admite solo caracteres necesarios para el formato DD-MM-AAAA)
        self.fecha_reporte = ft.TextField(label="Fecha de reporte DD-MM-AAAA", bgcolor="#FFFFFF", border_color="#FFFFFF",
                                          border_width=15, border_radius=10,)
        
        self.fecha_reporte.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")
        
        # Combo de opciones para seleccionar el estado actual del equipo afectado
        self.estado_equipo = ft.Dropdown(value="", label="Estado actual del Equipo", bgcolor="#FFFFFF", 
                                         border_color="#FFFFFF", border_width=15, border_radius=10)

        self.estado_equipo.options = opciones_estado_equipo

        # Campo de texto para detallar la incidencia 
        self.descripcion_incidencia = ft.TextField(label="Descripcion de Incidencia", bgcolor="#FFFFFF", border_color="#FFFFFF",
                                                   border_width=15, border_radius=10, multiline=True)
        
        
        """Creacion de los botones para el registro, actualizacion y eliminacion de incidencias"""

        # Creacion de los botones de accion para la gestion de incidencias
        self.boton_guardar = ft.ElevatedButton(on_click=self.registrar_incidencia, text="Registrar", 
                                               color="#00008B", width=90, height=40)

        self.boton_actualizar = ft.ElevatedButton(on_click=self.actualizar_datos_incidencia, text="Actualizar", 
                                                  bgcolor="#34495e", color="#00008B", width=90, height=40)
        self.boton_actualizar.disabled = True

        self.boton_borrar = ft.ElevatedButton(on_click=self.borrar_incidencia, text="Borrar", bgcolor="#34495e",
                                              color="#00008B", width=90, height=40,)
        self.boton_borrar.disabled = True


        """Creacion de los inputs para el filtrado y vizualizacion de incidencias registradas"""

        # Texto de descripcion de la tabla de incidencias registradas
        self.texto_desc_tabla = ft.Text(value="Tabla de gestion de incidencias registradas", style="italic", size=20, color="#FFFFFF")

        # combo de opciones para seleccionar el departamento por el cual filtrar las incidencias
        self.filtrado_departamento = ft.Dropdown(value="", label="Departamento", width=180, border_width=15, 
                                                 bgcolor="#FFFFFF", border_color="#FFFFFF", border_radius=10)
        
        # Combo de opciones para seleccionar el tipo de equipo por el cual filtrar las incidencias
        self.filtrado_tipo_equipo = ft.Dropdown(value="", label="Tipo Equipo", width=155, border_width=15, 
                                                       bgcolor="#FFFFFF", border_color="#FFFFFF", border_radius=10)
        
        self.filtrado_tipo_equipo.options = opciones_tipos_equipos 

        # Campo de texto para la fecha inicio de filtrado
        self.filtrado_fecha_desde = ft.TextField(label="Desde:", width=130, bgcolor="#FFFFFF", border_color="#FFFFFF",
                                            border_width=15, border_radius=10, multiline=True)
        
        self.filtrado_fecha_desde.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")

         # Campo de texto para la fecha limite de filtrado
        self.filtrado_fecha_hasta = ft.TextField(label="Hasta:", width=130, bgcolor="#FFFFFF", border_color="#FFFFFF",
                                            border_width=15, border_radius=10, multiline=True)
        
        self.filtrado_fecha_hasta.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")

        # Boton para filtrar incidencias
        self.boton_buscar_incidencia = ft.IconButton(on_click=self.filtrar_mostar_incidencias, icon="Search", bgcolor="#FFFFFF")

        # Boton para generar reporte de incidencias en pdf
        self.boton_generar_pdf = ft.IconButton(on_click=self.guardar_reporte_incidencias, icon="PICTURE_AS_PDF_OUTLINED", bgcolor="#FFFFFF")

        # Tabla para mostrar las incidencias registradas
        self.tabla_incidencias = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(value="ID")),
                ft.DataColumn(ft.Text(value="INCIDENCIA")),
                ft.DataColumn(ft.Text(value="EQUIPO")),
                ft.DataColumn(ft.Text(value="TIPO EQUIPO")),
                ft.DataColumn(ft.Text(value="MARCA")),
                ft.DataColumn(ft.Text(value="MODELO")),
                ft.DataColumn(ft.Text(value="DEPARTAMENTO")),
                ft.DataColumn(ft.Text(value="FECHA")),
                ft.DataColumn(ft.Text(value="ESTADO"))
            ],
            bgcolor="#FFFFFF",
            border_radius=15,
            expand=True,
            column_spacing=20,
            data_row_min_height=50,
            data_row_max_height=80,
        )


        """Referencia de la funcion utilizada para mostrar mensajes"""
        
        # Funcion para mostrar mensjaes
        self.mostrar_mensajes = mostrar_mensajes


        """Creacion de los elementos para colocar y centrar los inputs del formulario"""
        
        # Fila para colocar los botones de gestion
        self.fila_botones = ft.Row(
            controls=[
                self.boton_guardar,
                self.boton_actualizar,
                self.boton_borrar
            ],
            alignment="Center"
        )

        # Columna para colocar y ordenar verticalmente los elementos del formulario de gestion
        self.columna_elementos_formulario = ft.Column(
            controls=[
                self.text_desc_formulario,
                self.id_equipo,
                self.fecha_reporte,
                self.estado_equipo,
                self.descripcion_incidencia,
                self.fila_botones
            ],
            spacing=20
        )

        # Creacion de la vista de lista para el formulario
        self.vista_de_lista_formulario = ft.ListView(controls=[self.columna_elementos_formulario])

        # Creacion del container para el formulario de gestion
        self.formulario_gestion = ft.Container(
            content=self.vista_de_lista_formulario,
            bgcolor="#00008B",
            border_radius=10,
            col=4,
            padding=15
        )


        """Creacion de los elementos para colocar y ordedar los inputs de filtrado y visualizacion de datos"""

        # Fila para colocar los inputs de filtrado de incidencias
        self.fila_elementos_filtrado = ft.Row(
            controls=[
                self.filtrado_departamento,
                self.filtrado_tipo_equipo,
                self.filtrado_fecha_desde,
                self.filtrado_fecha_hasta,
                self.boton_buscar_incidencia,
                self.boton_generar_pdf
            ]
        )

        # Columna para colocar la tabla de incidencias registradas
        self.columna_tabla_incidencias = ft.Column(
            controls=[
                self.texto_desc_tabla,
                self.fila_elementos_filtrado,
                self.tabla_incidencias,
            ],
            spacing=20,
            expand=True
        )

        # Creacion de la vista de lista para la tabla de incidencias
        self.vista_de_lista_tabla = ft.ListView(controls=[self.columna_tabla_incidencias])

        # Creacion del container para la tabla de incidencias registradas
        self.tabla_gestion = ft.Container(
            content=self.vista_de_lista_tabla,
            bgcolor="#00008B",
            border_radius=10,
            col=8,
            padding=15
        )


        """Fila principal para todos los elementos del modulo de gestion de incidencias"""

        # Fila principal
        self.content = ft.ResponsiveRow(
            controls=[
                self.formulario_gestion, 
                self.tabla_gestion
            ],
            expand=True
        )

    """Metodo para generar reportes pdf de incidencias"""
    
    def guardar_reporte_incidencias(self, e):
        nombre_reporte = ""
        if not(self.verificar_inputs_filtrado()):
            nombre_reporte = "reporte incidencias"
        
        else:
            nombre_reporte = f"reporte de incidencias {self.filtrado_fecha_desde.value} hasta {self.filtrado_fecha_hasta.value}"

        pdf = PDF()
        pdf.add_page()

        datos = []
        for fila in self.tabla_incidencias.rows:
            datos.append([celda.content for celda in fila.cells])
    
        ancho_de_columnas = [10, 70, 30, 35, 35, 35, 60, 20, 20]
        encabezamiento = ("ID", "INCIDENCIA", "EQUIPO", "TIPO EQUIPO", "MARCA", 
                          "MODELO", "DEPARTAMENTO", "FECHA", "ESTADO")
        
        # Crear la tabla en el PDF de las incidencias
        pdf.crear_tabla(encabezamiento, datos, ancho_de_columnas)
        
        # Guardar el PDF de incidencias
        pdf.output(f"{nombre_reporte}.pdf")
        

    """Metodos para manejar la gestion de incidencias"""

    # Metodo para obtener los departamentos registrados en la base de datos
    def obtener_departamentos_db(self):
        self.filtrado_departamento.options.clear()
        departamentos = self.conn.ejecutar_sql_seleccion_total(OBTENER_DEP)
        
        for departamento in departamentos:
            self.filtrado_departamento.options.append(ft.dropdown.Option(text=departamento[1], key=departamento[0]))

    # Metodo para verificar si los inputs del formulario estan vacios 
    def verificar_datos(self):
        return not (self.id_equipo.value == "" or self.fecha_reporte.value =="" or
                    self.estado_equipo.value == "" or self.descripcion_incidencia.value == "")
    
    # Metodo para verificar si los inputs de filtrado estan vacios
    def verificar_inputs_filtrado(self):
        return not (self.filtrado_departamento.value == "" or self.filtrado_tipo_equipo.value == ""
                    or self.filtrado_fecha_desde.value == "" or self.filtrado_fecha_hasta.value == "")

    # Obtener el id_incidencia seleccionada
    def obtner_id_incidencia(self):
        return int(self.id_incidencia_seleccionada)

    # Metodo para obtener la fecha de reporte de la incidencia
    def obtener_fecha_reporte(self):
        fecha_reporte = str(self.fecha_reporte.value)
        return fecha_reporte

    # Metodo para obtener los datos ingredados en cada input del formulario
    def obtener_datos_registro(self):
        id_equipo = str(self.id_equipo.value)
        ci_usuario = int(self.usuario.obtener_ci_usuario())
        fecha_reporte = transformar_fecha_DD_MM_AAAA(self.obtener_fecha_reporte())
        estado_equipo = str(self.estado_equipo.value)
        descripcion_incidendia = str(self.descripcion_incidencia.value)

        return id_equipo, ci_usuario, fecha_reporte, estado_equipo, descripcion_incidendia

    # Metodo para obtener la fecha inicio de filtrado de incidencias 
    def obtener_fecha_desde(self):
        fecha_desde = str(self.filtrado_fecha_desde.value)
        return fecha_desde

    # Metodo para obtener la fecha limite de filtrado de incidencia
    def obtener_fecha_hasta(self):
        fecha_hasta = str(self.filtrado_fecha_hasta.value)
        return fecha_hasta

    # Metodo Obtener los datos ingresados en los inputs de filtrado de incidencias
    def obtener_datos_para_filtrado(self):
        departamento = self.filtrado_departamento.value
        tipo_equipo_i = self.filtrado_tipo_equipo.value
        fecha_desde = transformar_fecha_DD_MM_AAAA(self.obtener_fecha_desde())
        fecha_hasta = transformar_fecha_DD_MM_AAAA(self.obtener_fecha_hasta())

        return departamento, tipo_equipo_i, fecha_desde, fecha_hasta

    # Metodo para establecer el atributo id_incidencia_seleccionada en None
    def vaciar_id_incidencia_seleccionada(self):
        self.id_incidencia_seleccionada = None

    # Metodo para vaciar los inputs del formulario
    def vaciar_datos(self):
        self.id_equipo.value = ""
        self.fecha_reporte.value = ""
        self.estado_equipo.value = ""
        self.estado_equipo.hint_text = ""
        self.descripcion_incidencia.value = ""

    # Metodo para vaciar los inputs de filtrado de incidencias
    def vaciar_inputs_filtrado(self):
        self.filtrado_departamento.value = ""
        self.filtrado_departamento.hint_text = ""
        self.filtrado_tipo_equipo.value = ""
        self.filtrado_tipo_equipo.hint_text = ""
        self.filtrado_fecha_desde.value = ""
        self.filtrado_fecha_hasta.value = ""

    # Metodo para vaciar la tabla de incidencias registradas
    def vaciar_tabla_incidencias(self):
        self.tabla_incidencias.rows.clear()

    # Metodo para bloquear el boton de registro de incidencias
    def bloquear_registro(self):
        self.boton_guardar.disabled = True
        self.boton_guardar.bgcolor = "#34495e"

    # Metodo para desbloquear el boton de registro de incidencias
    def desbloquear_registro(self):
        self.boton_guardar.disabled = False
        self.boton_guardar.bgcolor = "#FFFFFF"

    # Metodo para bloquear los botones de actualizacion y eliminacion de incidencias
    def bloquear_actualizacion_borrar(self):
        self.boton_actualizar.disabled = True
        self.boton_borrar.disabled = True

        self.boton_actualizar.bgcolor = "#34495e"
        self.boton_borrar.bgcolor = "#34495e"

    # Metodo para desbloquear los botones de actualizacion y eliminacion de incidencias
    def desbloquear_actualizacion_borrar(self):
        self.boton_actualizar.disabled = False
        self.boton_borrar.disabled = False

        self.boton_actualizar.bgcolor = "#FFFFFF"
        self.boton_borrar.bgcolor = "#FFFFFF"

    # Metodo para obtener todas las incidencias registradas
    def obtener_incidencias(self):
        # Obtener las ultimas 20 incidencias registradas
        sql_obtener_incidencias = OBTENER_INCIDENCIAS + " ORDER BY id_incidencia DESC LIMIT 20"
        incidencias = self.conn.ejecutar_sql_seleccion_total(sql_obtener_incidencias)
        return incidencias
    
    # Metodo obtener las incidencia mediante filtrado
    def obtener_incidencias_filtradas(self):
        # Obtener los valores ingresados en los inputs de filtrado de incidencias
        datos_filtrado = self.obtener_datos_para_filtrado()
        
        # Modificar la consulta de seleccion de incidencias para realizar el filtrado
        sql_filtrado_incidencias = OBTENER_INCIDENCIAS + """ WHERE d.id = ? AND e.tipo_equipo = ? 
        AND inc.fecha_reporte BETWEEN ? AND ?"""
        
        # Incidencias obtenidas mediante el filtrado
        incidencias_filtradas = self.conn.ejecutar_sql(sql_filtrado_incidencias, (*datos_filtrado,))

        return incidencias_filtradas

    # Metodo para mostrar en la tabla de incidencias, todas las incidencias registradas
    def mostrar_incidencias_registradas(self, incidencias):
        # Limpiar la tabla de incidencias registradas
        self.vaciar_tabla_incidencias()

        for incidencia in incidencias:
            self.tabla_incidencias.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(value=incidencia[0])),
                        ft.DataCell(ft.Text(value=incidencia[1])),
                        ft.DataCell(ft.Text(value=incidencia[2])),
                        ft.DataCell(ft.Text(value=incidencia[3])),
                        ft.DataCell(ft.Text(value=incidencia[4])),
                        ft.DataCell(ft.Text(value=incidencia[5])),
                        ft.DataCell(ft.Text(value=incidencia[7])),
                        ft.DataCell(ft.Text(
                            value=transformar_fecha_AAAA_MM_DD(str(incidencia[10]))
                        )),
                        ft.DataCell(ft.Text(value=incidencia[11])),
                    ],on_select_changed=self.obtener_datos_inidencia_seleccionada
                )
            )

        self.page.update()
    
    # Metodo para filtrar y mostrar las incidencias registradas
    def filtrar_mostar_incidencias(self, e):
        if not self.verificar_inputs_filtrado():
            self.mostrar_mensajes("Debe establecer cada uno parametros solicitados para realizar el filtrado de incidencias", 
                                  "#212f3d")
        else:
            # Obtener las fechas de filtrado para validar su formato
            fecha_desde = self.obtener_fecha_desde()
            fecha_hasta = self.obtener_fecha_hasta()

            # Verificar si las fechas ingresadas por el usuario no cumplen con el formato DD-MM-AAAA 
            if (not validar_fecha(fecha_desde) or not validar_fecha(fecha_hasta)):
                self.mostrar_mensajes("Formatos de fechas para filtrar incorrecto, formato correcto: DD-MM-AAAA",
                                      "#212f3d")
                return
            
            incidencias_filtradas = self.obtener_incidencias_filtradas()
            self.mostrar_incidencias_registradas(incidencias_filtradas)

    # Metodo para obtener datos de las incidencias registradas para su actualizacion
    def obtener_datos_inidencia_seleccionada(self, e):
        self.id_incidencia_seleccionada = e.control.cells[0].content.value
        self.id_equipo.value = e.control.cells[2].content.value
        self.fecha_reporte.value = e.control.cells[7].content.value
        self.estado_equipo.value = e.control.cells[8].content.value
        self.estado_equipo.hint_text = e.control.cells[8].content.value
        self.descripcion_incidencia.value = e.control.cells[1].content.value

        self.bloquear_registro()
        self.desbloquear_actualizacion_borrar()

        self.page.update()

    # Metodo para registrar incidencia
    def registrar_incidencia(self, e):
        if not self.verificar_datos():
            self.mostrar_mensajes("Debe ingresar todos los datos solicitados para registrar la incidencia",
                                  "#212f3d")
        else:
            fecha_incidencia = self.obtener_fecha_reporte()

            if not validar_fecha(fecha_incidencia):
                self.mostrar_mensajes("Formato de fecha incorrecto, formato correcto: DD-MM-AAAA",
                                      "#212f3d")
                return
            
            id_equipo = str(self.id_equipo.value)

            # Verificar la existencia del equipo en la base de datos
            equipo = self.conn.ejecutar_sql(BUSCAR_EQUIPO, (id_equipo,))

            if len(equipo) > 0:
                datos_incidencia = self.obtener_datos_registro()
                self.conn.ejecutar_sql(REGISTRAR_INCIDENCIA, (*datos_incidencia,))
                self.vaciar_datos()
                self.mostrar_incidencias_registradas(self.obtener_incidencias())
                self.mostrar_mensajes("Incidencia registrada exitosamente", "#138d75")
            else:
                self.mostrar_mensajes("No se encontro equipo registrado con el identificador ingresado",
                                      "#C70039")
              
    # Metodo para actualizar informacion de incidencias
    def actualizar_datos_incidencia(self, e):
        if not self.verificar_datos():
            self.mostrar_mensajes("Debe ingresar todos los datos solicitados para actualizar la incidencia",
                                  "#212f3d")
        else:
            fecha_incidencia = self.obtener_fecha_reporte()

            if not validar_fecha(fecha_incidencia):
                self.mostrar_mensajes("Formato de fecha incorrecto, formato correcto: DD-MM-AAAA",
                                      "#212f3d")
                return
            
            id_equipo = str(self.id_equipo.value)

            # Verificar la existencia del equipo en la base de datos
            equipo = self.conn.ejecutar_sql(BUSCAR_EQUIPO, (id_equipo,))

            if len(equipo) > 0:
                id_incidencia = self.obtner_id_incidencia()
                datos_incidencia = self.obtener_datos_registro()
                
                self.conn.ejecutar_sql(ACTUALIZAR_DATOS_INCIDENCIA, (*datos_incidencia, id_incidencia))
                self.vaciar_id_incidencia_seleccionada()
                self.vaciar_datos()
                self.bloquear_actualizacion_borrar()
                self.desbloquear_registro()
                self.mostrar_incidencias_registradas(self.obtener_incidencias())
                self.mostrar_mensajes("Datos de incidencia actualizados exitosamente", "#138d75")
            else:
                self.mostrar_mensajes("No se encontro equipo registrado con el ID ingresado", 
                                      "#C70039")

    # Metodo para borrar incidencia
    def borrar_incidencia(self, e):
        id_incidencia = self.obtner_id_incidencia()

        self.conn.ejecutar_sql(BORRAR_INCIDENCIA, (id_incidencia,))
        self.vaciar_id_incidencia_seleccionada()
        self.vaciar_datos()
        self.bloquear_actualizacion_borrar()
        self.desbloquear_registro()
        self.mostrar_incidencias_registradas(self.obtener_incidencias())
        self.mostrar_mensajes("Incidencia eliminada exitosamente","#138d75")

    # Metodo para limpiar los datos del modulo al cerrar sesion
    def limpiar_datos_cerrar_sesion(self):
        self.vaciar_id_incidencia_seleccionada()
        self.vaciar_datos()

        self.bloquear_actualizacion_borrar()
        self.desbloquear_registro()

        self.vaciar_inputs_filtrado()
        self.vaciar_tabla_incidencias()