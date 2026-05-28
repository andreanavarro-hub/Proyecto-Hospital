#Apartado de importaciones
import datetime
import os
#Apartado de funciones
def login(archivo:str,usuario:str,contra:str) -> str:
    try:
        archivoAbierto = ""
        personaSeparada = ""
        accesoUsuario = 0
        accesoContra = 1
        accesoRol = 2
        rol = ""
        
        #Abrir archivo 
        archivoAbierto = open(archivo,"r")
        archivoAbierto.readline() #Leer la primera línea de ese archivo
        
        for persona in archivoAbierto:
            personaSeparada = persona.split(",")
            
            if personaSeparada[accesoUsuario] == usuario and personaSeparada[accesoContra] == contra:
                rol = personaSeparada[accesoRol].strip()
                break
        
        archivoAbierto.close() #Cerrar el archivo
        return rol
    
    except Exception as e:
        return e

def abrirArchivo() -> str: #Archivo abierto para cargar habitaciones a la matriz
    try:
        
        archivo = "estado_camas.txt"
        archivoAbierto = ""
        
        archivoAbierto = open(archivo,"r")
        
        archivoAbierto.readline() #Leer dos primeras líneas
        archivoAbierto.readline()
        
        return archivoAbierto 
        
    except Exception as e:
        return e

    
def cargarHabitaciones(archivoAbierto:str) -> list: #Carga las habitaciones a la matriz, sin importar el tipo
    try:
        
        datosHabitacion = ""
        tipoHab = ""
        cama = ""
        camas = []
        numCama = ""
        estado = ""
        cargarCama = {}
        idPaciente = ""
        cargarHab = ""
        habitaciones = []
        
        for habitacion in archivoAbierto:
            
            datosHabitacion = habitacion.split(",")
            
            if len(datosHabitacion) < 3:
                continue
            
            numero = datosHabitacion[0].strip()
            tipoHab = datosHabitacion[1].strip()
            numCama = datosHabitacion[2].split("|") #División para acceder al número de camas
    
            #1 - disponible - N/A | 2 - disponible - N/A
            for i in range(len(numCama)):  #DATOS DE CADA CAMA
                
                cama = numCama[i].split("-") 
                estado = cama[1].strip().lower()
                idPaciente = cama[2].strip()
                
                cargarCama = {
                    "cama" : int(i+1),
                    "estado": estado, 
                    "IDpaciente":idPaciente
                }
                
                camas.append(cargarCama)
                cargarCama = {} #No olvidar reiniciar 1: Diccionario de cada cama, 2: Listado de camas, 3: La información de habitación 
                
            cargarHab = {
                "habitacion" : int(numero),
                "tipo" : tipoHab,
                "camas" : camas
            }
            camas = []
            
            habitaciones.append(cargarHab)
            cargarHab = {}
             
        archivoAbierto.close()
        
        if len(habitaciones) < 30:
            raise Exception("Las habitaciones no se cargaron de forma adecuada.")
        
        return habitaciones
    except Exception as e:
        return e 
    
def identificarCamaDisponible(habitaciones:list) -> int|int: #Devuelve índice de hab y cama en matriz
    try:
        habitacion = ""
        habEncontrada = False
        camas = []
        accesoEstado = "estado"
        disponible = "disponible"
        accesoCamas = "camas"
        indiceHab = -1
        indiceCama = -1
        
        for i in range(len(habitaciones)):
            habitacion = habitaciones[i]
            
            if habEncontrada:
                break
            
            camas = habitacion[accesoCamas]
            for j in range(len(camas)): 
                if camas[j][accesoEstado] == disponible:
                    habEncontrada = True
                    indiceHab = i
                    indiceCama = j
                    break
      
        return indiceHab,indiceCama 
    except Exception as e:
        return e

def asignarCama(diccionario:list,indiceHab:int,indiceCama:int,idpaciente:str) -> str: #Mensaje de la asignación al paciente
    try:
        habitacion = ""
        cama = ""
        tipoHab = ""
        asignacion = ""
        accesoTipo = "tipo"
        accesoCamas = "camas"
        accesoNumCama = "cama"
        accesoNumero = "habitacion"
        
        habitacion = diccionario[indiceHab][accesoNumero]
        tipoHab = diccionario[indiceHab][accesoTipo]
        cama = diccionario[indiceHab][accesoCamas][indiceCama][accesoNumCama]
        
        asignacion = f"\nPaciente{idpaciente}\nAsignado(a) a la habitación:{habitacion}- {tipoHab}\ncama:{cama}\n"
        
        return asignacion
    except Exception as e:
        return e
 
