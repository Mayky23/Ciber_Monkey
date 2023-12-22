# pip install pymysql

"""
import pymysql
from pymysql.cursors import DictCursor

class TableColumn:
    def __init__(self, table_name, column_name, data_type, column_value):
        self.table_name = table_name
        self.column_name = column_name
        self.data_type = data_type
        self.column_value = column_value

def mysql_audit_main():
    try:
        # Pedimos datos relevantes para la conexión con la BD
        database_url = input("Ingrese la ruta de la conexión de la base de datos: ")
        username = input("Ingrese el nombre de usuario de la base de datos: ")
        password = input("Ingrese la contraseña de la base de datos: ")

        # Creamos la conexión a la BD
        with pymysql.connect(host=database_url, user=username, password=password, cursorclass=DictCursor) as connection:
            # Resto del código para auditar la base de datos
            check_user_permissions(connection)  # Verificar permisos de usuario
            analyze_security_configurations(connection)  # Analizar configuraciones de seguridad
            check_sql_injection_vulnerabilities(connection)  # Verificar vulnerabilidades de inyección SQL
            find_insecure_data(connection)  # Buscar datos sensibles almacenados de manera insegura
            search_sensitive_data_in_text_columns(connection)  # Buscar datos sensibles en columnas de texto
            check_plain_text_passwords(connection)  # Verificar contraseñas almacenadas en texto plano

    except pymysql.Error as e:
        print(f"Error de la base de datos: {e}")

def check_user_permissions(connection):
    try:
        # Crear un cursor para ejecutar la consulta
        with connection.cursor() as cursor:
            # Ejecutar la consulta para obtener los permisos y roles del usuario actual
            cursor.execute("SHOW GRANTS FOR CURRENT_USER")
            print("Permisos y roles de usuario:")
            
            # Recorrer el conjunto de resultados
            for result in cursor.fetchall():
                print(result["Grants"])
    except pymysql.Error as e:
        print(f"Error al verificar permisos y roles: {e}")

def analyze_security_configurations(connection):
    try:
        # Crear un cursor para ejecutar la consulta
        with connection.cursor() as cursor:
            # Ejecutar la consulta para obtener las configuraciones de seguridad
            cursor.execute("SELECT @@GLOBAL.sql_mode, @@SESSION.sql_mode")
            print("\nConfiguraciones de seguridad:")
            
            # Obtener el modo SQL global y de la sesión
            global_sql_mode, session_sql_mode = cursor.fetchone().values()
            
            # Imprimir las configuraciones de seguridad
            print(f"Modo SQL global: {global_sql_mode}")
            print(f"Modo SQL de la sesión: {session_sql_mode}")
    except pymysql.Error as e:
        print(f"Error al analizar configuraciones de seguridad: {e}")

def check_sql_injection_vulnerabilities(connection):
    try:
        # Solicitar al usuario el nombre de usuario y contraseña para verificar la inyección de SQL
        username = input("Ingrese el nombre de usuario para verificar inyección de SQL: ")
        password = input("Ingrese la contraseña para verificar inyección de SQL: ")

        # Consulta parametrizada para evitar la inyección de SQL
        sql_query = "SELECT * FROM users WHERE username = %s AND password = %s"
        
        # Preparar la declaración con la consulta parametrizada
        with connection.cursor() as cursor:
            # Ejecutar la consulta
            cursor.execute(sql_query, (username, password))
            
            print("\nResultados de consulta para verificar inyección de SQL:")
            if cursor.fetchone():
                print("Se encontraron resultados. Vulnerabilidad de inyección de SQL detectada.")
            else:
                print("No se encontraron resultados. No se detectaron vulnerabilidades de inyección de SQL.")
    except pymysql.Error as e:
        print(f"Error al verificar inyección de SQL: {e}")

def find_insecure_data(connection):
    try:
        # Solicitar al usuario el patrón de datos sensibles para buscar
        sensitive_data_pattern = input("Ingrese el patrón de datos sensibles para buscar: ")

        # Lista para almacenar las columnas sensibles encontradas
        sensitive_columns = []

        # Crear un cursor para ejecutar la consulta
        with connection.cursor() as cursor:
            # Ejecutar la consulta para obtener información de las columnas
            cursor.execute("SELECT * FROM information_schema.columns")
            
            print("\nResultados de consulta para identificar datos sensibles almacenados de manera insegura:")
            
            # Obtener la información de los metadatos del conjunto de resultados
            columns_metadata = [column[0] for column in cursor.description]
            
            # Iterar sobre los resultados
            for result in cursor.fetchall():
                # Obtener el nombre de la tabla actual
                table_name = result["TABLE_NAME"]
                
                # Iterar sobre las columnas del resultado actual
                for column_name, column_value in result.items():
                    # Excluir columnas de metadatos
                    if column_name in columns_metadata:
                        continue
                    
                    # Construir la consulta para buscar el patrón de datos sensibles en la columna actual
                    sql_query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE %s"
                    
                    # Ejecutar la consulta
                    with connection.cursor() as data_cursor:
                        # Establecer el valor del parámetro con el patrón de datos sensibles
                        data_cursor.execute(sql_query, (f"%{sensitive_data_pattern}%",))
                        
                        # Iterar sobre los resultados obtenidos
                        for data_result in data_cursor.fetchall():
                            # Crear una instancia de TableColumn con los valores obtenidos
                            sensitive_column = TableColumn(
                                table_name, column_name, result["DATA_TYPE"], data_result[column_name]
                            )
                            
                            # Agregar la columna sensible a la lista de columnas sensibles
                            sensitive_columns.append(sensitive_column)

        if not sensitive_columns:
            print("No se encontraron resultados. No se detectaron datos sensibles almacenados de manera insegura.")
        else:
            print("Se encontraron resultados. Datos sensibles almacenados de manera insegura detectados:")
            
            # Iterar sobre las columnas sensibles encontradas y mostrar los detalles de cada una
            for column in sensitive_columns:
                print("Tabla:", column.table_name)
                print("Campo:", column.column_name)
                print("Tipo de dato:", column.data_type)
                print("Valor:", column.column_value)
                print()

    except pymysql.Error as e:
        print(f"Error al buscar datos sensibles almacenados de manera insegura: {e}")

def search_sensitive_data_in_text_columns(connection):
    try:
        # Solicitar al usuario el patrón de datos sensibles para buscar en columnas de texto
        sensitive_data_pattern = input("Ingrese el patrón de datos sensibles para buscar en columnas de texto: ")

        # Lista para almacenar las columnas sensibles encontradas
        sensitive_columns = []

        # Crear un cursor para ejecutar la consulta
        with connection.cursor() as cursor:
            # Ejecutar la consulta para obtener información de las columnas de texto
            cursor.execute("SELECT * FROM information_schema.columns WHERE DATA_TYPE IN ('VARCHAR', 'TEXT')")
            
            print("\nResultados de consulta para buscar datos sensibles en columnas de texto:")
            
            # Obtener la información de los metadatos del conjunto de resultados
            columns_metadata = [column[0] for column in cursor.description]
            
            # Iterar sobre los resultados
            for result in cursor.fetchall():
                # Obtener el nombre de la tabla actual
                table_name = result["TABLE_NAME"]
                
                # Iterar sobre las columnas del resultado actual
                for column_name, column_value in result.items():
                    # Excluir columnas de metadatos
                    if column_name in columns_metadata:
                        continue
                    
                    # Construir la consulta para buscar el patrón de datos sensibles en la columna de texto actual
                    sql_query = f"SELECT * FROM {table_name} WHERE {column_name} LIKE %s"
                    
                    # Ejecutar la consulta
                    with connection.cursor() as data_cursor:
                        # Establecer el valor del parámetro con el patrón de datos sensibles
                        data_cursor.execute(sql_query, (f"%{sensitive_data_pattern}%",))
                        
                        # Iterar sobre los resultados obtenidos
                        for data_result in data_cursor.fetchall():
                            # Crear una instancia de TableColumn con los valores obtenidos
                            sensitive_column = TableColumn(
                                table_name, column_name, result["DATA_TYPE"], data_result[column_name]
                            )
                            
                            # Agregar la columna sensible a la lista de columnas sensibles
                            sensitive_columns.append(sensitive_column)

        if not sensitive_columns:
            print("No se encontraron resultados. No se detectaron datos sensibles en columnas de texto.")
        else:
            print("Se encontraron resultados. Datos sensibles en columnas de texto detectados:")
            
            # Iterar sobre las columnas sensibles encontradas y mostrar los detalles de cada una
            for column in sensitive_columns:
                print("Tabla:", column.table_name)
                print("Campo:", column.column_name)
                print("Tipo de dato:", column.data_type)
                print("Valor:", column.column_value)
                print()

    except pymysql.Error as e:
        print(f"Error al buscar datos sensibles en columnas de texto: {e}")

def check_plain_text_passwords(connection):
    try:
        # Crear un cursor para ejecutar la consulta
        with connection.cursor() as cursor:
            # Ejecutar la consulta para obtener todas las filas de la tabla "users"
            cursor.execute("SELECT * FROM users")
            
            print("\nResultados de consulta para verificar contraseñas almacenadas en texto plano:")
            
            # Iterar sobre los resultados de la consulta
            for result in cursor.fetchall():
                # Obtener el nombre de usuario y la contraseña de cada fila
                username = result["username"]
                password = result["password"]

                # Imprimir el nombre de usuario y la contraseña
                print("Usuario:", username)
                print("Contraseña:", password)
                print()
    
    except pymysql.Error as e:
        print(f"Error al verificar contraseñas almacenadas en texto plano: {e}")

if __name__ == "__main__":
    mysql_audit_main()

    
"""