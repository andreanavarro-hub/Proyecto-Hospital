# Proyecto Hospital
Este proyecto es un sistema interactivo de consola desarrollado en Python para la gestión de un hospital. El sistema permite administrar el ingreso y facturación de pacientes, la asignación de camas, el registro, y actualización de historias clínicas. Asi mismo, puede analizar las historias archivadas para generar un reporte sobre la tasa de ocupación de cada habitación, el promedio de días que permanecen los pacientes y el número de pacientes que son atendidos por los médicos del hospital. Estas funcionalidades son distribuidas en los tres roles de: **ADMIN**, **MEDICO** y **ENFERMERA**.

# Configuracion inicial
1. Installar python: Se recomiendo la versión 3
2. Descargar el proyecto
3. Preparar la base de datos local: Ubica los archivos estado_camas.txt y personal.txt en la misma carpeta que el script. Loa archivos se encuentran en la carpeta archivos.zip del repositorio.

# Estructura de archivos
 - El archivo: estado_camas.txt es esencial para que el programa cargue las habitaciones del hospital. Este archivo contiene el número de la habitación, tipo (A - B), número de camas, disponibilidad y el id del paciente que ocupa la cama.
- El archivo: personal.txt contiene el usuario, contraseña y rol que pueden iniciar sesión en el programa y para los cuales se desplegará un menú de funciones.
- El programa genera un carpeta llamada archivos, en la cual se archivan las historias de los pacientes facturados.
  
# Roles para inicio de sesión
| Usuario | Contraseña | Rol |
|---------|------------|-----|
|   111   | 01Andrea   | ADMIN |
|   112   | 01Mabelin  | MEDICO |
|   113   | 01Matias   | ENFERMERA |
  
# Ejemplo de Ejecución 
Ingrese su usuario: 111
Ingrese su contraseña: 01Andrea
RolIngresado: ADMIN

1: Asignar cama y crear historia
2: Verificar Alta Médica
3: Facturación
4: Crear reporte final
0: Cerrar sesión

# Herramientas utilizadas
- Python 3
- Visual Studio Code
- Módulos estándar: `os`, `datetime`
