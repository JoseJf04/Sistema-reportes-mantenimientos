"""Pantalla de visualizacion de notificaciones"""

import flet as ft

from datetime import datetime

from basedatos.funciones_manejo_db.querys import(OBTENER_MANTENIMIENTOS, ACTUALIZAR_ESTADO_MANTENIMIENTO)

from utilidades.validar_fechas import validar_fecha
from utilidades.convertir_fechas import transformar_fecha_DD_MM_AAAA

class VisualizacionesNotif:
    def __init__(self, page, mostrar_mensajes, conector):
        # Referencia del objeto conector a base de datos
        self.conn = conector
        
        # Referencia del objeto page que contiene todos los elementos de la interfaz
        self.page = page

        # Texto de descripcion del modulo para el usuario
        self.texto_descripcion = ft.Text(value="Notificaciones de Mantenimientos por Realizar", 
                                         size=24, color="#FFFFFF")
        
        # Campo de texto para indicar la fecha del filtrado de notificaciones
        self.filtrado_fecha = ft.TextField(label="Fecha de notificaciones a consultar DD-MM-AAAA:", width=450, bgcolor="#FFFFFF", 
                                           border_color="#FFFFFF", border_width=15, border_radius=10)

        self.filtrado_fecha.input_filter = ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")

        # Creacion del boton para filtrar
        self.boton_filtrar = ft.IconButton(on_click=self.filtrar_mostrar_mantenimientos, icon="SEARCH", bgcolor="#FFFFFF", icon_color="#00008B")
        
        # Referencia de la funcion utilizada para mostrar mensajes
        self.mostrar_mensajes = mostrar_mensajes

        # Creacion de la fila para colocar y centrar el texto de descripcion
        self.fila_texto_desc = ft.Row(controls=[self.texto_descripcion], 
                                      alignment="Center")

        # Creacion de la fila para colocar y centrar los elementos de filtrado
        self.fila_elementos_filtrado = ft.Row(controls=[self.filtrado_fecha, 
                                                        self.boton_filtrar,],
                                                        alignment=ft.MainAxisAlignment.CENTER)

        
        # Creacion del panel de la lista de notificaciones        
        self.panel_lista_notificaciones = ft.ExpansionPanelList(
            expand_icon_color="#000000",
            elevation=8,
            divider_color = "#FFFFFF",
        )

        # Columna para colocar y ordenar los elementos de forma vertical
        self.columna_elementos = ft.Column(controls=[self.fila_texto_desc, self.fila_elementos_filtrado,
                                                     self.panel_lista_notificaciones],
                                                     spacing=30)
        
        # Vista de lista para desplazarse verticalmente entre las notificaciones
        self.vista_lista = ft.ListView(controls=[self.columna_elementos])
        
        # Container de los elementos
        self.container_elementos = ft.Container(
            bgcolor= "#00008B",
            content=self.vista_lista,
            border_radius=10,
            padding=25,
        )

        # Fila responsiva para colocar el container de elementos
        self.content = ft.ResponsiveRow(controls=[self.container_elementos], expand=True)

        self.mostrar_notificaciones_mantenimientos(self.filtrar_mantenimientos())

    # Metodo para obtener las fecha inicio de mantenimiento para filtrar
    def obtener_fecha_desde(self):
        fecha_desde = str(self.filtrado_fecha.value)

        return fecha_desde

    # Metodo para completar mantenimientos
    def completar_mantenimiento(self, e: ft.ControlEvent):
        panel = e.control.data

        indice_notificacion = panel.header.value

        self.conn.ejecutar_sql(ACTUALIZAR_ESTADO_MANTENIMIENTO, ("Completado", indice_notificacion))

        print(f"Se completo el mantenimiento: {indice_notificacion}")
        
        self.mostrar_notificaciones_mantenimientos(self.filtrar_mantenimientos)

    # Metodo para obtener los mantenimientos filtrados
    def filtrar_mantenimientos(self, fecha_desde=None):
        
        sql_filtrado_mantenimiento = OBTENER_MANTENIMIENTOS + """ WHERE m.fecha_programada = ?
        AND (m.estado_mantenimiento = 'Pendiente por realizar' 
        OR m.estado_mantenimiento = 'En proceso' 
        OR m.estado_mantenimiento = 'Reprogramado')
        ORDER BY m.id_mantenimiento DESC"""

        mantenimientos= None

        if (not fecha_desde):
            fecha = datetime.now()
            fecha_actual = f"{fecha.year}-{fecha.month}-{fecha.day}"
            
            mantenimientos = self.conn.ejecutar_sql(sql_filtrado_mantenimiento, (fecha_actual,))
        
        else:

            fecha_desde = transformar_fecha_DD_MM_AAAA(fecha_desde)

            mantenimientos = self.conn.ejecutar_sql(sql_filtrado_mantenimiento, (fecha_desde,))

        return mantenimientos
    
    # Metodo para mostrar las notificaciones
    def mostrar_notificaciones_mantenimientos(self, mantenimientos):
        
        self.panel_lista_notificaciones.controls.clear()

        for mantenimiento in mantenimientos:
            # Obtener cada uno de los datos esenciales a mostrar en la notificacion
            identificador = mantenimiento[0] # Identificador del mantenimiento
            descripcion = mantenimiento[1] # Descripcion del mantenimiento a realizar
            equipo = mantenimiento[2] # Equipo a realizar mantenimiento
            tipo_equipo = mantenimiento[3] # tipo de equipo
            marca_equipo = mantenimiento[4] # marca del equipo
            modelo_equipo = mantenimiento[5] # Modelo del equipo
            departamento = mantenimiento[7] # Departamento donde realizar el mantenimiento
            usuario = mantenimiento[9] # Usuario encargado del mantenimiento
            estado= mantenimiento[11] # Estado del mantenimiento

            # Creacion del expansionpanel que contendra la notificacion
            exp_n = ft.ExpansionPanel(
                bgcolor= "#0030B3",
                
                header=ft.Text(identificador, size=16, color="#FFFFFF"),
                expanded=True,
            )   

            # Establecer el contenido a mostrar en el expansion panel de la notificacion
            exp_n.content = ft.ListTile(
                # Titulo del la notificacion con descripcion de del mantenimiento a realizar
                title=ft.Text(f"Tarea a realizar: {descripcion} al equipo {equipo} {tipo_equipo} {marca_equipo} {modelo_equipo}",
                              color="#000000", size=18),
                
                # Subtitulo de especificacion del usuario al que le corresponde realizar la tarea 
                subtitle=ft.Text(f"""\nUsuario encargado de la tarea: {usuario} en el departamento de {departamento} ({estado})"""),
                
                bgcolor="#FFFFFF",
                trailing= ft.IconButton(icon="CHECK_ROUNDED", bgcolor="#0366CA", icon_color="#FFFFFF",
                                        on_click=self.completar_mantenimiento, data=exp_n)
            )

            self.panel_lista_notificaciones.controls.append(exp_n)
        
        self.page.update()

    # Metodo para filtrar y mostrar los mantenimientos
    def filtrar_mostrar_mantenimientos(self, e):
        fecha_desde = self.obtener_fecha_desde()

        if not validar_fecha(fecha_desde):
            self.mostrar_mensajes("Formato de fecha incorrecto, formato correcto: DD-MM-AAAA",
                                  "")
        
        else:
            mantenimientos = self.filtrar_mantenimientos(fecha_desde)
            self.mostrar_notificaciones_mantenimientos(mantenimientos)

