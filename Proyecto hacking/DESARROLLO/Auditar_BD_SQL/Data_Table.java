package Auditar_BD_SQL;

class TableColumn {
    private String tableName;
    private String columnName;
    private String dataType;
    private String columnValue;

    public TableColumn(String tableName, String columnName, String dataType, String columnValue) {
        this.tableName = tableName;
        this.columnName = columnName;
        this.dataType = dataType;
        this.columnValue = columnValue;
    }

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