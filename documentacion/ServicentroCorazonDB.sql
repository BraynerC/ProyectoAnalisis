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

CREATE TABLE Usuarios (
    usuario_id INT PRIMARY KEY IDENTITY(1,1),
    nombre_usuario NVARCHAR(50) UNIQUE NOT NULL,
    contrasena NVARCHAR(255) NOT NULL, 
    empleado_id INT NULL, 
    rol NVARCHAR(50) DEFAULT 'Cliente',
    fecha_creacion DATETIME DEFAULT GETDATE(),
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

CREATE TABLE Proveedores (
    id INT IDENTITY(1,1) PRIMARY KEY,      
    nombre_proveedor NVARCHAR(100) NOT NULL, 
    contacto NVARCHAR(100) NOT NULL,         
    telefono NVARCHAR(15) NOT NULL,          
    email NVARCHAR(100) NOT NULL              
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
    fecha_devolucion DATETIME DEFAULT GETDATE(),
    motivo NVARCHAR(255),
    fecha_fin DATETIME
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
    fecha_entrega DATE,
    producto_id INT
);

CREATE TABLE Servicios_Adicionales (
    servicio_id INT PRIMARY KEY IDENTITY(1,1),
    tipo_servicio NVARCHAR(50) CHECK (tipo_servicio IN ('Lubricentro', 'Llantera')),
    descripcion NVARCHAR(MAX),
    fecha_servicio DATE,
    empleado_id INT,
    cliente_id INT
);

CREATE TABLE Reportes (
    reporte_id INT PRIMARY KEY IDENTITY(1,1),
    tipo_reporte NVARCHAR(100),
    fecha_generacion DATETIME DEFAULT GETDATE(),
    contenido NVARCHAR(MAX),
    usuario_id INT
);

CREATE TABLE Promociones (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100) NOT NULL,
    detalles NVARCHAR(MAX),
    fecha_creacion DATETIME DEFAULT GETDATE(),
    descuento DECIMAL(5, 2), 
    fecha_inicio DATETIME, 
    fecha_fin DATETIME,
    producto_id INT
);

CREATE TABLE Parametros_Mantenimiento (
    id INT PRIMARY KEY IDENTITY(1,1),
    pressure_limit DECIMAL(10, 2) NOT NULL,
    temperature_limit DECIMAL(10, 2) NOT NULL,
    fuel_level_limit DECIMAL(10, 2) NOT NULL,
    fecha_actualizacion DATETIME DEFAULT GETDATE()
);

-- CREACION DE TABLA CLIENTES
CREATE TABLE Clientes (
    cliente_id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100),
    telefono NVARCHAR(15),
    email NVARCHAR(100)
);

-- CREACION DE TABLA CITAS
CREATE TABLE Citas (
    cita_id INT PRIMARY KEY IDENTITY(1,1),
    tipo_servicio VARCHAR(50),
    descripcion TEXT,
    fecha_servicio DATETIME,
    estado VARCHAR(50) DEFAULT 'Pendiente',
    cliente_nombre VARCHAR(100),
    cliente_telefono VARCHAR(20),
    cliente_email VARCHAR(100)
);

CREATE TABLE gasolina (
    gasolina_id INT PRIMARY KEY IDENTITY(1,1),
    tipo VARCHAR(50), 
    cantidad_litros FLOAT,
    minimo_litros FLOAT 
);

INSERT INTO gasolina (tipo, cantidad_litros, minimo_litros)
VALUES 
    ('Gasolina Super', 5000, 1000),
    ('Gasolina Regular', 7000, 1500), 
    ('Diesel', 10000, 2000); 

CREATE TABLE reabastecimiento (
    reabastecimiento_id INT PRIMARY KEY IDENTITY(1,1),
    gasolina_id INT FOREIGN KEY REFERENCES gasolina(gasolina_id),
    cantidad FLOAT,
    fecha_solicitud DATETIME,
    fecha_entrega DATETIME
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
ADD FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id),
    FOREIGN KEY (cliente_id) REFERENCES Clientes(cliente_id);

ALTER TABLE Reabastecimiento_Gasolina
ADD FOREIGN KEY (producto_id) REFERENCES Inventarios(producto_id);

ALTER TABLE Reportes
ADD CONSTRAINT FK_UsuarioID
FOREIGN KEY (usuario_id) REFERENCES Usuarios(usuario_id);

ALTER TABLE Usuarios
ADD CONSTRAINT FK_EmpleadoID
FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id);

ALTER TABLE Promociones
ADD FOREIGN KEY (producto_id) REFERENCES Inventarios(producto_id);

ALTER TABLE Inventarios
ADD marca NVARCHAR(100);

ALTER TABLE Proveedores
ADD marca_id INT,
    FOREIGN KEY (marca_id) REFERENCES Inventarios(producto_id);

