
import mysql.connector  # mysql-connector-python

class CConexion:

    def ConexionBaseDeDatos():
        try:
            conexion = mysql.connector.connect(user='user',
                                              password='464|hL|C{r:S',
                                              host='127.0.0.1',
                                              database='PuertoNautico',
                                              port='3306')
            print("Conexion correcta")
            return conexion
        
        except mysql.connector.Error as error:
            print("Error de conexion {}".format(error))
            return conexion
        