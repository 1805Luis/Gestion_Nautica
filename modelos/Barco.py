from conexion.Conexion import *
from conexion.ConexionAdmin import *

class CBarcos:
   
    def mostrarBarcos(estado,Titulo):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            if( estado.lower() == "todos"):
                cursor.execute("select * from barcos")
            else:
                query = "SELECT B.MMSI, B.tipo_barco, B.titulo_requerido, B.zona_navegacion, B.eslora, B.tripulacion, B.pantalan, B.amarre FROM Barcos B JOIN NivelesTitulo NL ON B.titulo_requerido = NL.titulo_barco JOIN NivelesTitulo NL_Titulo ON NL_Titulo.titulo_barco = %s WHERE NL.nivel <= NL_Titulo.nivel AND B.estado != 'En revisión';"
                cursor.execute(query, (Titulo,))
                
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    

    def estaAlquilado(MMSI,inicio,fin,idReserva):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            if(idReserva == 0):
                query = "SELECT * FROM Alquileres WHERE MMSI = %s AND ((fecha_inicio <= %s AND fecha_fin >= %s) OR (fecha_inicio <= %s AND fecha_fin >= %s));"
                cursor.execute(query, (MMSI,inicio,fin,fin,inicio))
            else:
                query = "SELECT * FROM Alquileres WHERE MMSI = %s AND ((fecha_inicio <= %s AND fecha_fin >= %s) OR (fecha_inicio <= %s AND fecha_fin >= %s))and id != %s;"
                cursor.execute(query, (MMSI,inicio,fin,fin,inicio,idReserva))
                
            miResultado = cursor.fetchall()
            
            cantidad_filas = len(miResultado)  # Contar la cantidad de filas obtenidas
            cone.commit()
            cone.close()
            return cantidad_filas

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    def CrearAlquiler(MMSI, n_socio, fecha_inicio, fecha_fin):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "INSERT INTO Alquileres (MMSI, n_socio, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s);"
            cursor.execute(query, (MMSI, n_socio, fecha_inicio, fecha_fin))
            cone.commit()
            nuevo_id = cursor.lastrowid # Obtener el ID del nuevo registro
            cone.close()
            
            return nuevo_id  # Retorna el nuevo ID
            

        except mysql.connector.Error as error:
            print("Error de mostrar datos {}".format(error))
    
    #Funciones de admin
    
    def CrearBarco(MMSI, tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado):
        try:
            cone = CConexionAdmin.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "INSERT INTO Barcos (MMSI, tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s);"
            cursor.execute(query, (MMSI, tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado))
            cone.commit()
            cone.close()            

        except mysql.connector.Error as error:
            print("Error de inseccion de datos {}".format(error))

    def ModificarBarco(MMSI, tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado):
        try:
            cone = CConexionAdmin.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "UPDATE Barcos SET tipo_barco = %s,titulo_requerido = %s, zona_navegacion = %s, eslora = %s, tripulacion = %s, pantalan = %s, amarre = %s,estado = %s WHERE MMSI = %s;"
            cursor.execute(query, (tipo_barco, titulo_requerido, zona_navegacion, eslora, tripulacion, pantalan, amarre, estado,MMSI))
            cone.commit()
            cone.close()            

        except mysql.connector.Error as error:
            print("Error de inseccion de datos {}".format(error))
    
    def EliminarBarco(MMSI):
        try:
            cone = CConexionAdmin.ConexionBaseDeDatos()
            cursor = cone.cursor()
            query = "DELETE FROM Barcos WHERE MMSI = %s;"
            cursor.execute(query, (MMSI,))
            cone.commit()
            cone.close()            

        except mysql.connector.Error as error:
            print("Error de inseccion de datos {}".format(error))