#Actualizar la nueva cama ocupada en el archivo:
def actualizarArchivo(archivo:str,habAocupar:int,camaOcupada:int,idPaciente:str) -> str: #Actualizará el archivo con cama ocupada por paciente
    try:
        habitacion = ""
        idVacio = "N/A"
        ocupado = "ocupado"
        buscarCama = ""
        lineaActualizada = ""
        ajuste = ""
       
        #Abrir archivo y cargar en memoria
        abrirArchivo = open(archivo,"r")
        contenidoArchivo = abrirArchivo.readlines()
        abrirArchivo.close()
        
        for i in range(len(contenidoArchivo)):
            
            linea = contenidoArchivo[i]
            habitacion = f"{habAocupar},"
            
            if linea.find(habitacion) == 0:#Si es la misma habitación y línea
    
                buscarCama = linea.find(f"{camaOcupada}",2)
                
                if habAocupar < 11: #Hab tipo A
                    limite = linea.find(idVacio,buscarCama + 1)
                    lineaActualizada = f"1 - {ocupado} - {idPaciente}"
     
                elif habAocupar >= 11 : #Hab tip B
                    if camaOcupada == 1:
                        limite =  linea.find(idVacio, buscarCama + 1)
                        lineaActualizada = f"1 - {ocupado} - {idPaciente}"
                    elif camaOcupada == 2:
                        limite = linea.find(idVacio, buscarCama + 1)
                        lineaActualizada = f"2 - {ocupado} - {idPaciente}"
                
                ajuste = linea[buscarCama:limite].replace(linea[buscarCama:limite],lineaActualizada)
                contenidoArchivo[i] = linea[:buscarCama] + ajuste + linea[limite + len(idVacio):]
            
            else:
                continue
            
            #Abrir archivo y reescribir
            abrirArchivo = open(archivo,"w")
            abrirArchivo.writelines(contenidoArchivo)
            abrirArchivo.close()
            return f"Habitación {habAocupar} archivo actualizado"
    except Exception as e:
        return e
     
def crearHistoriaPaciente(idPaciente:str) -> str: #Devuelve archivo creado
    try:
        
        nombreArchivo = f"historia_{idPaciente}.txt"
        historiapaciente = open(nombreArchivo,"x")
       
        historiapaciente.close()
        return nombreArchivo
        
    except Exception as e:
        return e
    
def verificarAltaMedica(idPaciente:str):
    try:
        
        abrirArchivo = ""
        contenidoArchivo = ""
        altaMedica = "ALTA MEDICA"
        aprobacion = False
         
        archivo = f"historia_{idPaciente}.txt"
        abrirArchivo = open(archivo,"r")
        contenidoArchivo = abrirArchivo.read()
       
        if contenidoArchivo.find(altaMedica) != -1:
            aprobacion = not(aprobacion)
        
        abrirArchivo.close()
        
        return aprobacion
        
    except Exception as e:
        return e

def factura(dias:int,costoCama:int,idPaciente) -> str: # Devolverá solo el nombre del archivo
    try:
        total = 0
        resultado = ""
        archivoNombre = ""
        archivoCreado = ""
        archivoNombre = f"factura_paciente{idPaciente}.txt"
        
        total = costoCama * dias
        resultado += f"\nPaciente: {idPaciente}\nCosto cama: {costoCama}\nPermanencia(Días): {dias}"
        resultado += f"\nValor Total A Pagar: {total}\n"
        resultado += "*" * 10
        #Crear archivo de factura
        archivoCreado = open(archivoNombre,"w")
        archivoCreado.write(resultado)
        archivoCreado.close()
    
        return archivoNombre
    
    except Exception as e:
        return e
    
