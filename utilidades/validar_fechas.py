"""Funcion para validar fechas en formato AAAA-MM-YYYY"""
import re

def validar_fecha(fecha):
    # Patrón para validar el formato DD-MM-YYYY
    patron = r'^\d{2}-\d{2}-\d{4}$'

    if re.match(patron, str(fecha)):
        return True
    else:
        return False

