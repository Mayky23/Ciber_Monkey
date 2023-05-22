package Auditar_BD_SQL;


import java.sql.Connection;        // Establecer la conexión con la base de datos
import java.sql.DriverManager;     // Administración de controladores de bases de datos
import java.sql.PreparedStatement; // Ejecutar consultas con parametros
import java.sql.ResultSet;         // Obtener los resultados de las consultas
import java.sql.ResultSetMetaData; // Obtener metadatos de los resultados de las consultas
import java.sql.SQLException;      // Manejar las excepciones de la base de datos
import java.sql.Statement;         // Ejecutar instrucciones SQL
import java.util.ArrayList;        // Almacenar objetos en una lista dinámica
import java.util.List;             // Para trabajar con colecciones ordenadas
import java.util.Scanner;          // Leer la entrada del usuario

public class Auditar_BD {

    public static void main(String[] args) {

        //Pedimos datos relevantes para la conexión con la BD
        Scanner scanner = new Scanner(System.in);

        System.out.print("Ingrese la ruta de la conexión de la base de datos: ");
        String databaseUrl = scanner.nextLine();

        System.out.print("Ingrese el nombre de usuario de la base de datos: ");
        String username = scanner.nextLine();

        System.out.print("Ingrese la contraseña de la base de datos: ");
        String password = scanner.nextLine();

        //Creamos la conexión a la BD
        try (Connection connection = DriverManager.getConnection(databaseUrl, username, password)) {

            // Resto del código para auditar la base de datos
            checkUserPermissions(connection); // Verificar permisos de usuario
            analyzeSecurityConfigurations(connection); // Analizar configuraciones de seguridad
            checkSQLInjectionVulnerabilities(connection); // Verificar vulnerabilidades de inyección SQL
            findInsecureData(connection); // Buscar datos sensibles almacenados de manera insegura
            searchSensitiveDataInTextColumns(connection); // Buscar datos sensibles en columnas de texto
            checkPlainTextPasswords(connection); // Verificar contraseñas almacenadas en texto plano
        
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    // Método para verificar los permisos y roles del usuario actual
    private static void checkUserPermissions(Connection connection) throws SQLException {
        // Crear una declaración para ejecutar la consulta
        Statement statement = connection.createStatement();
        
        // Ejecutar la consulta para obtener los permisos y roles del usuario actual
        ResultSet resultSet = statement.executeQuery("SHOW GRANTS FOR CURRENT_USER");

        System.out.println("Permisos y roles de usuario:");
        // Recorrer el conjunto de resultados
        while (resultSet.next()) {
            // Obtener el permiso/rol actual
            String grant = resultSet.getString(1);
            
            // Imprimir el permiso/rol actual
            System.out.println(grant);
        }
        
        // Cerrar el conjunto de resultados y la declaración
        resultSet.close();
        statement.close();
    }


    // Método para analizar las configuraciones de seguridad de la base de datos
    private static void analyzeSecurityConfigurations(Connection connection) throws SQLException {
        // Crear una declaración para ejecutar la consulta
        Statement statement = connection.createStatement();
        
        // Ejecutar la consulta para obtener las configuraciones de seguridad
        ResultSet resultSet = statement.executeQuery("SELECT @@GLOBAL.sql_mode, @@SESSION.sql_mode");

        System.out.println("\nConfiguraciones de seguridad:");
        // Verificar si hay resultados
        if (resultSet.next()) {
            // Obtener el modo SQL global y de la sesión
            String globalSqlMode = resultSet.getString(1);
            String sessionSqlMode = resultSet.getString(2);
            
            // Imprimir las configuraciones de seguridad
            System.out.println("Modo SQL global: " + globalSqlMode);
            System.out.println("Modo SQL de la sesión: " + sessionSqlMode);
        }
        
        // Cerrar el conjunto de resultados y la declaración
        resultSet.close();
        statement.close();
    }

    // Método para verificar vulnerabilidades de inyección de SQL
    private static void checkSQLInjectionVulnerabilities(Connection connection) throws SQLException {
        Scanner scanner = new Scanner(System.in);
        
        // Solicitar al usuario el nombre de usuario y contraseña para verificar la inyección de SQL
        System.out.print("Ingrese el nombre de usuario para verificar inyección de SQL: ");
        String username = scanner.nextLine();

        System.out.print("Ingrese la contraseña para verificar inyección de SQL: ");
        String password = scanner.nextLine();

        // Consulta parametrizada para evitar la inyección de SQL
        String sqlQuery = "SELECT * FROM users WHERE username = ? AND password = ?";
        
        // Preparar la declaración con la consulta parametrizada
        try (PreparedStatement statement = connection.prepareStatement(sqlQuery)) {
            // Establecer los valores de los parámetros
            statement.setString(1, username);
            statement.setString(2, password);
            
            // Ejecutar la consulta
            ResultSet resultSet = statement.executeQuery();

            System.out.println("\nResultados de consulta para verificar inyección de SQL:");
            if (resultSet.next()) {
                System.out.println("Se encontraron resultados. Vulnerabilidad de inyección de SQL detectada.");
            } else {
                System.out.println("No se encontraron resultados. No se detectaron vulnerabilidades de inyección de SQL.");
            }
            
            // Cerrar el conjunto de resultados
            resultSet.close();
        }
    }

    // Método para buscar datos sensibles almacenados de manera insegura
    private static void findInsecureData(Connection connection) throws SQLException {
        Scanner scanner = new Scanner(System.in);
        
        // Solicitar al usuario el patrón de datos sensibles para buscar
        System.out.print("Ingrese el patrón de datos sensibles para buscar: ");
        String sensitiveDataPattern = scanner.nextLine();

        // Lista para almacenar las columnas sensibles encontradas
        List<TableColumn> sensitiveColumns = new ArrayList<>();

        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("SELECT * FROM information_schema.columns");

        System.out.println("\nResultados de consulta para identificar datos sensibles almacenados de manera insegura:");
        
        // Obtener la información de los metadatos del conjunto de resultados
        ResultSetMetaData metaData = resultSet.getMetaData();
        
        while (resultSet.next()) {
            // Obtener el nombre de la tabla actual del conjunto de resultados
            String tableName = resultSet.getString("TABLE_NAME");
            
            // Obtener el nombre de la columna actual del conjunto de resultados
            String columnName = resultSet.getString("COLUMN_NAME");
            
            // Obtener el tipo de dato de la columna actual del conjunto de resultados
            String dataType = resultSet.getString("DATA_TYPE");
        
            // Construir la consulta para buscar el patrón de datos sensibles en la columna actual
            String sqlQuery = "SELECT * FROM " + tableName + " WHERE " + columnName + " LIKE ?";
            
            try (PreparedStatement dataStatement = connection.prepareStatement(sqlQuery)) {
                // Establecer el valor del parámetro con el patrón de datos sensibles
                dataStatement.setString(1, "%" + sensitiveDataPattern + "%");
                
                ResultSet dataResultSet = dataStatement.executeQuery();
        
                while (dataResultSet.next()) {
                    // Obtener el valor de la columna actual del conjunto de resultados de datos
                    String columnValue = dataResultSet.getString(columnName);
                    
                    // Crear una instancia de TableColumn con los valores obtenidos
                    TableColumn sensitiveColumn = new TableColumn(tableName, columnName, dataType, columnValue);
                    
                    // Agregar la columna sensible a la lista de columnas sensibles
                    sensitiveColumns.add(sensitiveColumn);
                }
        
                dataResultSet.close();
            }
        }        

        if (sensitiveColumns.isEmpty()) {
            // No se encontraron resultados, lo que significa que no se detectaron datos sensibles almacenados de manera insegura
            System.out.println("No se encontraron resultados. No se detectaron datos sensibles almacenados de manera insegura.");
        } else {
            // Se encontraron resultados, lo que indica que se detectaron datos sensibles almacenados de manera insegura
            System.out.println("Se encontraron resultados. Datos sensibles almacenados de manera insegura detectados:");
            
            // Iterar sobre las columnas sensibles encontradas y mostrar los detalles de cada una
            for (TableColumn column : sensitiveColumns) {
                System.out.println("Tabla: " + column.getTableName());
                System.out.println("Campo: " + column.getColumnName());
                System.out.println("Tipo de dato: " + column.getDataType());
                System.out.println("Valor: " + column.getColumnValue());
                System.out.println();
            }
        }
        
        // Cerrar el conjunto de resultados y la declaración
        resultSet.close();
        statement.close();
        
    }

    // Método para buscar datos sensibles en columnas de texto
    private static void searchSensitiveDataInTextColumns(Connection connection) throws SQLException {
        Scanner scanner = new Scanner(System.in);
        
        // Solicitar al usuario el patrón de datos sensibles para buscar en columnas de texto
        System.out.print("Ingrese el patrón de datos sensibles para buscar en columnas de texto: ");
        String sensitiveDataPattern = scanner.nextLine();

        // Lista para almacenar las columnas sensibles encontradas
        List<TableColumn> sensitiveColumns = new ArrayList<>();

        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("SELECT * FROM information_schema.columns WHERE DATA_TYPE IN ('VARCHAR', 'TEXT')");

        System.out.println("\nResultados de consulta para buscar datos sensibles en columnas de texto:");
        
        // Obtener la información de los metadatos del conjunto de resultados
        ResultSetMetaData metaData = resultSet.getMetaData();
        
        while (resultSet.next()) {
            // Obtener el nombre de la tabla actual del conjunto de resultados
            String tableName = resultSet.getString("TABLE_NAME");
            
            // Obtener el nombre de la columna actual del conjunto de resultados
            String columnName = resultSet.getString("COLUMN_NAME");
            
            // Obtener el tipo de dato de la columna actual del conjunto de resultados
            String dataType = resultSet.getString("DATA_TYPE");
        
        
            // Construir la consulta para buscar el patrón de datos sensibles en la columna de texto actual
            String sqlQuery = "SELECT * FROM " + tableName + " WHERE " + columnName + " LIKE ?";
            
            try (PreparedStatement dataStatement = connection.prepareStatement(sqlQuery)) {
                // Establecer el valor del parámetro con el patrón de datos sensibles
                dataStatement.setString(1, "%" + sensitiveDataPattern + "%");
                
                // Ejecutar la consulta preparada y obtener el conjunto de resultados
                ResultSet dataResultSet = dataStatement.executeQuery();
            
                // Iterar sobre los resultados obtenidos
                while (dataResultSet.next()) {
                    String columnValue = dataResultSet.getString(columnName);
                    
                    // Crear un objeto TableColumn con los detalles de la columna sensible
                    TableColumn sensitiveColumn = new TableColumn(tableName, columnName, dataType, columnValue);
                    
                    // Agregar la columna sensible a la lista
                    sensitiveColumns.add(sensitiveColumn);
                }
            
                // Cerrar el conjunto de resultados de la consulta
                dataResultSet.close();
            }
            
        }

        if (sensitiveColumns.isEmpty()) {
            // No se encontraron resultados, lo que significa que no se detectaron datos sensibles en columnas de texto
            System.out.println("No se encontraron resultados. No se detectaron datos sensibles en columnas de texto.");
        } else {
            // Se encontraron resultados, lo que indica que se detectaron datos sensibles en columnas de texto
            System.out.println("Se encontraron resultados. Datos sensibles en columnas de texto detectados:");
            
            // Iterar sobre las columnas sensibles encontradas y mostrar los detalles de cada una
            for (TableColumn column : sensitiveColumns) {
                System.out.println("Tabla: " + column.getTableName());
                System.out.println("Campo: " + column.getColumnName());
                System.out.println("Tipo de dato: " + column.getDataType());
                System.out.println("Valor: " + column.getColumnValue());
                System.out.println();
            }
        }
        
        // Cerrar el conjunto de resultados y la declaración
        resultSet.close();
        statement.close();
        
    }

    // Método para verificar contraseñas almacenadas en texto plano
    private static void checkPlainTextPasswords(Connection connection) throws SQLException {
        Statement statement = connection.createStatement();
        
        // Realizar una consulta para obtener todas las filas de la tabla "users"
        ResultSet resultSet = statement.executeQuery("SELECT * FROM users");

        System.out.println("\nResultados de consulta para verificar contraseñas almacenadas en texto plano:");
        
        // Iterar sobre los resultados de la consulta
        while (resultSet.next()) {
            // Obtener el nombre de usuario y la contraseña de cada fila
            String username = resultSet.getString("username");
            String password = resultSet.getString("password");

            // Imprimir el nombre de usuario y la contraseña
            System.out.println("Usuario: " + username);
            System.out.println("Contraseña: " + password);
            System.out.println();
        }

        // Cerrar el conjunto de resultados y la declaración
        resultSet.close();
        statement.close();
    }

}
