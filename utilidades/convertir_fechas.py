"""Funciones para transformar formatos de fecha"""

# Transforma una fecha de AAAA-MM-DD a DD-MM-AAAA
def transformar_fecha_AAAA_MM_DD(fecha):
    anio, mes, dia = fecha.split('-')
    return f"{dia}-{mes}-{anio}"

# Transforma una fecha de DD-MM-AAAA a AAAA-MM-DD
def transformar_fecha_DD_MM_AAAA(fecha):
    dia, mes, anio = fecha.split('-')
    return f"{anio}-{mes}-{dia}"