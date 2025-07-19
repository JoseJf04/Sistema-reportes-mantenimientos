"""Formulario de gestion de mantenimientos a equipos"""

import flet as ft

from basedatos.funciones_manejo_db.querys import (REGISTRAR_MANTENIMIENTO, BUSCAR_EQUIPO,
                                                  OBTENER_MANTENIMIENTOS, ACTUALIZAR_DATOS_MANTENIMIENTO,
                                                  BORRAR_MANTENIMIENTO, OBTENER_DEP)

from formularios.opciones_desplegables import (opciones_estado_mantenimiento,
                                               opciones_tipos_equipos)

from PDF.generador_reportes_pdf import PDF

from utilidades.validar_fechas import validar_fecha
from utilidades.convertir_fechas import transformar_fecha_DD_MM_AAAA
from utilidades.convertir_fechas import transformar_fecha_AAAA_MM_DD

class GestionMantenimientos:
    def __init__(self, page, usuario, mostrar_mensajes, conector):
        
        # Referencia del objeto page que contiene todos los elementos de la interfaz
        self.page = page

        # Referencia del objeto usuario
        self.usuario = usuario

        # Referencia del objeto conector de base de datos
        self.conn = conector

        # id mantenimiento selecionado
        self.mantenimiento_seleccionado = None


        """Creacion de los inputs del formulario de gestion de mantenimientos"""
        
        # Texto de descripcion del formulario 
        self.text_desc_formulario = ft.Text(value="Gestion de mantenimientos", style="italic", size=20, color="#FFFFFF")

        # Campo de texto para el id del equipo al que corresponde el mantenimiento
        self.id_equipo = ft.TextField(label="Identificador del equipo", bgcolor="#FFFFFF", border_color="#FFFFFF", 
                                      border_width=15, border_radius=10)
        
        # Campo de texto para la fecha asignada al mantenimiento
        self.fecha_programada = ft.TextField(label="Fecha Agendada DD-MM-AAAA", bgcolor="#FFFFFF", border_color="#FFFFFF",
                                          border_width=15, border_radius=10)
        
        self.fecha_programada.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")

        # Combo de opciones para el estado del mantenimiento
        self.estado_mantenimiento = ft.Dropdown(value="", label="Estado del mantenimiento", bgcolor="#FFFFFF", 
                                         border_color="#FFFFFF", border_width=15, border_radius=10)

        self.estado_mantenimiento.options = opciones_estado_mantenimiento

        # Campo de texto para la descripcion detallada del mantenimiento a realizar
        self.descripcion_mantenimiento = ft.TextField(label="Desc. del mantenimiento a realizar", bgcolor="#FFFFFF", border_color="#FFFFFF",
                                                      border_width=15, border_radius=10, multiline=True)


        """Creacion de los botones para registrar, actualizar y eliminar mantenimientos"""

        # Creacion de los botones para la gestion de mantenimientos
        self.boton_guardar = ft.ElevatedButton(on_click=self.registrar_mantenimiento, text="Registrar", 
                                               color="#00008B", width=90, height=40)

        self.boton_actualizar = ft.ElevatedButton(on_click=self.actualizar_datos_mantenimiento, 
                                                  text="Actualizar", bgcolor="#34495e",
                                                  color="#00008B", width=90, height=40)
        self.boton_actualizar.disabled = True

        self.boton_borrar = ft.ElevatedButton(on_click=self.borrar_mantenimiento, text="Borrar", bgcolor="#34495e",
                                              color="#00008B", width=90, height=40,)
        self.boton_borrar.disabled = True


        """Creacion de los elementos para filtrar y vizualizar mantenimientos registrados"""

        # Texto de descripcion de la tabla de mantenimientos registrados
        self.texto_desc_tabla = ft.Text(value="Tabla de gestion de mantenimientos registrados", style="italic", size=20, color="#FFFFFF")

        # Combo de opciones para seleccionar el departamento por el cual filtrar los mantenimientos
        self.filtrado_departamentos = ft.Dropdown(value="", label="Departamento", width=180, border_width=15, 
                                                  bgcolor="#FFFFFF", border_color="#FFFFFF", border_radius=10)

        # Combo de opciones para seleccionar el tipo de equipo a filtrar
        self.filtrado_tipo_equipo = ft.Dropdown(value="", label="Tipo Equipo", width=155, bgcolor="#FFFFFF", 
                                                border_color="#FFFFFF", border_width=15, border_radius=10)
        
        self.filtrado_tipo_equipo.options = opciones_tipos_equipos

        # Campo de texto para ingresar la fecha inicio del filtrado
        self.filtrado_fecha_desde = ft.TextField(label="Desde:", width=130, bgcolor="#FFFFFF", border_color="#FFFFFF",
                                                   border_width=15, border_radius=10, multiline=True)
        
        self.filtrado_fecha_desde.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")

        # Campo de texto para ingresar la fecha limite del filtrado
        self.filtrado_fecha_hasta = ft.TextField(label="Hasta:", width=130, bgcolor="#FFFFFF", border_color="#FFFFFF",
                                                   border_width=15, border_radius=10, multiline=True)

        self.filtrado_fecha_hasta.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")
        
        # Boton de filtrado de mantenimientos registrados
        self.boton_buscar = ft.IconButton(on_click=self.filtrar_mostrar_mantenimientos, icon="SEARCH", bgcolor="#FFFFFF")

        # Boton para generar reportes de mantenimientos en pdf
        self.boton_generar_pdf = ft.IconButton(on_click=self.guardar_reporte_mantenimientos, icon="PICTURE_AS_PDF_OUTLINED", 
                                               bgcolor="#FFFFFF")

        # Tabla para mostrar los mantenimientos registrados
        self.tabla_mantenimientos = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text(value="ID")),
                ft.DataColumn(ft.Text(value="DESCRIPCION")),
                ft.DataColumn(ft.Text(value="EQUIPO")),
                ft.DataColumn(ft.Text(value="TIPO EQUIPO")),
                ft.DataColumn(ft.Text(value="MARCA")),
                ft.DataColumn(ft.Text(value="MODELO")),
                ft.DataColumn(ft.Text(value="DEPARTAMENTO")),
                ft.DataColumn(ft.Text(value="FECHA")),
                ft.DataColumn(ft.Text(value="ESTADO")),
            ],
            bgcolor="#FFFFFF",
            border_radius=20,
            column_spacing=15,
            expand=True,
            data_row_min_height=50,
            data_row_max_height=100
        )


        """ Referencia de la funcion utilizada para mostrar mensajes al usuario"""
        
        # Funcion Mostrar mensajes
        self.mostrar_mensajes = mostrar_mensajes


        """Creacion de los elementos para colocar y ordenar los inputs del formulario"""
        
        # Fila para colocar los botones de gestion
        self.fila_botones = ft.Row(
            controls=[
                self.boton_guardar,
                self.boton_actualizar,
                self.boton_borrar
            ],
            alignment="Center"
        )

        # Columna para colocar y ordenar verticalmente los elementos del formulario
        self.columna_elementos_formulario = ft.Column(
            controls=[
                self.text_desc_formulario,
                self.id_equipo,
                self.fecha_programada,
                self.estado_mantenimiento,
                self.descripcion_mantenimiento,
                self.fila_botones
            ],
            spacing=20
        )

         # Creacion de la vista de lista para los elementos del formulario
        self.vista_de_lista_formulario = ft.ListView(controls=[self.columna_elementos_formulario])
        
        # Creacion del container para el formulario de gestion
        self.formulario_gestion = ft.Container(
            content=self.vista_de_lista_formulario,
            bgcolor="#00008B",
            border_radius=10,
            col=4,
            padding=15
        )


        """Creacion de los elementos para ordenar los inputs de filtrado y  las vizualizaciones de datos"""
    
        # Fila para colocar los elementos de filtrado
        self.fila_elementos_filtrado = ft.Row(
            controls=[
                self.filtrado_departamentos,
                self.filtrado_tipo_equipo,
                self.filtrado_fecha_desde,
                self.filtrado_fecha_hasta,
                self.boton_buscar,
                self.boton_generar_pdf
            ]
        )

        # Columna para colocar la tabla de mantenimientos registrados
        self.columna_tabla_mantenimientos = ft.Column(
            controls=[
                self.texto_desc_tabla,
                self.fila_elementos_filtrado,
                self.tabla_mantenimientos,
            ],
            spacing=20,
            expand=True
        )

        # Creacion de la vista de lista para la tabla de mantenimientos
        self.vista_de_lista_tabla = ft.ListView(controls=[self.columna_tabla_mantenimientos])

        # Creacion del container para la tabla de mantenimientos regitsrados
        self.tabla_gestion = ft.Container(
            content=self.vista_de_lista_tabla,
            bgcolor="#00008B",
            border_radius=10,
            col=8,
            padding=15
        )


        """Fila principal para todos los elementos del modulo de gestion de mantenimientos"""
        
        # Fila principal
        self.content = ft.ResponsiveRow(
            controls=[
                self.formulario_gestion, 
                self.tabla_gestion
            ],
            expand=True
        )

    """Metodo para generar reportes pdf de matenimientos"""
    def guardar_reporte_mantenimientos(self, e):
        nombre_reporte = ""
        if not(self.verificar_inputs_filtrado()):
            nombre_reporte = "reporte de mantenimientos"
        
        else:
            nombre_reporte = f"reporte de mantenimientos {self.filtrado_fecha_desde.value} hasta {self.filtrado_fecha_hasta.value}"

        pdf = PDF()
        pdf.add_page()

        datos = []
        for fila in self.tabla_mantenimientos.rows:
            datos.append([celda.content for celda in fila.cells])
    
        ancho_de_columnas = [10, 70, 30, 35, 35, 35, 60, 20, 20]
        encabezamiento = ("ID", "DESCRIPCION", "EQUIPO", "TIPO EQUIPO", "MARCA", 
                          "MODELO", "DEPARTAMENTO", "FECHA", "ESTADO")
        
        # Crear la tabla en el PDF de mantenimientos
        pdf.crear_tabla(encabezamiento, datos, ancho_de_columnas)
        
        # Guardar el PDF de mantenimientos
        pdf.output(f"{nombre_reporte}.pdf")


    """Creacion de los metodos del modulo para gestionar los mantenimientos"""

    # Metodo para obtener los departamentos registrados en la base de datos
    def obtener_departamentos_db(self):
        self.filtrado_departamentos.options.clear()
        departamentos = self.conn.ejecutar_sql_seleccion_total(OBTENER_DEP)
        
        for departamento in departamentos:
            self.filtrado_departamentos.options.append(ft.dropdown.Option(text=departamento[1], key=departamento[0]))

    # Metodo para verificar si los inputs del formulario estan vacios
    def verificar_datos(self):
        return not (self.id_equipo.value == "" or self.fecha_programada.value == ""
                    or self.estado_mantenimiento.value == "" 
                    or self.descripcion_mantenimiento.value == "")

    # verificar si los inputs de filtrado estan vacios
    def verificar_inputs_filtrado(self):
        return not (self.filtrado_departamentos.value == "" or self.filtrado_tipo_equipo.value == "" 
                    or self.filtrado_fecha_desde.value == "" or self.filtrado_fecha_hasta.value == "")
    
    # Metodo para obtener el id del mantenimiento seleccionado
    def obtener_id_mantenimiento(self):
        return int(self.mantenimiento_seleccionado)

    # Metodo para obtener la fecha del mantenimiento
    def obtener_fecha_mantenimiento(self):
        fecha_mantenimiento = str(self.fecha_programada.value)
        return fecha_mantenimiento

    # Metodo para obtener del formulario los datos ingresados para el registro o actualizacion de mantenimientos
    def obtener_datos(self):
        id_equipo = str(self.id_equipo.value)
        ci_usuario = int(self.usuario.obtener_ci_usuario())
        fecha_mantenimiento = transformar_fecha_DD_MM_AAAA(self.obtener_fecha_mantenimiento())
        estado = str(self.estado_mantenimiento.value)
        descripcion = str(self.descripcion_mantenimiento.value)

        return id_equipo, ci_usuario, fecha_mantenimiento, estado, descripcion

    # Metodo para obtener la fecha inicio por la cual filtrar los mantenimientos
    def obtener_fecha_desde(self):
        fecha_desde = str(self.filtrado_fecha_desde.value)
        return fecha_desde
    
    # Metodo para obtener la fecha limite por la cual filtrar los mantenimientos
    def obtener_fecha_hasta(self):
        fecha_hasta = str(self.filtrado_fecha_hasta.value)
        return fecha_hasta

    # obtener datos de los inputs de filtrado 
    def obtener_datos_para_filtrado(self):
        departamento = self.filtrado_departamentos.value
        tipo_equipo = self.filtrado_tipo_equipo.value
        fecha_desde = transformar_fecha_DD_MM_AAAA(self.obtener_fecha_desde())
        fecha_hasta = transformar_fecha_DD_MM_AAAA(self.obtener_fecha_hasta())

        return departamento, tipo_equipo, fecha_desde, fecha_hasta

    # Metodo para establcer el atributo mantenimiento_seleccionado en None
    def vaciar_mantenimiento_seleccionado(self):
        self.mantenimiento_seleccionado = None

    # Metodo para vaciar los inputs del formulario
    def vaciar_datos(self):
        self.id_equipo.value = ""
        self.fecha_programada.value = ""
        self.estado_mantenimiento.value = ""
        self.estado_mantenimiento.hint_text = ""
        self.descripcion_mantenimiento.value = ""

    # Metodo para vaciar los inputs de filtrado
    def vaciar_datos_filtrado(self):
        self.filtrado_departamentos.value = ""
        self.filtrado_departamentos.hint_text = ""
        self.filtrado_tipo_equipo.value = ""
        self.filtrado_tipo_equipo.hint_text = ""
        self.filtrado_fecha_desde.value = ""
        self.filtrado_fecha_hasta.value = ""

    # Metodo para vaciar la tabla de mantenimientos registrados
    def vaciar_tabla_mantenimientos(self):
        self.tabla_mantenimientos.rows.clear()

    # Metodo para bloquear el boton de registro
    def bloquear_registro(self):
        self.boton_guardar.disabled = True
        self.boton_guardar.bgcolor = "#34495e"
    
    # Metodo para desbloquear el boton de registro
    def desbloquear_registro(self):
        self.boton_guardar.disabled = False
        self.boton_guardar.bgcolor = "#FFFFFF"

    # Metodo para bloquear los botones de actualizacion y borrado
    def bloquear_actualizacion_borrar(self):
        self.boton_actualizar.disabled = True
        self.boton_borrar.disabled = True

        self.boton_actualizar.bgcolor = "#34495e"
        self.boton_borrar.bgcolor = "#34495e"

    # Metodo para desbloquear los botones de actualizacion y borrado
    def desbloquear_actualizacion_borrar(self):
        self.boton_actualizar.disabled = False
        self.boton_borrar.disabled = False

        self.boton_actualizar.bgcolor = "#FFFFFF"
        self.boton_borrar.bgcolor = "#FFFFFF"

    # Metodo para obtener los datos de un mantenimiento de la tabla de mantenimientos registrados
    def obtener_mantenimiento_seleccionado(self, e):
        self.mantenimiento_seleccionado = e.control.cells[0].content.value
        self.id_equipo.value = e.control.cells[2].content.value
        self.fecha_programada.value = e.control.cells[7].content.value
        self.estado_mantenimiento.value = e.control.cells[8].content.value
        self.estado_mantenimiento.hint_text = e.control.cells[8].content.value
        self.descripcion_mantenimiento.value = e.control.cells[1].content.value

        self.bloquear_registro()
        self.desbloquear_actualizacion_borrar()

        self.page.update()

    # Metodo para ontener todos los mantenimientos registrados
    def obtener_mantenimientos(self):
        # Obtener todos los mantenimientos registrados
        sql_obtener_mantenimientos = OBTENER_MANTENIMIENTOS + " ORDER BY id_mantenimiento DESC LIMIT 20"
        mantenimientos = self.conn.ejecutar_sql_seleccion_total(sql_obtener_mantenimientos)
        return mantenimientos

    # Metodo para obtener los mantenimientos mediante filtrado
    def obtener_mantenimientos_filtrados(self):
        # Obtener los valores ingresados en los inputs de filtrado de mantenimientos
        datos_filtrado = self.obtener_datos_para_filtrado()
        
        # Modificar la consulta de seleccion de mantenimientos para filtrado
        sql_filtrado_mantenimientos = OBTENER_MANTENIMIENTOS + """ WHERE d.id = ? AND e.tipo_equipo = ? 
        AND m.fecha_programada BETWEEN ? AND ?"""
        
        # Obtener los mantenimientos filtrados
        mantenimientos_filtrados = self.conn.ejecutar_sql(sql_filtrado_mantenimientos, (*datos_filtrado,))
        return mantenimientos_filtrados

    # Metodo para mostrar los mantenimientos registrados
    def mostrar_mantenimientos(self, mantenimientos):
        # Limpiar la tablas de mantenimientos
        self.vaciar_tabla_mantenimientos()

        for mantenimiento in mantenimientos:
            self.tabla_mantenimientos.rows.append(
                ft.DataRow(
                    cells=[
                        # ID mantenimiento
                        ft.DataCell(ft.Text(value=mantenimiento[0])),
                        ft.DataCell(ft.Text(value=mantenimiento[1])),
                        ft.DataCell(ft.Text(value=mantenimiento[2])),
                        ft.DataCell(ft.Text(value=mantenimiento[3])),
                        ft.DataCell(ft.Text(value=mantenimiento[4])),
                        ft.DataCell(ft.Text(value=mantenimiento[5])),
                        ft.DataCell(ft.Text(value=mantenimiento[7])),
                        ft.DataCell(
                            ft.Text(
                                value=transformar_fecha_AAAA_MM_DD(str(mantenimiento[10]))
                            )
                        ),
                        ft.DataCell(ft.Text(value=mantenimiento[11])),
                    ], on_select_changed = self.obtener_mantenimiento_seleccionado                )
            )

        self.page.update()

    # Metodo para filtrar y mostrar los mantenimientos en la tabla
    def filtrar_mostrar_mantenimientos(self, e):
        if not self.verificar_inputs_filtrado():
            self.mostrar_mensajes("Debe establecer cada uno parametros solicitados para realizar el filtrado de mantenimientos", 
                                  "#212f3d")
        else:
            # Obtener las fechas ingresadas por el usuario para el filtrado de mantenimientos
            fecha_desde = self.obtener_fecha_desde()
            fecha_hasta = self.obtener_fecha_hasta()

            # Verificar si las fechas de filtrado ingresadas por el usuario no cumplen con el formato DD-MM-AAAA
            if (not validar_fecha(fecha_desde) or not validar_fecha(fecha_hasta)):
                self.mostrar_mensajes("Formato de fechas para filtrar incorrecto, formato correcto: DD-MM-AAAA",
                                      "#212f3d")
                return
            
            mantenimientos_filtrados = self.obtener_mantenimientos_filtrados()
            self.mostrar_mantenimientos(mantenimientos_filtrados)

    # Metodo para registrar mantenimiento de equipo
    def registrar_mantenimiento(self, e):
        if not self.verificar_datos():
            self.mostrar_mensajes("Debe ingresar todos los datos solicitados para registrar",
                                  "#212f3d")
        else:
            fecha_mantenimiento = self.fecha_programada.value
            
            if not validar_fecha(fecha_mantenimiento):
                self.mostrar_mensajes("Formato de fecha incorrecto, formato correcto: DD-MM-AAAA",
                                      "#212f3d")
                return

            id_equipo = str(self.id_equipo.value)

            # consultar la existencia del equipo al que se le quiere registrar un mantenimiento
            equipo = self.conn.ejecutar_sql(BUSCAR_EQUIPO, (id_equipo,))

            if len(equipo) > 0:
                datos_mantenimiento = self.obtener_datos()
                self.conn.ejecutar_sql(REGISTRAR_MANTENIMIENTO, (*datos_mantenimiento,))
                self.vaciar_datos()
                self.mostrar_mensajes("Mantenimiento registrado exitosamente",
                                      "#138d75")
                self.mostrar_mantenimientos(self.obtener_mantenimientos())
            else:
                self.mostrar_mensajes("No se encontro equipo registrado con el identificador ingresado",
                                      "#C70039")

    # Metodo para actualizar los datos de una incidencia
    def actualizar_datos_mantenimiento(self, e):
        if not self.verificar_datos():
            self.mostrar_mensajes("Debe ingresar todos los datos solicitados para actualizar", 
                                  "#212f3d")
        else:
            fecha_mantenimiento = self.fecha_programada.value

            if not validar_fecha(fecha_mantenimiento):
                self.mostrar_mensajes("Formato de fecha incorrecto, formato correcto: DD-MM-AAAA",
                                      "#212f3d")
                return 

            id_equipo = str(self.id_equipo.value)
            
            # Consultar la existencia del equipo al que se le quiere actualizar el mantenimiento 
            equipo = self.conn.ejecutar_sql(BUSCAR_EQUIPO, (id_equipo,))

            if len(equipo) > 0:
                mantenimiento_selecionado = self.obtener_id_mantenimiento()
                datos_mantenimiento = self.obtener_datos()
                
                self.conn.ejecutar_sql(ACTUALIZAR_DATOS_MANTENIMIENTO, (*datos_mantenimiento, mantenimiento_selecionado))
                self.vaciar_mantenimiento_seleccionado()
                self.vaciar_datos()
                self.bloquear_actualizacion_borrar()
                self.desbloquear_registro()
                self.mostrar_mantenimientos(self.obtener_mantenimientos())
                self.mostrar_mensajes("Datos de mantenimiento actualizados exitosamente", 
                                      "#138d75")
            else:
                self.mostrar_mensajes("No se encontro equipo registrado con el identificador ingresado", 
                                      "#C70039")
    
    # Metodo para borrar mantenimiento
    def borrar_mantenimiento(self, e):
        mantenimiento_selecionado = self.obtener_id_mantenimiento()
        self.conn.ejecutar_sql(BORRAR_MANTENIMIENTO, (mantenimiento_selecionado,))
        self.vaciar_mantenimiento_seleccionado()
        self.vaciar_datos()
        self.bloquear_actualizacion_borrar()
        self.desbloquear_registro()
        self.mostrar_mantenimientos(self.obtener_mantenimientos())
        self.mostrar_mensajes("Mantenimiento borrado exitosamente", "#138d75")

    # Metodo para los elementos del modulo al cerrar sesion
    def limpiar_datos_cerrar_session(self):
        self.vaciar_mantenimiento_seleccionado()
        self.vaciar_datos()
       
        self.bloquear_actualizacion_borrar()
        self.desbloquear_registro()
        
        self.vaciar_datos_filtrado()
        self.vaciar_tabla_mantenimientos()