# Una vez se crea el archivo: 
def agregarDetalleshistoria(mensajeAsignacion:str,idPaciente:str) -> str: #Agrega la cama del paciente a su historia 
    try:
        nombreArchivo = ""
        archivoAbierto = ""
        resultado = ""
        nombreArchivo = f"historia_{idPaciente}.txt"
        
        archivoAbierto = open(nombreArchivo,"a")
        archivoAbierto.write(mensajeAsignacion)
        archivoAbierto.close()
        resultado = f"\nLa habitación asignada al paciente {idPaciente} ha sido agregado con éxito\n"
        
        return resultado
        
    except Exception as e:
        return e
    
def consultarHistoria(paciente: str) -> str: #Consultar historia clínica del paciente por medio de su id.
    try:
        #APARTADO DE VARIABLES
        archivo = ""
        mensaje = ""
        contenido = ""

        archivo = f"historia_{paciente}.txt"

        mensaje += "\n"+"-" * 10 + f"\n# Historia clínica del paciente {paciente}\n"
        
        
        if not os.path.exists(archivo):
            raise Exception(f"No existe una historia clínica para el paciente {paciente}")

        with open(archivo, "r" ) as file:
            contenido = file.read().strip()

        if contenido == "":
            mensaje += "La historia clínica está vacía."
        else:
            for linea in contenido.splitlines():
                mensaje += f"• {linea}\n"

        mensaje +=  "-" * 10 + "\n"

        return mensaje
    except Exception as e:
        return e
     
#Después de la facturación:    1: Liberar cama en la matriz 
def liberarCamaEnMatriz(habitaciones:list,indiceHab:str,indiceCama:int) -> list|str: #Retorna dos valores 1: la lista actualizada y la actualización concreta (Mensaje)
    try:
        accesoPaciente = "IDpaciente"
        disponible = "disponible"
        accesoHab = "habitacion"
        accesoEstado = "estado"
        accesoCamas = "camas"
        accesoCama = "cama"
        idVacio = "N/A"
        actualizacion = ""
        
        habitaciones[indiceHab][accesoCamas][indiceCama][accesoEstado] = disponible
        habitaciones[indiceHab][accesoCamas][indiceCama][accesoPaciente] = idVacio

        actualizacion = f"\nActualización realizada para:\n Habitación: {habitaciones[indiceHab][accesoHab]}\n" #Hab
        actualizacion += f"Cama:{habitaciones[indiceHab][accesoCamas][indiceCama][accesoCama]}" #Número de cama
        actualizacion += f"\nNuevo estado:{habitaciones[indiceHab][accesoCamas][indiceCama][accesoEstado]}\n" #estado de la cama actualizado
        actualizacion += f"Paciente:{habitaciones[indiceHab][accesoCamas][indiceCama][accesoPaciente]}" #Id del paciente
        
        return habitaciones,actualizacion
    
    except Exception as e:
        return habitaciones, str(e)
    
#2: Actualizar el archivo con la cama disponible
def liberarCamaArchivo(archivo:str,habAliberar:int,camaALiberar:int,) -> str: #Devolverá nueva cama disponible
    try:
        habitacion = ""
        idVacio = "N/A"
        disponible = "disponible"
        buscarCama = ""
        lineaActualizada = ""
        ajuste = ""
       
        #Abrir archivo y cargar en memoria
        abrirArchivo = open(archivo,"r")
        contenidoArchivo = abrirArchivo.readlines()
        abrirArchivo.close()
        
        for i in range(len(contenidoArchivo)):
            
            linea = contenidoArchivo[i]
            habitacion = f"{habAliberar},"
            
            if linea.find(habitacion) == 0:#Si es la misma habitación y línea
                
                buscarCama = linea.find(f"{camaALiberar}",2)
                
                if habAliberar < 11: #Hab tipo A
                    limite = linea.find("\n", buscarCama)
                    lineaActualizada = f"1 - {disponible} - {idVacio}"
     
                elif habAliberar >= 11 : #Hab tip B
                    
                    if camaALiberar == 1:
                        limite = linea.find(" |", buscarCama)
                        lineaActualizada = f"1 - {disponible} - {idVacio}"
                    elif camaALiberar == 2:
                        limite = linea.find("\n", buscarCama)
                        lineaActualizada = f"2 - {disponible} - {idVacio}"
                
                ajuste = lineaActualizada
                contenidoArchivo[i] = linea[:buscarCama] + ajuste + linea[limite:]
            
            else:
                continue
            
            #Abrir archivo y reescribir en él
            abrirArchivo = open(archivo,"w")
            abrirArchivo.writelines(contenidoArchivo)
            abrirArchivo.close()
            
            return f"Habitación {habAliberar} archivo actualizado"
    except Exception as e:
        return e
