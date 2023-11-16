package Auditar_BD_SQL;

// Clase para representar una columna de una tabla en la base de datos
class TableColumn {
    private String tableName;    // Nombre de la tabla
    private String columnName;   // Nombre de la columna
    private String dataType;     // Tipo de dato de la columna
    private String columnValue;  // Valor de la columna

    // Constructor de la clase
    public TableColumn(String tableName, String columnName, String dataType, String columnValue) {
        this.tableName = tableName;
        this.columnName = columnName;
        this.dataType = dataType;
        this.columnValue = columnValue;
    }

    // Métodos para acceder a los atributos de la columna
    public String getTableName() {
        return tableName;
    }

    public String getColumnName() {
        return columnName;
    }

    public String getDataType() {
        return dataType;
    }

    public String getColumnValue() {
        return columnValue;
    }
}
