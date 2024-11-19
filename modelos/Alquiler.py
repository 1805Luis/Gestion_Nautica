from conexion.Conexion import *

class CAlquiler:
    
    def mostrarHistorico(Id,anio):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "SELECT MONTH(A.fecha_inicio) AS mes, COUNT(*) AS num_alquileres FROM Alquileres A WHERE A.n_socio = %s AND YEAR(A.fecha_inicio) = %s GROUP BY mes ORDER BY mes;"
            cursor.execute(query, (Id,anio))
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    def actualizarReserva(Id,inicio,fin):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "UPDATE Alquileres SET fecha_inicio = %s, fecha_fin = %s WHERE id = %s;"
            cursor.execute(query, (inicio,fin,Id))
            cone.commit()
            cone.close()

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    def eliminarAlquiler(id):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "Delete from Alquileres WHERE id = %s;"
            cursor.execute(query, (id))
            cone.commit()
            cone.close()

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))

    def mostrarTodos(id):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "select  B.MMSI, B.tipo_barco, A.fecha_inicio,A.fecha_fin from alquileres as A INNER JOIN barcos as B ON A.MMSI = B.MMSI where A.n_socio = %s"
            cursor.execute(query, (id,))
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))