# 3 Archivar historias
def archivarHistorias(idPaciente:str) -> str:
    try:
        
        origen = ""
        destino = ""
        carpetaDestino = "archivos"
        nombreArchivo = f"historia_{idPaciente}.txt"
        mensaje = ""
        
        os.makedirs(carpetaDestino, exist_ok=True) #función de Os que verifica carpeta (destino) y si no existe, la crea
        
        origen = open(nombreArchivo, "r")
        destino = open(f"archivos/{nombreArchivo}", "w")
        destino.write(origen.read())
        origen.close()
        destino.close()
    
        mensaje =  f"\nLa historia: {nombreArchivo} ha sido archivada en la carpeta llamada: {carpetaDestino}. \n"
        
        return mensaje
    except Exception as e:
        return e

def agregarPermanencia(idPaciente:str,estanciaDias: str) -> str:
    try:
        archivo =""
        
        archivo = open(f"historia_{idPaciente}.txt", "a")
        archivo.write(f"\nPermanencia(Días): {estanciaDias}")
        
        archivo.close()
        return f"\nPermanencia de {estanciaDias} días agregada a la historia.\n"
    
    except Exception as e:
        return e
      
#Funcionalidades del médico y enfermera 
def actualizarHistoria(usuario: str, rol: str, paciente: str, tipoEntrada: str) -> str: #Actualizar historia clínica del paciente
    try:
        mensaje = ""
        archivo = ""
        fecha = ""
        mensaje = "\n"+"-" * 10 + f"\n# Actualizando historia clínica del paciente {paciente}\n"
        archivo = f"historia_{paciente}.txt"
        
        if not os.path.exists(archivo):
            raise Exception(f"No existe una historia clínica para el paciente {paciente}.")
            
        fecha = datetime.datetime.now()

        with open(archivo, "a") as file:
            file.write(f"\n[{fecha}][{usuario}][{rol}][{tipoEntrada}]")

        mensaje += "La historia clínica ha sido actualizada exitosamente.\n"
        mensaje += "-" * 10 +'\n'
        
        return mensaje
    
    except Exception as e:
        return e

def darAlta(usuario:str,rol:str,paciente:str): #Dar de alta al paciente
    try:
        mensaje = ""
        archivo = ""
        fecha = ""
        mensaje = "\n---------- Dar de alta paciente ---------- \n"
        mensaje += "\n"+"-" * 10 + f"\n# Dando de alta al paciente {paciente}\n"
        archivo = f"historia_{paciente}.txt"
        
        if not os.path.exists(archivo):
            raise Exception(f"No existe una historia clínica para el paciente {paciente}")
        
        fecha = datetime.datetime.now()

        with open(archivo, "a") as file:
            file.write(f"\n[{fecha}][{usuario}][{rol}]:ALTA MEDICA")

        mensaje += "El paciente ha sido dado de alta exitosamente.\n"
        mensaje += "-" * 10 +'\n'
        return mensaje
    except Exception as e:
        return e

#Para el Módulo de reportes:
def obtenerArchivosDirectorio(carpeta:str) -> str: #Devolver lista con listas de archivos cargados
    try: 
        
        archivos = []
        accederCarpeta = ""
        contenidoArchivo = ""
        archivosCargados = []
        
        archivos = os.listdir(carpeta)

        if len(archivos) < 1:
            raise Exception("No hay archivos en la carpeta.")

        archivosCargados = []

        for archivo in archivos:
            accederCarpeta   = os.path.join(carpeta, archivo)
            abrirArchivo     = open(accederCarpeta, "r")
            contenidoArchivo = abrirArchivo.readlines()
            abrirArchivo.close()
            archivosCargados.append(contenidoArchivo)

        return archivosCargados 
    except Exception as e:
        return e

