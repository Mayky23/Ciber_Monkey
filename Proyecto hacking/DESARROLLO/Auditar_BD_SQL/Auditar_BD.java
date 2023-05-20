package Auditar_BD_SQL;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Auditar_BD {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Ingrese la ruta de la conexión de la base de datos: ");
        String databaseUrl = scanner.nextLine();
        
        System.out.print("Ingrese el nombre de usuario de la base de datos: ");
        String username = scanner.nextLine();

        System.out.print("Ingrese la contraseña de la base de datos: ");
        String password = scanner.nextLine();

        try (Connection connection = DriverManager.getConnection(databaseUrl, username, password)) {
            // Resto del código para auditar la base de datos
            checkUserPermissions(connection);
            analyzeSecurityConfigurations(connection);
            checkSQLInjectionVulnerabilities(connection);
            findInsecureData(connection);
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    private static void checkUserPermissions(Connection connection) throws SQLException {
        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("SHOW GRANTS FOR CURRENT_USER");

        System.out.println("Permisos y roles de usuario:");
        while (resultSet.next()) {
            String grant = resultSet.getString(1);
            System.out.println(grant);
        }
        resultSet.close();
        statement.close();
    }

    private static void analyzeSecurityConfigurations(Connection connection) throws SQLException {
        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("SELECT @@GLOBAL.sql_mode, @@SESSION.sql_mode");

        System.out.println("\nConfiguraciones de seguridad:");
        if (resultSet.next()) {
            String globalSqlMode = resultSet.getString(1);
            String sessionSqlMode = resultSet.getString(2);
            System.out.println("Modo SQL global: " + globalSqlMode);
            System.out.println("Modo SQL de la sesión: " + sessionSqlMode);
        }
        resultSet.close();
        statement.close();
    }

    private static void checkSQLInjectionVulnerabilities(Connection connection) throws SQLException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese el nombre de usuario para verificar inyección de SQL: ");
        String username = scanner.nextLine();

        System.out.print("Ingrese la contraseña para verificar inyección de SQL: ");
        String password = scanner.nextLine();

        String sqlQuery = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'";
        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery(sqlQuery);

        System.out.println("\nResultados de consulta para verificar inyección de SQL:");
        if (resultSet.next()) {
            System.out.println("Se encontraron resultados. Vulnerabilidad de inyección de SQL detectada.");
        } else {
            System.out.println("No se encontraron resultados. No se detectaron vulnerabilidades de inyección de SQL.");
        }
        resultSet.close();
        statement.close();
    }

    private static void findInsecureData(Connection connection) throws SQLException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Ingrese el patrón de datos sensibles para buscar: ");
        String sensitiveDataPattern = scanner.nextLine();

        List<TableColumn> insecureColumns = new ArrayList<>();

        Statement statement = connection.createStatement();
        ResultSet resultSet = statement.executeQuery("SELECT * FROM information_schema.columns");

        System.out.println("\nResultados de consulta para identificar datos sensibles almacenados de manera insegura:");
        ResultSetMetaData metaData = resultSet.getMetaData();
        while (resultSet.next()) {
            String tableName = resultSet.getString("TABLE_NAME");
            String columnName = resultSet.getString("COLUMN_NAME");
            String dataType = resultSet.getString("DATA_TYPE");

            String sqlQuery = "SELECT * FROM " + tableName + " WHERE " + columnName + " LIKE '%" + sensitiveDataPattern + "%'";
            Statement dataStatement = connection.createStatement();
            ResultSet dataResultSet = dataStatement.executeQuery(sqlQuery);

            while (dataResultSet.next()) {
                String columnValue = dataResultSet.getString(columnName);
                TableColumn insecureColumn = new TableColumn(tableName, columnName, dataType, columnValue);
                insecureColumns.add(insecureColumn);
            }

            dataResultSet.close();
            dataStatement.close();
        }

        if (insecureColumns.isEmpty()) {
            System.out.println("No se encontraron resultados. No se detectaron datos sensibles almacenados de manera insegura.");
        } else {
            System.out.println("Se encontraron resultados. Datos sensibles almacenados de manera insegura detectados:");
            for (TableColumn column : insecureColumns) {
                System.out.println("Tabla: " + column.getTableName());
                System.out.println("Campo: " + column.getColumnName());
                System.out.println("Tipo de dato: " + column.getDataType());
                System.out.println("Valor: " + column.getColumnValue());
                System.out.println();
            }
        }

        resultSet.close();
        statement.close();
    }

    
}
