-- Crear base de datos
CREATE DATABASE PuertoNautico
DEFAULT CHARACTER SET 'utf8mb4'
COLLATE utf8mb4_unicode_ci;

USE PuertoNautico;

-- Tabla Barcos
CREATE TABLE Barcos (
    MMSI INT PRIMARY KEY NOT NULL,
    tipo_barco VARCHAR(50),
    titulo_requerido VARCHAR(50),
    zona_navegacion INT,
    eslora FLOAT,
    tripulacion INT,
    pantalan VARCHAR(1),
    amarre INT,
    estado VARCHAR(30)
);

CREATE TABLE NivelesTitulo (
    titulo_barco VARCHAR(3),
    nivel INT
);

-- Tabla Clientes
CREATE TABLE Clientes (
    n_socio INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nombre VARCHAR(50),
    apellido1 VARCHAR(50),
    apellido2 VARCHAR(50),
    titulo VARCHAR(50),
    telefono VARCHAR(15),
    rol VARCHAR(20),
    estado ENUM('activa', 'suspendida') NOT NULL
);

-- Tabla Alquileres
CREATE TABLE Alquileres (
	id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    MMSI INT,
    n_socio INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    FOREIGN KEY (MMSI) 
		REFERENCES Barcos(MMSI)
		ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (n_socio) 
		REFERENCES Clientes(n_socio)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- Insertar datos en la tabla Barcos
INSERT INTO Barcos (MMSI, tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado) VALUES
(101, 'Velero', 'LN', 6, 5.0, 4, 'A', 1, 'Disponible'),
(102, 'Yate', 'PER', 4, 14.5, 8, 'B', 5 , 'Disponible'),
(103, 'Catamarán', 'PY', 2, 20.0, 12, 'C', 10 , 'En revisión'),
(104, 'Lancha', 'PNB', 5, 7.5, 6, 'A', 3, 'Disponible'),
(105, 'Velero', 'CY', 1, 24.0, 10, 'D', 2 , 'Disponible');

INSERT INTO NivelesTitulo (titulo_barco, nivel) VALUES
('LN', 1),
('PNB', 2),
('PER', 3),
('PY', 4),
('CY', 5);

-- Insertar datos en la tabla Clientes
INSERT INTO Clientes (n_socio, nombre, apellido1, apellido2, titulo, telefono,rol,estado) VALUES
(1, 'Ana', 'Pérez', 'García', 'PY', '123456789',"user","activa"),
(2, 'Juan', 'Rodríguez', 'Torres', 'PER', '987654321',"admin","activa"),
(3, 'Luis', 'López', 'Sánchez', 'LN', '555123456',"user","activa");

-- Insertar datos en la tabla Alquileres
INSERT INTO Alquileres (MMSI, n_socio, fecha_inicio, fecha_fin) VALUES
(101, 3, '2024-09-01', '2024-09-03'),
(102, 2, '2024-10-20', '2024-10-30'),
(103, 1, '2024-08-18', '2024-10-25'),
(104, 3, '2024-09-05', '2024-09-07'),
(105, 2, '2024-09-01', '2024-09-10'),
(101, 2, '2024-05-11', '2024-05-05'),
(102, 2, '2024-09-10', '2024-09-15'),  
(104, 2, '2024-10-01', '2024-10-05'),  
(105, 2, '2024-09-20', '2024-09-25'); 


-- Crear una vista--
CREATE VIEW VistaClientes AS
SELECT n_socio, rol, estado
FROM PuertoNautico.Clientes;


-- Crear el usuario con una contraseña y permisos para acceder desde cualquier máquina
CREATE USER 'admin'@'%' IDENTIFIED BY 'F35,}KYywT1x';

-- Conceder permisos de SELECT, DELETE,UPDATE,INSERT en la tabla Barcos
GRANT SELECT, DELETE, UPDATE,INSERT ON PuertoNautico.Barcos TO 'admin'@'%';


GRANT SELECT, UPDATE, DELETE ON VistaClientes TO 'admin'@'%';

-- Conceder permisos de UPDATE y DELETE en la tabla Clientes
GRANT SELECT, DELETE, UPDATE ON PuertoNautico.Clientes TO 'admin'@'%';


-- Crear el usuario con una contraseña y permisos para acceder desde cualquier máquina
CREATE USER 'user'@'%' IDENTIFIED BY '464|hL|C{r:S';

-- Conceder permisos de SELECT, DELETE,UPDATE,INSERT en la tabla Barcos
GRANT SELECT, DELETE, UPDATE,INSERT ON PuertoNautico.Clientes TO 'user'@'%';
GRANT SELECT ON PuertoNautico.Barcos TO 'user'@'%';
GRANT SELECT ON PuertoNautico.nivelestitulo TO 'user'@'%';

GRANT SELECT, DELETE, UPDATE,INSERT ON PuertoNautico.alquileres TO 'user'@'%';

-- Aplicar los cambios
FLUSH PRIVILEGES; 