def calcularHabUsadas(archivosCargados:list) -> str:
    try:
        contHabTipoA = 0 #tipoA
        contHabtipoB = 0 #tipoB
        buscarHabA = 0
        buscarHabB = 0
        habtipoA = "tipoA"
        habTipoB = "tipoB"
        totalPacientes = 0
        tasaOcupacionA = 0
        tasaOcupacionB = 0
        resultado = ""
        
        totalPacientes = len(archivosCargados)
        for lineas in archivosCargados: #Acceder a cada archivo guardado (lineas!)
            for linea in lineas:
                buscarHabA = linea.find(habtipoA) #Buscar el índice para ambas hab
                buscarHabB = linea.find(habTipoB)
                
                if buscarHabA != -1 or buscarHabB != -1:
                    if buscarHabA != -1:
                        contHabTipoA += 1
                    elif buscarHabB != -1:
                        contHabtipoB += 1
                    break
        
        tasaOcupacionA = (contHabTipoA/totalPacientes) * 100
        tasaOcupacionB = (contHabtipoB/totalPacientes) * 100
        
        resultado = f"\nTasas calculadas por tipo de habitación:\nHabitación tipo A:{tasaOcupacionA}\nHabitación tipo B:{tasaOcupacionB}"    
         
        return resultado
                   
    except Exception as e:
        return e

def calcularMedicos(archivosCargados:list) -> str:
    try:
        listadoMedicos = [] #Estructura: [{"Nombre"}:Pacientes]
        altaMedica = "ALTA MEDICA"
        medicoEncontrado = False
        nombreMedico = ""
        accesoMedico = "medico"
        accesoPacientes = "pacientes"
       
        resultado = ""
        
        for lineas in archivosCargados:
            nombreMedico    = ""
            medicoEncontrado = False

            for linea in lineas:
                if altaMedica in linea:
                    partes       = linea.split("][")
                    nombreMedico = partes[1].strip() if len(partes) >= 3 else ""
                    break

            for i in range(len(listadoMedicos)):
                if listadoMedicos[i].get(accesoMedico) == nombreMedico:
                    listadoMedicos[i][accesoPacientes] += 1
                    medicoEncontrado = True
                    break

            if not medicoEncontrado and nombreMedico != "":
                listadoMedicos.append({accesoMedico: nombreMedico, accesoPacientes: 1})

        resultado = "Pacientes atendidos por cada médico:"
        for medico in listadoMedicos:
            resultado += f"\nMédico: {medico[accesoMedico]} — Pacientes: {medico[accesoPacientes]}"

        return resultado
                  
    except Exception as e:
        return e

def estadiaPromedio(archivosCargados:list) -> str:
    try: # Estruc. Línea: {idPaciente}\nCosto cama: {costoCama}\nPermanencia(Días): {dias}"
        
        buscarDias = "Permanencia(Días):"
        ultimoCaracter = ":"
        inicio = 0 #Usar .rfind()
        dias = ""
        totalPacientes = 0
        acumDias = 0
        promedio = 0
        resultado = ""
        
        totalPacientes = len(archivosCargados)
        for lineas in archivosCargados:
            for linea in lineas:
                if linea.find(buscarDias) != -1:
                    inicio = linea.rfind(ultimoCaracter)+1
                    dias = linea[inicio:].strip()
                    break
            
            if dias.isnumeric():
                acumDias += int(dias)
        
        if acumDias > 0 and totalPacientes > 0:
            promedio = acumDias / totalPacientes
            resultado += f"Estadía promedio de los pacientes:\nDe {totalPacientes} pacientes reportados, en promedio su estancia es de {promedio} días\n"
       
        return resultado      
        
    except Exception as e:
        return e

def crearReporte(promedioPacientes:str,medicos:str,tasaHab:str) -> str: #Retorna nombre del archivo creado
    try:
        
        contenido = ""
        archivoCreado = ""
        nombreArchivo = ""
        extension = ".txt"
        
        contenido += "Reporte final\n"
        contenido += f"\n{promedioPacientes}"
        contenido += f"\n{tasaHab}"
        contenido += f"\n{medicos}"
        
        nombreArchivo = f"reporte_final{extension}"
        
        archivoCreado = open(nombreArchivo,"a")
        archivoCreado.write(contenido)
        archivoCreado.close()
        
        return nombreArchivo
        
    except Exception as e:
        return e
    
