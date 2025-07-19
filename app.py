"""Proyecto Reportes y Notificaciones de Incidencias"""

import flet as ft
from basedatos.conector_db import Conector
from usuario import Usuario
from basedatos.funciones_manejo_db.querys import (SELECCIONAR_USUARIO, SELEC_CREDENCIALES_USUARIO)
from formularios.gestion_dep import GestionDepartamentos
from formularios.gestion_usuarios import GestionUsuarios
from formularios.gestion_equipos import GestionEquipos
from formularios.gestion_incidencias import GestionIncidencias
from formularios.gestion_mantenimientos import GestionMantenimientos
from notificaciones.visualizaciones import VisualizacionesNotif

def main(page: ft.Page):
    """Configuración de la página principal."""
    
    # Establecer el título de la página
    page.title = "Sistema de Reportes y Notificaciones"

    page.window.always_on_top = True
    page.bgcolor = "TRANSPARENT"

    page.decoration = ft.BoxDecoration(
        image=ft.DecorationImage(
            src="img_2.jpg",
            fit=ft.ImageFit.COVER,
        )
    )

    # Alinear los elementos de la pagina al centro
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # funcion para mostrar mensajes en panatalla
    def mostrar_mensajes(mensaje, color):
        barra_mensajes.content = ft.Text(value=mensaje, color="#FFFFFF", size=16)
        barra_mensajes.bgcolor = color
        barra_mensajes.action_color = "#FFFFFF"
        barra_mensajes.open = True
        page.update()


    """Instancia del conector de base de datos"""
    conector = Conector()


    """Instancia del Usuario"""
    usuario_sistema = Usuario()


    """Instancia del modulo de notificaciones"""
    
    vizualizacion_notificaciones = VisualizacionesNotif(page, mostrar_mensajes, conector)


    """Intancia de los formularios"""

    gestion_dep = GestionDepartamentos(page, mostrar_mensajes, conector)

    gestion_usuarios = GestionUsuarios(page, mostrar_mensajes, conector)

    gestion_equipos = GestionEquipos(page, mostrar_mensajes, conector)

    gestion_incidencias = GestionIncidencias(page, usuario_sistema, mostrar_mensajes, conector)

    gestion_mantenimientos = GestionMantenimientos(page, usuario_sistema, mostrar_mensajes, conector)


    """Funciones de manejo de elementos a mostrar en pantalla"""

    # Ordenar la columna de elementos del sistema
    def ordenar_dispocision_sistema(lista_elementos=[]):
        columna_elementos.controls=lista_elementos

    # configurar la fila la superior de formularios con contenido para mostrar
    def configurar_filasuperior(contenido):
        fila_superior_formularios.controls=[
            contenido
        ]
    
    # vaciar la columna de elementos
    def limpiar_columna_elementos():
        columna_elementos.controls.clear()

    # vaciar la fila superior de formularios
    def limpiar_fila_superior_formularios():
        fila_superior_formularios.controls.clear()

    # Mostrar las notificaciones actuales al moverse a la pantalla de notificaciones
    def mostrar_notificaciones():
        limpiar_fila_superior_formularios()
        configurar_filasuperior(vizualizacion_notificaciones.content)

        # Obtener los mantenimientos correspondientes a la fecha actual
        mantenimientos_fecha_actual = vizualizacion_notificaciones.filtrar_mantenimientos()
        
        # Mostrar las notificaciones de los mantenimientos pendientes para la fecha actual
        vizualizacion_notificaciones.mostrar_notificaciones_mantenimientos(mantenimientos_fecha_actual)

        page.update()

    # Mostrar el formulario de gestion de departamentos
    def mostrar_gestion_departamentos():
        limpiar_fila_superior_formularios()
        configurar_filasuperior(gestion_dep.content)

        # Mostrar los departamentos registrados al desplegar el formulario de gestion de departamentos
        gestion_dep.mostrar_dep_registrados()

        page.update()
    
    # Mostrar el formulario de gestion de usuarios
    def mostrar_gestion_usuarios():
        limpiar_fila_superior_formularios()
        configurar_filasuperior(gestion_usuarios.content)
        page.update()
    
    # Mostrar el formulario de gestion de equipos informaticos
    def mostrar_gestion_equipos():
        limpiar_fila_superior_formularios()
        configurar_filasuperior(gestion_equipos.content)
        
        gestion_equipos.vaciar_inputs_filtrado()
        
        gestion_equipos.obtener_departamentos_db()

        equipos_registrados = gestion_equipos.obtener_equipos_registrados()
        gestion_equipos.mostrar_equipos_registrados(equipos_registrados)

        page.update()

    # Mostrar formulario de incidencias
    def mostrar_gestion_incidencias():
        limpiar_fila_superior_formularios()
        configurar_filasuperior(gestion_incidencias.content)
        
        gestion_incidencias.vaciar_inputs_filtrado()

        gestion_incidencias.obtener_departamentos_db()
        
        incidencias_registradas = gestion_incidencias.obtener_incidencias()
        
        gestion_incidencias.mostrar_incidencias_registradas(incidencias_registradas)
        
        page.update()
    
    # Mostrar formulario de mantenimientos
    def mostrar_gestion_mantenimientos():
        limpiar_fila_superior_formularios()
        configurar_filasuperior(gestion_mantenimientos.content)
        
        gestion_mantenimientos.vaciar_datos_filtrado()

        gestion_mantenimientos.obtener_departamentos_db()
        
        mantenimientos_registrados = gestion_mantenimientos.obtener_mantenimientos()
        
        gestion_mantenimientos.mostrar_mantenimientos(mantenimientos_registrados)
        
        page.update()
    
    # Funcion para navegar en el sistema como usuario administrador
    def navegar_opciones_administrador(e):
        indice_seleccionado = e.control.selected_index

        if indice_seleccionado == 0:
            mostrar_notificaciones()

        elif indice_seleccionado == 1:
            mostrar_gestion_departamentos()

        elif indice_seleccionado == 2:
            mostrar_gestion_usuarios()

        elif indice_seleccionado == 3:
            mostrar_gestion_equipos()
        
        elif indice_seleccionado == 4:
            mostrar_gestion_incidencias()
        
        elif indice_seleccionado == 5:
            mostrar_gestion_mantenimientos()
        
        elif indice_seleccionado == 6:
            cerrar_sesion()

    # Funcion para navegar en el sistema como usuario estandar
    def navegar_opciones_estandar(e):
        indice_seleccionado = e.control.selected_index

        if indice_seleccionado == 0:
            mostrar_notificaciones()

        elif indice_seleccionado == 1:
            mostrar_gestion_equipos()
        
        elif indice_seleccionado == 2:
            mostrar_gestion_incidencias()

        elif indice_seleccionado == 3:
            mostrar_gestion_mantenimientos()

        elif indice_seleccionado == 4:
            cerrar_sesion()

    """Funcion para manejar eventos del login"""
    
    # Funcion para verificar si el campo cedula del login esta vacio
    def verificar_ci_ingresada():
        if text_ci_acceso.value:
            return True
        else:
            return False
    
    # Metodo para verificar si el campo clave del login esta vacio
    def verificar_clave_ingresada():
        if text_clave_acceso.value:
            return True
        else:
            return False

    # Obtener la cedula ingresada por el usuario
    def obteter_ci():
        return int(text_ci_acceso.value)

    # Obtener la clave ingresada por el usuario
    def obtener_clave():
        return str(text_clave_acceso.value)
    
    # Vaciar y limpiar el campo de texto de cedula en el login
    def vaciar_campo_ci():
        text_ci_acceso.value = ""
    
    # Vaciar y limpiar el campo de texto de clave en el login
    def vaciar_campo_clave():
        text_clave_acceso.value = ""

    # Limpiar la interfaz de usuario de sus elementos
    def limpiar_interfaz_usuario():
        limpiar_fila_superior_formularios()
        limpiar_columna_elementos()

    # Establecer el fondo del sitema en color blanco al iniciar sesion
    def establecer_fondo_blanco():
        page.bgcolor = "#FFFFFF"

    # Mostrar la imagen de la empresa como fondo del sistema
    def establecer_imagen_fondo():
        page.bgcolor = "TRANSPARENT"
    
    # Establecer las opciones del usuario administrador en la barra de navegacion
    def establecer_opciones_administrador():
        # Añadir a la barra de navegacion solo las opciones del administrador
        barra_navegacion.destinations=[
            destino_vizualizacion_notificaciones,
            destino_gestion_departamentos,
            destino_gestion_usuarios,
            destino_gestion_equipos,
            destino_gestion_incidencias,
            destino_gestion_mantenimientos,
            destino_cerrar_sesion
        ]

    # Establecer las opciones del usuario estandar en la barra de navegacion
    def establecer_opciones_estandar():
        # Añadir a la barra de navegacion solo las opciones del usuario estandar
        barra_navegacion.destinations=[
            destino_vizualizacion_notificaciones,
            destino_gestion_equipos,
            destino_gestion_incidencias,
            destino_gestion_mantenimientos,
            destino_cerrar_sesion
        ]

    # Dar acceso a las pantallas y formularios del usuario administrador
    def dar_acceso_adminsitrador():
        limpiar_interfaz_usuario()

        # Establecer las opciones del usuario administrador
        establecer_opciones_administrador()

        barra_navegacion.on_change = navegar_opciones_administrador

        page.navigation_bar = barra_navegacion

        # Añadir la pantalla de notificaciones a la fila la superior de formularios
        configurar_filasuperior(vizualizacion_notificaciones.content)

        # Añadir a la columna de elementos las secciones del sistema de manera vertical
        ordenar_dispocision_sistema([fila_superior_formularios])

        establecer_fondo_blanco()

        page.update()

    # Dar acceso a las pantallas y formularios del usuario estandar
    def dar_acceso_estandar():
        limpiar_interfaz_usuario()

        # Establecer las opciones del usuario estandar
        establecer_opciones_estandar()

        barra_navegacion.on_change = navegar_opciones_estandar

        page.navigation_bar = barra_navegacion
        
        # Añadir la pantalla de notificaciones a la fila la superior de formularios
        configurar_filasuperior(vizualizacion_notificaciones.content)

        # Añadir a la columna de elementos las secciones del sistema de manera vertical
        ordenar_dispocision_sistema([fila_superior_formularios])

        establecer_fondo_blanco()

        page.update()

    # Iniciar sesion
    def iniciar_sesion(e):
        if not verificar_ci_ingresada() or not verificar_clave_ingresada():
            mostrar_mensajes("Debe ingresar cada una de las credenciales solicitadas", "#212f3d")
        else:
            ci_ingresada = obteter_ci()
            clave_ingresada = obtener_clave()
            usuario = conector.ejecutar_sql(SELECCIONAR_USUARIO, (ci_ingresada,))

            if len (usuario) > 0:
                credenciales_usuario = conector.ejecutar_sql(SELEC_CREDENCIALES_USUARIO, (ci_ingresada,))
                ci, nombre_usuario, clave, tipo_usuario = credenciales_usuario[0]
                
                if clave_ingresada == clave:
                    if tipo_usuario == "Administrador":
                        dar_acceso_adminsitrador()
                    elif tipo_usuario == "Estandar":
                        dar_acceso_estandar()
                    
                    usuario_sistema.establecer_credenciales(ci, nombre_usuario, tipo_usuario)
                    
                    vaciar_campo_ci()
                    vaciar_campo_clave()
                    mostrar_mensajes("Bienvenido al Sistema", "#138d75")
                else:
                    mostrar_mensajes("Clave Incorrecta", "#C70039")
            else:
                mostrar_mensajes("Usuario No Registrado", "#C70039")

    # Cerrar sesion
    def cerrar_sesion():
        limpiar_interfaz_usuario()

        barra_navegacion.selected_index = None

        barra_navegacion.on_change = None

        barra_navegacion.destinations = []

        page.navigation_bar = None        

        # Añadir a la fila superior de formularios el login
        configurar_filasuperior(container_login)

        # Reordenar la columna de elementos solo con el login
        ordenar_dispocision_sistema([fila_superior_formularios])

        # vaciar los inputs de cada uno de los formularios del sistema
        if usuario_sistema.tipo_usuario == "Adminsitrador":
            gestion_usuarios.limpiar_datos_cerrar_sesion() 
            gestion_dep.limpiar_datos_cerrar_sesion()
            
        gestion_equipos.limpiar_datos_cerrar_sesion()        
        gestion_incidencias.limpiar_datos_cerrar_sesion()
        gestion_mantenimientos.limpiar_datos_cerrar_session()      
        
        # Establecer la imagen de la empresa como fondo para el login
        establecer_imagen_fondo()
        
        # limpiar las credenciales del objeto usuario
        usuario_sistema.limpiar_credenciales()
        
        page.update()


    """Creacion y configuracion de los elementos del login"""

    # Crear un texto de descripción del login de la aplicación
    text_descripcion_login = ft.Text(
        value="SISTEMA DE REPORTES Y NOTIFICACIONES", 
        color="White",
        size=24,
        font_family="Sans-Serif",
        weight=ft.FontWeight.BOLD
    )

    # Imagen banner del login
    img_login = ft.Image(src="logo.png", width=400, border_radius=10)

    # Crear campos de texto para los datos de inicio de sesion 
    text_ci_acceso = ft.TextField(label="Cedula:", width=400,
                                  bgcolor="#FFFFFF", border_color="#FFFFFF", 
                                  border_width=15, border_radius=10, 
                                  input_filter=ft.NumbersOnlyInputFilter())
    
    text_clave_acceso = ft.TextField(label="Contraseña:", width=400, 
                              bgcolor="#FFFFFF", border_color="#FFFFFF", 
                              border_width=15, border_radius=10,
                              password=True)
    
    # Crear un botón para iniciar sesión
    boton_inicio_sesion = ft.ElevatedButton(
        on_click=iniciar_sesion,
        text="INICIAR SESION", 
        color="#00008B", 
        width=200, 
        height=50
    )

    # Crear una columna para organizar los elementos de inicio de sesión
    columna_datos_login = ft.Column(
        controls=[text_descripcion_login, img_login, text_ci_acceso, text_clave_acceso, 
                  boton_inicio_sesion]
    )
    columna_datos_login.horizontal_alignment = "Center"
    columna_datos_login.alignment = "Center"
    columna_datos_login.spacing = 20

    # Crear un contenedor para el login
    container_login = ft.Container(
        bgcolor="#00008B",
        border_radius= 25,
        height=400,
        width=600,
        content=columna_datos_login
    )


    """Creacion de los botones de navegacion de la pagina"""

    #Boton para desplegar el formulario de gestion de activos

    destino_vizualizacion_notificaciones = ft.NavigationBarDestination(icon="CIRCLE_NOTIFICATIONS_ROUNDED", 
                                                                       label="NOTIFICACIONES")
    
    destino_gestion_departamentos = ft.NavigationBarDestination(icon="HOME_WORK_ROUNDED", 
                                                                label="DEPARTAMENTOS")
    
    destino_gestion_usuarios = ft.NavigationBarDestination(icon="PERSON", label="USUARIOS")
    
    destino_gestion_equipos = ft.NavigationBarDestination(icon="COMPUTER", label="EQUIPOS")
    
    destino_gestion_incidencias= ft.NavigationBarDestination(icon="WARNING_ROUNDED", label="INCIDENCIAS")

    destino_gestion_mantenimientos = ft.NavigationBarDestination(icon="BUILD_ROUNDED", label="MANTENIMIENTOS")

    destino_cerrar_sesion = ft.NavigationBarDestination(icon="EXIT_TO_APP", label="SALIR")


    """Creacion y configuracion de la barra para mostrar mensajes"""
    
    # Creacion de la barra de mensajes y notificaciones
    barra_mensajes = ft.SnackBar(content=ft.Text(value=""), action="Alright!")
    # Sobreponer la barra de mavegacion por sobre todos los elementos
    page.overlay.append(barra_mensajes)
    # Añadir la barra de notificaciones a page
    page.snack_bar = barra_mensajes


    """Creacion y configuracion de elementos de organizacion de la pagina"""

    # Crear una fila superior para formularios
    fila_superior_formularios = ft.Row(controls=[container_login], expand=True)
    fila_superior_formularios.alignment = "Center"
    
    # Barra de navegacion
    barra_navegacion = ft.NavigationBar(
        destinations=[],
        on_change = None,
        bgcolor= "#FFFFFF",
        indicator_color= "#3030EC"
    )

    # Columna para colocar la fila superior de formularios y la barra de navegacion
    columna_elementos = ft.Column(controls=[fila_superior_formularios], expand= True)

    # Añadir la fila del contenedor de login a la página
    page.add(columna_elementos)

# Ejecutar la aplicación
ft.app(target=main)