DROP DATABASE IF EXISTS ServicentroCorazonDB;
GO

CREATE DATABASE ServicentroCorazonDB;
GO

USE ServicentroCorazonDB;
GO

-- CREACION DE TABLAS
CREATE TABLE Empleados (
    empleado_id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    email NVARCHAR(100) UNIQUE,
    telefono NVARCHAR(15),
    direccion NVARCHAR(255),
    fecha_contratacion DATE,
    rol NVARCHAR(50) CHECK (rol IN ('Administrador', 'Gerente', 'Empleado', 'Tecnico', 'Mantenimiento')),
    estatus NVARCHAR(10) DEFAULT 'Activo' CHECK (estatus IN ('Activo', 'Inactivo'))
);

CREATE TABLE Inventarios (
    producto_id INT PRIMARY KEY IDENTITY(1,1),
    nombre_producto NVARCHAR(100),
    tipo NVARCHAR(50) CHECK (tipo IN ('Combustible', 'Producto de Tienda')),
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10, 2),
    fecha_ultima_actualizacion DATETIME DEFAULT GETDATE()
);

CREATE TABLE Ventas (
    venta_id INT PRIMARY KEY IDENTITY(1,1),
    empleado_id INT,
    total DECIMAL(10, 2),
    fecha_venta DATETIME DEFAULT GETDATE()
);

CREATE TABLE Detalle_Venta (
    detalle_id INT PRIMARY KEY IDENTITY(1,1),
    venta_id INT,
    producto_id INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2)
);

CREATE TABLE Devoluciones (
    devolucion_id INT PRIMARY KEY IDENTITY(1,1),
    venta_id INT,
    producto_id INT,
    cantidad INT,
    fecha_devolucion DATETIME DEFAULT GETDATE()
);

CREATE TABLE Mantenimiento (
    mantenimiento_id INT PRIMARY KEY IDENTITY(1,1),
    equipo NVARCHAR(100),
    fecha_programada DATE,
    fecha_realizacion DATE,
    estado NVARCHAR(20) CHECK (estado IN ('Pendiente', 'Completado'))
);

CREATE TABLE Reabastecimiento_Gasolina (
    reabastecimiento_id INT PRIMARY KEY IDENTITY(1,1),
    cantidad DECIMAL(10, 2),
    fecha_solicitud DATETIME DEFAULT GETDATE(),
    fecha_entrega DATE
);

CREATE TABLE Servicios_Adicionales (
    servicio_id INT PRIMARY KEY IDENTITY(1,1),
    tipo_servicio NVARCHAR(50) CHECK (tipo_servicio IN ('Lubricentro', 'Llantera')),
    descripcion NVARCHAR(MAX),
    fecha_servicio DATE,
    empleado_id INT
);

CREATE TABLE Reportes (
    reporte_id INT PRIMARY KEY IDENTITY(1,1),
    tipo_reporte NVARCHAR(100),
    fecha_generacion DATETIME DEFAULT GETDATE(),
    contenido NVARCHAR(MAX)
);

-- CREACION DE CLAVES FORANEAS
ALTER TABLE Ventas
ADD FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id);

ALTER TABLE Detalle_Venta
ADD FOREIGN KEY (venta_id) REFERENCES Ventas(venta_id),
    FOREIGN KEY (producto_id) REFERENCES Inventarios(producto_id);

ALTER TABLE Devoluciones
ADD FOREIGN KEY (venta_id) REFERENCES Ventas(venta_id),
    FOREIGN KEY (producto_id) REFERENCES Inventarios(producto_id);

ALTER TABLE Servicios_Adicionales
ADD FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id);

ALTER TABLE Reabastecimiento_Gasolina
ADD producto_id INT,
	FOREIGN KEY (producto_id) REFERENCES Inventarios(producto_id);

ALTER TABLE Reportes
ADD venta_id INT,
	FOREIGN KEY (venta_id) REFERENCES Ventas(venta_id);

ALTER TABLE Mantenimiento
ADD empleado_id INT,
	FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id);