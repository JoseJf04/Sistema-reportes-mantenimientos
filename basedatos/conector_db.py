import mariadb

"""Creacion de la clase conector para manejar la base de datos"""

# Clase Conector para manejar la base de datos
class Conector:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3306
        self.user = "root"
        self.password = "1234"
        self.database = "db_sistema_reportes_mantenimientos"

        self.conn = None
        self.cursor = None

    # Metodo para establecer la conexion
    def establecer_conexion(self):
        try:
            # Creacion del conector
            self.conn = mariadb.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
            )

            # Creacion del cursor
            self.cursor = self.conn.cursor()

            # Imprimir el estado de la conexion exitosa
            print("Conexion exitosa")

        except mariadb.Error as err:
            print(err)
            self.conn = None
            self.cursor = None

    # Metodo para cerrar la conexion
    def cerrar_conexion(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()

        self.conn = None
        self.cursor = None

        print("Conexion cerrada exitosamente")

    # Metodo para ejecutar la seleccion completa de una tabla
    def ejecutar_sql_seleccion_total(self, seleccion_sql):
        try:
            # Llamda del metodo establecer conexion
            self.establecer_conexion()

            # Ejecucion de la consulta
            self.cursor.execute(seleccion_sql)

            # Obtener los datos en el cursor
            datos = self.cursor.fetchall()

            # Cerrar la conexion con la base de datos
            self.cerrar_conexion()

            # Retornar los datos
            return datos

        except mariadb.mariadb.Error as err:
            print(err)

    # Metodo para ejecutar querys de lectura, escritura y modificacion de datos
    def ejecutar_sql(self, instruccion, parametros):
        try:
            # llamada al metodo establcer conexion
            self.establecer_conexion()

            # Ejecucion de la instruccion SQL mediante el cursor
            self.cursor.execute(instruccion, parametros)

            # Verificacion de la instruccion para ejecutar commit
            if instruccion.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.conn.commit()
                print("Operacion realizada exitosamente")

            # Verificacion de la instruccion para devolver los datos consultados
            if instruccion.strip().upper().startswith('SELECT'):
                datos = self.cursor.fetchall()
                self.cerrar_conexion()
                return datos

            # Cerras la conexion
            self.cerrar_conexion()

        except mariadb.Error as err:
            print(err)
            self.cerrar_conexion()
