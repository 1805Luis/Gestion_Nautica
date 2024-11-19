from smartcard.System import readers

from smartcard.util import toHexString, toBytes

class CSmartCard:
    def send_apdu(self, connection, apdu):
        response, sw1, sw2 = connection.transmit(apdu)
        print(f"Response: {toHexString(response)}, SW1: {sw1:02X}, SW2: {sw2:02X}")
        return response, sw1, sw2

    def read_card(self,inicio,NBytes):
        # Obtener la lista de lectores
        r = readers()
        print("Lectores disponibles:", r)

        # Verificar si hay lectores disponibles
        if not r:
            return 0

        try:
            # Crear una conexión con el primer lector
            connection = r[0].createConnection()
            connection.connect()

            # Definir la APDU a enviar
            select_card_apdu = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]

            # Llamar al método send_apdu
            response, sw1, sw2 = self.send_apdu(connection, select_card_apdu)

            # Verificar el estado de la respuesta
            if sw1 == 0x90 and sw2 == 0x00:

                lectura_tarjeta = [0xFF, 0xB0, 0x00] 
                inicio_cantidad =[inicio, NBytes]
                apdu_lectura = lectura_tarjeta + inicio_cantidad
                response, sw1, sw2 = self.send_apdu(connection,apdu_lectura)
                response_string = bytes(response).decode('ascii', errors='ignore')
                return response_string
            else:
                return 0
            
        except Exception as e:
            print(f"Error al leer la tarjeta: {e}")
            return 0

    def write_card(self,inicio,NBytes,contenido):
        # Obtener la lista de lectores
        r = readers()
        print("Lectores disponibles:", r)

        # Verificar si hay lectores disponibles
        if not r:
            return 0

        try:
            # Crear una conexión con el primer lector
            connection = r[0].createConnection()
            connection.connect()

            # Definir la APDU a enviar
            select_card_apdu = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]

            # Llamar al método send_apdu
            response, sw1, sw2 = self.send_apdu(connection, select_card_apdu)

            # Verificar el estado de la respuesta
            if sw1 == 0x90 and sw2 == 0x00:
                psc_apdu = [0xFF, 0x20, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF]
                response, sw1, sw2 = self.send_apdu(connection,psc_apdu)
                if sw1 == 0x90 and sw2==0x07:
                    instruccion_Escritura = [0xFF, 0xD0, 0x00]
                    inicio_Escritura = [inicio]
                    Bytes_Escritura = [NBytes]
                    write_apdu = instruccion_Escritura+inicio_Escritura+Bytes_Escritura+contenido
                    self.send_apdu(connection,write_apdu)
            else:
                return 0
            
        except Exception as e:
            print(f"Error al leer la tarjeta: {e}")
            return 0
        
    def HayLector():
        r = readers()
        print("Lectores disponibles:", r)

        # Verificar si hay lectores disponibles
        if not r:
            return 0
        else:
            return 1
    
    def HayTarjeta():
        # Obtener la lista de lectores
        r = readers()

        if not r:
            return False

        try:
            # Crear una conexión con el primer lector
            connection = r[0].createConnection()
            connection.connect()

            # Definir la APDU a enviar
            select_card_apdu = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]

            # Llamar al método send_apdu
            response, sw1, sw2 = connection.transmit(select_card_apdu)

            # Verificar el estado de la respuesta
            if sw1 == 0x90 and sw2 == 0x00:

                lectura_tarjeta = [0xFF, 0xB0, 0x00] 
                inicio_cantidad =[0x70, 0x02]
                apdu_lectura = lectura_tarjeta + inicio_cantidad
                response, sw1, sw2 = connection.transmit(apdu_lectura)
                response_string = bytes(response).decode('ascii', errors='ignore')
                if(response_string == "ID"):
                    return True
                else:
                    return False

            else:
                return False
            
        except Exception as e:
            return False

    
    
    def PrepararTarjeta(self):
        # Obtener la lista de lectores
        r = readers()
        print("Lectores disponibles:", r)

        # Verificar si hay lectores disponibles
        if not r:
            return 0

        try:
            # Crear una conexión con el primer lector
            connection = r[0].createConnection()
            connection.connect()

            # Definir la APDU a enviar
            select_card_apdu = [0xFF, 0xA4, 0x00, 0x00, 0x01, 0x06]

            # Llamar al método send_apdu
            response, sw1, sw2 = self.send_apdu(connection, select_card_apdu)

            # Verificar el estado de la respuesta
            if sw1 == 0x90 and sw2 == 0x00:
                psc_apdu = [0xFF, 0x20, 0x00, 0x00, 0x03, 0xFF, 0xFF, 0xFF]
                response, sw1, sw2 = self.send_apdu(connection,psc_apdu)
                if sw1 == 0x90 and sw2==0x07:
                    instruccion_Escritura = [0xFF, 0xD0, 0x00]
                    Bytes_Escritura = [0x10]

                    comandos = [
                        [0x20, 0x4E, 0x4F, 0x4D, 0x42, 0x52, 0x45, 0x3A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], # NOMBRE:**********
                        [0x30, 0x41, 0x50, 0x45, 0x4C, 0x4C, 0x49, 0x44, 0x4F, 0x20, 0x31, 0x3A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], #APELLIDO 1:**********
                        [0x40, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], #**********
                        [0x50, 0x41, 0x50, 0x45, 0x4C, 0x4C, 0x49, 0x44, 0x4F, 0x20, 0x32, 0x3A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], #APELLIDO 2:**********
                        [0x60, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], ##**********
                        [0x70, 0x49, 0x44, 0x3A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], #ID:**********
                        [0x80, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D,0x2D], #--------------
                        [0x90, 0x4D, 0x4D, 0x53, 0x49, 0x3A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], #MMSI:**********
                        [0xA0, 0x5A, 0x4F, 0x4E, 0x41, 0x3A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], #TITULACION:*****
                        [0xB0, 0x49, 0x44, 0x2D, 0x52, 0x45, 0x53, 0x45, 0x52, 0x56, 0x41, 0x3A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A], #ID-RESERVA:*****
                        [0xC0, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D, 0x2D,0x2D], #--------------
                        [0xD0, 0x46, 0x45, 0x43, 0x48, 0x41, 0x20, 0x41, 0x4C, 0x51, 0x55, 0x49, 0x4C, 0x45, 0x52, 0x3A,0x2A], #*FECHA ALQUILER*
                        [0xE0, 0x49, 0x4E, 0x49, 0x43, 0x49, 0x4F, 0x3A, 0x2A, 0x2A, 0x2F, 0x2A, 0x2A, 0x2F, 0x2A, 0x2A,0x2A], #INICIO:**/**/***
                        [0xF0, 0x46, 0x49, 0x4E, 0x3A, 0x2A, 0x2A, 0x2F, 0x2A, 0x2A, 0x2F, 0x2A, 0x2A, 0x2A, 0x2A, 0x2A,0x2A]  #FIN:**/**/******
                    ]

                    for comando in comandos:
                        inicio_escritura = [comando[0]] 
                        contenido = comando[1:] 
                        write_apdu = instruccion_Escritura+inicio_escritura+Bytes_Escritura+contenido
                        self.send_apdu(connection,write_apdu)
            else:
                return 0
            
        except Exception as e:
            print(f"Error al leer la tarjeta: {e}")
            return 0