#Apartado principal
try:
    #Datos de entrada
    usuario = ""
    contra = ""
    opcionMenu = 0
    idPaciente = ""
    costoCama = 0
    estanciaDias = 0
    continuar = "1"
    
    #Datos de salida
    asignacion = ""
    historiaPaciente = ""
    reporteFinal = ""
    
    #Variables alternativas
    nombreHospital = "Medellín" 
    rolAdmin = "ADMIN"
    rolMedico = "MEDICO"
    rolEnfermera = "ENFERMERA"
    #Archivos/Carpetas
    archivoPersonal = "personal.txt"
    archivoCamas = "estado_camas.txt"
    carpetaArchivados = "archivos"

    archivoAbierto = ""
    habitaciones = ""
    archivoModificado = ""
    rolIngresado = ""
    opcionRol = ""
    habPaciente = -1
    camaPaciente = -1
    camaEncontrada = 0
    nombreFactura = ""
    facturaCompleta = "" 
    camaLiberada = ""
    matrizLiberada = ""
    altaMedica = False
    altaMedicaAusente = "\nNo se encontró alta médica.\nComuníquese con el médico encargado. \n"
    tiposEntrada = ["Prescripción", "Suministro Medicamento", "Evolución","Prescripcion", "Evolucion"]
    actualizacionMedico = ""
    resultado = ""
    historiaArchivada = ""
    agregarHabitacion = ""
    diasAgregados = ""
    
    #Reporte:
    archivosReporte = []
    estanciaPacientes = ""
    tasaHabitaciones = ""
    pacientesMedicos = ""

    while continuar == "1":
        
        while True:
            try:
                usuario = input(f"\nBienvenido/a al portal de:\nHospital {nombreHospital} \n\nIncio de Sesión\nFecha de ingreso:{datetime.datetime.now()} \n - Recuerde que su usuario es su id.\n - Si desea salir del programa digite: 0 en la entrada de usuario.\n\nIngrese su usuario: ")
                if usuario.strip() == "0":
                    print("Programa finalizado.")
                    break
                contra = input("\nIngrese su contraseña: \n")
                #Sugerencia: levantar aquí error de usurio inválido
                rolIngresado = login(archivo=archivoPersonal,usuario=usuario,contra=contra)
                if rolIngresado == "":
                    raise Exception("Usuario y/o contraseña inválidos. Intente de nuevo.")
                elif not(rolIngresado == rolAdmin or rolIngresado == rolMedico or rolIngresado == rolEnfermera):
                    raise Exception("\nRol no reconocido por el portal. Comuníquese con el área encargada para su actualización.\n")
                else:
                    print(f"\nIngreso realizado con éxito.\nROL : {rolIngresado}...\n")
                    break #Este ciclo se rompe, una vez identifica un rol ( o devuelve un string NO vacío)
            except Exception as e:
                print(f"{e}") # Si no ingresa usuario y contraseña válidos entonces genera el error que dice PERO vuelve a preguntar, lo mismo si no reconoce el rol(PREGUNTAR ESO)
                continue
        
        if rolIngresado == rolAdmin:
            
            #Cargar habitaciones:
            archivoAbierto = abrirArchivo()
            habitaciones = cargarHabitaciones(archivoAbierto)
                
            while True:
                try:
                    opcionRol = input("\nIngrese alguna de las siguientes opciones:\n1: Asignar una cama y crear historia del paciente\n2: Verificar Alta Médica\n3: Facturación\n4: Crear reporte final\n\n0: Cerrar sesión\n-> ").strip()
                    if opcionRol.isnumeric() and not(0 <= int(opcionRol) <= 4):
                        raise Exception ("valor ingresado no se encuentra en el rango de opciones: (1|2|3|4|0)\n")
                    elif not(opcionRol.isnumeric() or opcionRol.replace(",","").replace(".","").isnumeric())  :
                        raise Exception ("valor ingresado no es un número entero.\n")
                    else:
                        break
                except Exception as e:
                    print(f"Indique un digito válido: {e}")
                    continue
           
            while opcionRol == "1" or opcionRol == "2" or opcionRol == "3" or opcionRol == "4" or opcionRol == "0":
                    
                if opcionRol == "0":
                    print("\nLa sesión ha sido cerrada por el usuario...\n")
                    opcionRol = ""
                    break
                    
                elif opcionRol == "1": #Asignar cama
                    while True:
                        idPaciente = input("\nIngrese el id del paciente: \n").replace(".","").strip()
                        if idPaciente.isnumeric():
                            print(f"\nID ingresado: {idPaciente}\n")
                            break
                        else:
                            print("\nRecuerde ingresar un id válido:numérico.\n")
                    
                    #Buscar cama libre en matriz
                    habPaciente,camaPaciente = identificarCamaDisponible(habitaciones)
                    if habPaciente > -1 and camaPaciente > -1:
                    #Hay camas disponibles: Devolver mensaje
                        asignacion = asignarCama(habitaciones,indiceHab=int(habPaciente),indiceCama=int(camaPaciente),idpaciente=idPaciente)
                        print(asignacion)
                        #Actualizar archivo con cama ocupada
                        archivoModificado = actualizarArchivo(archivo=archivoCamas,habAocupar=int(habPaciente+1),camaOcupada=int(camaPaciente+1),idPaciente=idPaciente)
                        print(archivoModificado)   
        
                        historiaPaciente = crearHistoriaPaciente(idPaciente=idPaciente) #Devuelve archivo nuevo del paciente
                        print(f"\nLa historia del paciente ha sido creada: {historiaPaciente}\n")
                        #Agregar a su historia la información de la habitación
                        agregarHabitacion = agregarDetalleshistoria(mensajeAsignacion=asignacion,idPaciente=idPaciente)
                        print(agregarHabitacion)
                        
                elif opcionRol == "2":
                    idPaciente = input("\nIngrese el id para validar el Alta Medica: \n").strip().replace(",","").replace(".","")
                    altaMedica = verificarAltaMedica(idPaciente=idPaciente)
                    if not(altaMedica):
                        print(altaMedicaAusente)
                    else:
                        print("\nEl Alta Medica ya se encuentra disponible.\n")
                        
                elif opcionRol == "3":
                    idPaciente = input("Ingrese el id del paciente a facturar: ").strip().replace(",","").replace(".","")
                    altaMedica = verificarAltaMedica(idPaciente=idPaciente)
                    if not(altaMedica):
                        print(f"\nRecuerde: Sin alta médica no se puede facturar. id paciente:{idPaciente}\n")
                    else:
                        print("Alta Medica confirmada ...")
                        
                    while True:
                        try: #VALIDAR DECIMALES
                            estanciaDias = input("\nIngrese la estancia en días del paciente: \n").strip()
                            if int(estanciaDias) <= 0:
                                raise ValueError("Valor ingresado es menor a 1.")
                            elif not(estanciaDias.isnumeric() or estanciaDias.isdecimal()):
                                raise TypeError("Valor ingresado no es un número entero.")
                            else:
                                break
                        except ValueError as e:
                            print(f"\nIngrese un número de días válido:{e}\n")
                            continue
                        except TypeError as e:
                            print(f"\nIngrese un número de días válido:{e}\n")
                            continue
            
                    while True:
                        try:
                            costoCama = input("\nIngrese el costo de la cama: \n").strip().replace(",","").replace(".","")
                            if int(costoCama) <= 0: #AGREGAR UN PRECIO MINIMO DEFINICIDO
                                raise ValueError("Valor ingresado es menor a 1.")
                            elif not(costoCama.isnumeric()):
                                raise TypeError("El costo debe ser un valor numérico")
                            else:
                                break
                        except ValueError as e:
                            print(f"Ingrese un costo válido: {e}")
                            continue
                        except TypeError as e:
                            print(f"Ingrese un costo válido: {e}")
                            continue
                    
                    diasAgregados = agregarPermanencia(idPaciente=idPaciente,estanciaDias=estanciaDias)          
                    #Generar archivo de factura
                    nombreFactura = factura(dias=int(estanciaDias),costoCama=int(costoCama),idPaciente=idPaciente)
                    print(f"\nSe ha generado la siguiente factura: {nombreFactura}\n")
                    #Liberar cama en matriz
                    habitaciones,matrizLiberada = liberarCamaEnMatriz(habitaciones,indiceHab=habPaciente,indiceCama=camaPaciente)
                    print(matrizLiberada)
                    #Liberar cama en archivo
                    camaLiberada = liberarCamaArchivo(archivo=archivoCamas,habAliberar=int(habPaciente)+1,camaALiberar=int(camaPaciente+1))
                    print(camaLiberada)
                    #Archivar historia
                    historiaArchivada = archivarHistorias(idPaciente=idPaciente)
                    print(historiaArchivada)
                    
                elif opcionRol == "4": #Crear reporte final
                        #Determinar promedio estancia
                        archivosReporte = obtenerArchivosDirectorio(carpeta=carpetaArchivados)
                        tasaHabitaciones = calcularHabUsadas(archivosCargados=archivosReporte)
                        estanciaPacientes = estadiaPromedio(archivosCargados=archivosReporte)
                        pacientesMedicos = calcularMedicos(archivosCargados=archivosReporte)
                        #Crear reporte(concatenar)
                        reporte = crearReporte(promedioPacientes=estanciaPacientes,medicos=pacientesMedicos,tasaHab=tasaHabitaciones)
                        #Imprimir reporte
                        print(reporte)
                    
                while True:
                        try:
                            opcionRol = input("\nIngrese alguna de las siguientes opciones:\n1: Asignar una cama y crear historia del paciente\n2: Verificar Alta Médica\n3: Facturación\n4: Crear reporte final\n\n0: Cerrar sesión\n-> ").strip()
                            if opcionRol.isnumeric() and not(0 <= int(opcionRol) <= 4):
                                raise Exception ("valor ingresado no se encuentra en el rango de opciones: (1|2|3|4|0)\n")
                            elif not(opcionRol.isnumeric() or opcionRol.replace(",","").replace(".","").isnumeric())  :
                                raise Exception ("valor ingresado no es un número entero.\n")
                            else:
                                break
                        except Exception as e:
                                print(f"Indique un digito válido: {e}")
                                continue

        elif rolIngresado == rolEnfermera or rolIngresado == rolMedico:
            while True:
                opcion_medico = "\n3. Dar de alta" if rolIngresado == rolMedico else ""
                opcionMenu = input(f"Ingrese el número de la operación que desea realizar: \n1: Ver historia\n2: Actualizar Historia{opcion_medico}\n0: Salir\n")
                try:
                    if opcionMenu == "1":
                            print("\n---------- Consultar Historia ---------- \n")
                            idPaciente = input("Ingrese el id del paciente: ")
                            result = consultarHistoria(idPaciente)
                            print(result)
                    elif opcionMenu == "2":
                        print("\n---------- Actualizar Historia ---------- \n")
                        idPaciente = input("Ingrese el id del paciente: ")
                        
                        while True:
                            tipoEntrada = input("Ingrese el tipo de entrada\n(Prescripción, Suministro Medicamento, Evolución):\nRecuerde escribirlo de forma completa\n").strip().title()
                            if tipoEntrada not in tiposEntrada:
                                    print("X --- Tipo de entrada inválido\n")
                            else:
                                actualizacionMedico = actualizarHistoria(usuario, rolIngresado, idPaciente, tipoEntrada)
                                print(actualizacionMedico)
                                break
                            
                    elif opcionMenu == "3" and rolIngresado == rolMedico:
                            idPaciente = input("Ingrese el id del paciente: ")
                            resultado = darAlta(usuario, rolIngresado, idPaciente)
                            print(resultado)
                    elif opcionMenu == "0":
                            print("\nCerrando sesión.\n")
                            rolIngresado = ""
                            break
                    else:
                        print("X --- Ingrese una opción válida\n")
                except Exception as e:
                    print("Ocurrio un error", e)
                    print("-" * 10 +'\n')
                
        while True:
            continuar = input("- Para iniciar sesión con otro usuario digite: 1 \n - Si finalizó el proceso médico y desea finalizar el programa definitivamente, digite: 0 \n").strip()
            if continuar == "0":
                print("Finalizando programa...")
                break
            elif continuar == "1":
                break
            else:
                print("\nIngrese una de las opciones anteriores.\n")
                
except Exception as e:
    print(f"Error en el sistema: {e} ")
finally:
    print("\nPrograma terminado.")