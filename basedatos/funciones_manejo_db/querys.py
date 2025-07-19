from basedatos.conector_db import Conector

"""Intrucciones SQL para el control de departamentos"""

# Registrar departamento de la empresa
REGISTER_DEP = """INSERT INTO departamentos(descripcion) VALUES(?)"""

# Obteneter lista de departamentos registrados
OBTENER_DEP = "SELECT * FROM departamentos"

# Buscar un deparamento especifico
BUSCAR_DEP = "SELECT * FROM departamentos WHERE descripcion=?"

# Actualizar datos de departamento
ACTUALIZAR_DEP = "UPDATE departamentos SET descripcion=? WHERE id=?"


"""Intrucciones SQL para manejar usuarios"""

# Registrar usuario
REGISTRAR_USAURIO = """INSERT INTO usuarios(cedula, nombres, 
nombre_usuario, clave, tipo_usuario) VALUES(?, ?, ?, ?, ?)"""

# Seleccionar un usuario especifico 
SELECCIONAR_USUARIO = "SELECT * FROM usuarios WHERE cedula = ?"

SELEC_CREDENCIALES_USUARIO = """SELECT cedula, nombre_usuario, clave, tipo_usuario
FROM usuarios WHERE cedula = ?""" 

# Actualizar datos de un usuario especifico
ACTUALIZAR_DATOS_USUARIO = """UPDATE usuarios SET cedula = ?, nombres=?, nombre_usuario=?, 
clave=?, tipo_usuario=? WHERE cedula=?"""

# Borrar usuario
BORRAR_USUARIO = "DELETE FROM usuarios WHERE cedula = ?"


"""Instrucciones SQL Para manejar equipos"""

# Registrar equipo
REGISTRAR_EQUIPO = """INSERT INTO equipos_informaticos(id_equipo, descripcion, 
marca, modelo, tipo_equipo, id_departamento) VALUES(?, ?, ?, ?, ?, ?)"""

# Buscar un equipo especifico
BUSCAR_EQUIPO = "SELECT * FROM equipos_informaticos WHERE id_equipo = ?"

# Obtener todos los datos equipo
OBTENER_EQUIPOS = """SELECT
e.id_equipo,
e.descripcion,
e.marca,
e.modelo,
e.tipo_equipo,
e.id_departamento,
d.descripcion 
FROM equipos_informaticos AS e
INNER JOIN departamentos AS d
ON e.id_departamento = d.id
"""

# Actualizar los datos de un equipo
ACTUALIZAR_DATOS_EQUIPO = """UPDATE equipos_informaticos set descripcion=?,
marca=?, modelo=?, tipo_equipo=?, id_departamento=? WHERE id_equipo=?"""

# Borrar un equipo
BORRAR_EQUIPO = "DELETE FROM equipos_informaticos WHERE id_equipo = ?"


"""Instrucciones SQL para manejar Incidencias de equipos"""

# Registrar incidencia
REGISTRAR_INCIDENCIA = """INSERT INTO incidencias_equipos(id_equipo_i, ci_usuario,
fecha_reporte, estado_equipo, desc_incidencia) VALUES(?, ?, ?, ?, ?)"""

# Obtener todas las incidencias registradas 
OBTENER_INCIDENCIAS = """
SELECT
inc.id_incidencia,
inc.desc_incidencia,
inc.id_equipo_i,
e.tipo_equipo,
e.marca,
e.modelo,
d.id,
d.descripcion,
inc.ci_usuario,
u.nombres,
inc.fecha_reporte,
inc.estado_equipo
FROM incidencias_equipos AS inc
JOIN equipos_informaticos AS e ON inc.id_equipo_i = e.id_equipo
JOIN departamentos AS d ON e.id_departamento = d.id
JOIN usuarios AS u ON inc.ci_usuario = u.cedula"""

# Actualizar datos de incidencia
ACTUALIZAR_DATOS_INCIDENCIA = """UPDATE incidencias_equipos SET id_equipo_i=?, ci_usuario=?,
fecha_reporte=?, estado_equipo=?, desc_incidencia=? WHERE id_incidencia=?"""

# Borrar incidencia
BORRAR_INCIDENCIA = "DELETE FROM incidencias_equipos WHERE id_incidencia=?"


"""Instrucciones SQL para manejar mantenimientos a equipos"""

# Registrar mantenimiento
REGISTRAR_MANTENIMIENTO = """INSERT INTO mantenimientos_equipos(id_equipo_i, ci_usuario,
fecha_programada, estado_mantenimiento, descripcion) VALUES(?, ?, ?, ?, ?)"""

# Obtener Mantenimientos
OBTENER_MANTENIMIENTOS = """
SELECT
m.id_mantenimiento,
m.descripcion,
m.id_equipo_i,
e.tipo_equipo,
e.marca,
e.modelo,
d.id,
d.descripcion,
m.ci_usuario,
u.nombres,
m.fecha_programada,
m.estado_mantenimiento
FROM mantenimientos_equipos AS m
JOIN equipos_informaticos AS e ON m.id_equipo_i = e.id_equipo
JOIN departamentos AS d ON e.id_departamento = d.id
JOIN usuarios AS u ON m.ci_usuario = u.cedula"""

# Actualizar datos de mantenimiento
ACTUALIZAR_DATOS_MANTENIMIENTO = """UPDATE mantenimientos_equipos SET id_equipo_i = ?, 
ci_usuario = ?, fecha_programada = ?, estado_mantenimiento = ?, 
descripcion = ? WHERE id_mantenimiento = ?"""

# Borrar mantenimiento
BORRAR_MANTENIMIENTO = "DELETE FROM mantenimientos_equipos WHERE id_mantenimiento = ?"

# Completar mantenimiento
ACTUALIZAR_ESTADO_MANTENIMIENTO = """UPDATE mantenimientos_equipos SET estado_mantenimiento=? 
WHERE id_mantenimiento = ?"""