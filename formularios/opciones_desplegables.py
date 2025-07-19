"""Opciones de los dropdowns a utilizar en cada pantalla del sistema"""

import flet as ft

# Opciones para el estado de los equipos informaticos
opciones_estado_equipo = [
    ft.dropdown.Option("Operativo"),
    ft.dropdown.Option("Dañado"),
    ft.dropdown.Option("Fuera de Servicio")
    ]

# Opciones para los tipos de equipo 
opciones_tipos_equipos = [
    ft.dropdown.Option("Computador"), 
    ft.dropdown.Option("Impresora"),
    ft.dropdown.Option("Escaner"), 
    ft.dropdown.Option("Ruter"),
    ft.dropdown.Option("Monitor"), 
    ft.dropdown.Option("Periferico"), 
    ft.dropdown.Option("Otro Equipo"),
    ft.dropdown.Option("Otro Periferico")
    ]


# Opciones para los estados de mantenimientos
opciones_estado_mantenimiento = [
    ft.dropdown.Option("Pendiente por realizar"),
    ft.dropdown.Option("En proceso"),
    ft.dropdown.Option("Completado"),
    ft.dropdown.Option("Cancelado"),
    ft.dropdown.Option("Reprogramado")
    ]