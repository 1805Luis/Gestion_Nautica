# Proyecto de Gestión de Reservas con Lectores de Tarjetas para un Club Nautico

## Indice
- [1. Breve descripción](#breve-descripción)
- [2. Software y material necesario](#necesario)
- [3.Estructura del proyecto](#estructura)
- [4.Funcionalidades](#funcionalidades)
- [5. Flujo](#flujo)


## 1. <a name="breve-descripción"></a> Breve descripción

Este proyecto es una aplicación gráfica para la gestión de reservas de socios, con integración a lectores de tarjetas inteligentes para autenticar a los usuarios y guardar su reserva actual. La aplicación se inicia esperando que el lector de tarjetas esté conectado y que se introduzca una tarjeta válida para poder acceder al sistema. La aplicación cuenta con dos usuarios: admin y user.

## 2. <a name="necesario"></a> Software y material necesario

Para llevar a cabo está practica hemos necesitado:
 - Software:
     - Editor de codigo(vs)
     - MySQL Workbench
 - Hardware:
     - lector ACR39U
     - SmartCard SLE5542

## 3. <a name="estructura"></a> Estructura del proyecto

- Proyecto/
    - BBDD/                                # Archivo .sql en el que esta la creación de la base de datos, tablas, usuarios y algunos datos
    - main.py                          # Archivo principal que ejecuta la aplicación
    - config.py                        # Configuración general del proyecto
    - conexion/
        - Conexion.py                  # Conexion para los usuarios normales
        -  ConexionAdmin.py            # Conexion para los usuarios administrador
    - util/
        - util_ventana.py              # Funciones para manejar la ventana
        - metodos_comunes.py           # Funciones comunes en el codigo 
        -  util_imagenes.py            # Funciones para cargar imágenes
        - demon.py                     # Funciones del demonio para comprobar el estado del lector
    - formularios/
        -  form_admin_flota.py         # Panel de administar barcos
        -  form_admin_socios.py        # Panel de administar socios
        -  form_admin.py               # Panel de administra donde se despliega admin_flota y admin_socio
        -  form_historico_reservas.py  # Panel para mostrar perfil del usuario
        - form_info_tarjeta.py         # Panel de información en la tarjeta (datos y reservas)
        -  form_info.py                # Panel de informacion
        -  form_maestro.py             # Panel principal
        -  form_perfil.py              # Panel de administrar el perfil del socio de la tarjeta actual
        - form_registro.py             # Panel para el registro del usuario
        - form_reservar.py             # Panel de reservas
    - imagenes/
        - logo.ico                     # Icono de la app
        - titulacion/                  # Imagenes de cada uno de los titulos
    - modelos/
        -  Alquiler.py                 # Modelos para gestionar los alquileres
        -  Barco.py                    # Modelos para gestionar los barcos
        -  SmartCard.py                # Modelos para gestionar tarjetas inteligentes
        -  Cliente.py                  # Modelos para gestionar clientes


## 4. <a name="funcionalidades"></a> Funcionalidades

- **Inicialización y Configuración de la Ventana:** Al iniciar la aplicación, se establece el título y el icono de la ventana, y se gestiona la conexión con el lector de tarjetas inteligentes.

- **Comprobación de Lector y Tarjeta:** La aplicación espera hasta que detecte un lector de tarjetas disponible y luego espera hasta que se inserte una tarjeta. Esto se maneja con bucles while que verifican periódicamente la presencia del lector y la tarjeta. Si no se detecta un lector o tarjeta, la interfaz presenta un mensaje de advertencia y espera una acción del usuario.

- **Manejo Multihilo con Demonio:** Un hilo demonio (threading.Thread) se inicia para realizar una comprobación constante de la tarjeta inteligente, permitiendo que la interfaz de usuario siga funcionando mientras se verifica el estado de la tarjeta.

- **Registro de Usuario:** Si no se detecta un número de socio válido o si es un usuario nuevo, se abre una ventana de registro (ventana_registro) que bloquea la interacción con la ventana principal hasta que el registro se complete.

- **Interfaz de Usuario:**  Una vez que se valida el número de socio y se valida que su cuenta esté activa, se inicializa la interfaz de usuario, configurando diversos paneles y controles:

 - **Barra Superior:** Contiene el título de la aplicación, el icono del menú lateral, un botón de cierre de sesión y una etiqueta de bienvenida que muestra el nombre del usuario  extraído de la tarjeta.

 - **Menú Lateral:** Un menú que permite la navegación entre varias secciones de la aplicación, como el perfil de usuario, reservas y administración, esta ultima estará disponible solo para los administradores del sistema. Los botones del menú cambian de estilo cuando el ratón pasa sobre ellos, mejorando la experiencia de usuario.

- **Cuerpo Principal:** El área donde se cargan los formularios correspondientes según la sección seleccionada, como el formulario de reserva, información de perfil y gestión de reservas actuales.

- **Cambio Dinámico de Secciones:** Los paneles dentro del cuerpo principal de la ventana se gestionan dinámicamente, permitiendo que el usuario navegue entre diferentes formularios de manera fluida sin tener que cerrar la aplicación.

- **Perfil del Usuario:** El sistema define y carga la foto de perfil del usuario basado en su titulación, que es obtenida desde la base de datos del sistema. Esto se hace mediante la función definirFotoPerfil, que determina qué imagen se debe mostrar en el perfil.

- **Control de Menú Lateral:** Dependiendo del rol del usuario (como "ADMIN"), el menú lateral muestra diferentes opciones. Los usuarios con permisos de administrador tienen opciones adicionales, como la administración de barcos y socios.

- **Cerrar Sesión:** El botón de cierre de sesión termina la aplicación, lo que permite a los usuarios salir de la aplicación de manera segura.


## 5. <a name="flujo"></a> Flujo
### Inicialización de la app
   - ***Usuario registrado***
       - Siendo admin<br>
            ![Inicio_Admin](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Inicio_Admin.png)
       - Siendo user<br>
            ![Inicio_User](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Inicio_User.png)
   - ***Usuario no registrado***<br>
            ![Registro](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Registro.png)
### Interacción con los paneles
   - ***Perfil***
        - Información del Usuario<br>
            ![Perfil_User](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Perfil_User.png)
        - Historial de Reservas<br>
            ![Grafica](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Perfil_Historico.png)
            <br>o también se puede observar en modo tabla<br>
            ![Tabla](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Perfil_HistoricoTablas.png)
   - ***Reservar***
        - Sin hacer reserva<br>
            ![Reservar](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Reservar.png)
        - Hecha una reserva<br>
            ![Reserva_Exito](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Reserva_Exito.)

   - ***Reserva Actual***
      - Con una reserva<br>
            ![ReservaActual_ConReserva](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/ReservaActual_ConReserva.png)
      - Sin una reserva<br>
            ![ReservaActual_SinReserva](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/ReservaActual_SinReserva.png)
   - ***Administrar***
        - Administrar flota<br>
            ![Administrar_Flota](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Administar_Flota.png)
        - Usuarios<br>
            ![Administrar_User](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Administar_User.png)
   - ***Info***<br>
            ![Info](https://github.com/1805Luis/Gestion_Nautica/blob/main/imagenes_ejecuci%C3%B3n/Info.png)


