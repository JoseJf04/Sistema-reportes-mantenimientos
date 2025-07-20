# Sistema-reportes-mantenimientos
Sistema para la gestión de reportes de mantenimientos e incidencias en equipos informáticos con notificaciones

## Caracteristicas 
*   **Base de datos MariaDB**
*   **Diseño intuitivo y moderno**
*   **Interfaz facil de utilizar**
*   **Gestion de usuarios y roles para utilizar el sistema**
*   **Gestion de departamentos y equipos informaticos pertenecientes a estos**
*   **Registro y monitoreo de incidencias ocurridas en los equipos registrados**
*   **Agendado de mantenimientos a equipos y seguimiento de estos**
*   **Notificaciones a los usuarios de mantenimientos a realizar**
*   **Generacion de informes en PDF**

## Instalacion del proyecto

1. **Clona el repositorio**
    ```bash
    git clone https://github.com/JoseJf04/Sistema-reportes-mantenimientos
    cd <repository_directory>
    ```

2. **Creacion del entorno virtual**
*  **Windows**
    ```bash
    python -m venv nombre_del_entorno_virtual
    ```
* **Linux**
    ```bash
    python3 -m venv nombre_del_entorno_virtual
    ```

3. **Activar el entorno virtual**
*   **Windows**
    ```bash
    nombre_del_entorno_virtual\Scripts\activate
    ```
* **Linux**
    ```bash
    source nombre_del_entorno_virtual/bin/activate
    ```

4.  **Instalacion de dependencias**
    ```bash
    pip install -r requirements.txt
    ```

## Importacion de la Base de Datos

*   Importar en el gestor de base de datos el archivo sql ubicado en `/basedatos/DB_sistema.sql`

## Ejecucion del codigo 
* **Windows**
    ```bash
    python -m app.py
    ```
* **Linux**
    ```bash
    python3 -m app.py
    ```