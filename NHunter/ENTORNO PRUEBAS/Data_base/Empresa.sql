-- Creación de la base de datos
CREATE DATABASE empresa;
USE empresa;

-- Creación de la tabla "clientes"
CREATE TABLE clientes (
  id INT PRIMARY KEY,
  nombre VARCHAR(50),
  email VARCHAR(50),
  telefono VARCHAR(15)
);

-- Inserción de datos en la tabla "clientes"
INSERT INTO clientes (nombre, email, telefono) VALUES
  ('Juan Perez', 'juan@example.com', '1234567890'),
  ('Ana Lopez', 'ana@example.com', '9876543210'),
  ('Pedro Ramirez', 'pedro@example.com', '5555555555'),
  ('María Rodriguez', 'maria@example.com', '1111111111'),
  ('Carlos Gomez', 'carlos@example.com', '9999999999');

-- Creación de la tabla "empleados"
CREATE TABLE empleados (
  id INT PRIMARY KEY ,
  nombre VARCHAR(50),
  email VARCHAR(50),
  telefono VARCHAR(15),
  salario DECIMAL(10, 2)
);

-- Inserción de datos en la tabla "empleados"
INSERT INTO empleados (nombre, email, telefono, salario) VALUES
  ('Luisa Martinez', 'luisa@example.com', '2222222222', 2500.00),
  ('Javier Fernandez', 'javier@example.com', '3333333333', 3500.00),
  ('Marta Gonzalez', 'marta@example.com', '4444444444', 2800.00),
  ('Daniel Sanchez', 'daniel@example.com', '6666666666', 4000.00),
  ('Laura Torres', 'laura@example.com', '7777777777', 3200.00);

-- Creación de la tabla "productos"
CREATE TABLE productos (
  id INT PRIMARY KEY,
  nombre VARCHAR(50),
  precio DECIMAL(10, 2),
  stock INT
);

-- Inserción de datos en la tabla "productos"
INSERT INTO productos (nombre, precio, stock) VALUES
  ('Camisa', 29.99, 50),
  ('Pantalón', 49.99, 30),
  ('Zapatos', 79.99, 20),
  ('Sombrero', 14.99, 10),
  ('Bufanda', 9.99, 15);
