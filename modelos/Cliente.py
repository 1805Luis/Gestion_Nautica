from conexion.Conexion import *
from conexion.ConexionAdmin import *

class CClientes:

    def existeSocio(nSocio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "select * from Clientes where n_socio = %s;"
            cursor.execute(query, (nSocio,))
            miResultado = cursor.fetchall()
            cantidad_filas = len(miResultado)
            cone.close()
            return cantidad_filas == 1

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    def rolSocio(nSocio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "select rol from Clientes where n_socio = %s;"
            cursor.execute(query, (nSocio,))
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado[0][0].upper()

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))

    def estadoCuenta(nSocio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "SELECT estado FROM Clientes where n_socio = %s;"
            cursor.execute(query, (nSocio,))
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            estado = miResultado[0][0].upper()
            return estado == "ACTIVA"

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))

    def mostrarTitulacionSocio(nSocio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "select titulo from Clientes where n_socio = %s;"
            cursor.execute(query, (nSocio,))
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    def mostrarUsuario(nSocio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "select n_socio, nombre, apellido1, apellido2, titulo, telefono from Clientes where n_socio = %s;"
            cursor.execute(query, (nSocio,))
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))

    def ingresarClientes(nombre, apellido1, apellido2, titulo, telefono):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = "INSERT INTO Clientes (nombre, apellido1, apellido2, titulo, telefono, rol) VALUES (%s, %s, %s, %s, %s, %s);"
            valores = (nombre, apellido1, apellido2, titulo, telefono, "user")
            
            # Ejecutar la inserción
            cursor.execute(sql, valores)
            cone.commit()

            # Obtener el ID del nuevo registro
            nuevo_id = cursor.lastrowid

            cone.close()
            return nuevo_id  # Retorna el nuevo ID

        except mysql.connector.Error as error:
            print("Error de ingreso de datos {}".format(error))
            return None  # Retorna None en caso de error
        
    def editarUsuario(nombre,apellido1,apellido2,titulo,telefono,nSocio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "UPDATE Clientes SET nombre = %s,   apellido1 = %s,   apellido2 = %s,  titulo = %s,  telefono = %s WHERE n_socio = %s;"
            cursor.execute(query, (nombre,apellido1,apellido2,titulo,telefono,nSocio))
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    def eliminarUsuario(nSocio): 
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "DELETE FROM Clientes WHERE n_socio = %s;"
            cursor.execute(query, (nSocio,))
            cone.commit()
            cone.close()

        except mysql.connector.Error as error:
            print("Error al eliminar los datos {}".format(error))

    # Funciones de admin

    def mostrarTodosSocios():
        try:
            cone = CConexionAdmin.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "select * from VistaClientes;"
            cursor.execute(query)
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    def actualizarRolCuenta(nSocio,rol,cuenta):
        try:
            cone = CConexionAdmin.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "update Clientes SET rol = %s,   estado = %s WHERE n_socio = %s;"
            cursor.execute(query,(rol,cuenta,nSocio))
            miResultado = cursor.fetchall()
            print(miResultado)
            cone.commit()
            cone.close()
            return miResultado
        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))

    