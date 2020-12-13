"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """


import sys
import config
from App import controller
from DISClib.ADT import stack
import timeit
from DISClib.ADT import list as lt
assert config


"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

recursionLimit = 20000

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("************************************************")
    print(color.YELLOW + "BIENVENIDO" + color.END)

    print(color.BOLD + "1-" + color.END + " Inicializar analizador.")
    print(color.BOLD + "2-" + color.END + " Cargar información de servicios.")
    print(color.DARKCYAN + "FUNCIONES REQUERIMIENTO 1" + color.END)
    print(color.BOLD + "3-" + color.END + " Mostrar el top de compañías.")

    print(color.DARKCYAN + "FUNCIONES REQUERIMIENTO 2" + color.END)
    print(color.BOLD + "4- " + color.END + "Los N taxis con más puntos en una fecha")
    print(color.BOLD + "5- " + color.END + "Los M taxis con más puntos en un rango de fechas")

    print(color.DARKCYAN + "FUNCIONES REQUERIMIENTO 3" + color.END)
    print(color.BOLD + "6- " + color.END + "Conecer el mejor horario para desplazarse entre dos " + color.UNDERLINE + "Community Area " + color.END)

    print(color.BOLD + "0- SALIR" + color.END)
    print("************************************************")

def optionTwo():
    asking = True
    problem = "No se encontró el archivo buscado. Ingréselo nuevamente."
    fileRequest = input("¿Qué archivo desea cargar? (small, medium, large): ")
    while asking:    #Pregunta hasta que se ingrese un valor válido
        if fileRequest.lower() == "small":
            file = "taxi-trips-wrvz-psew-subset-small.csv"
            asking = False
        elif fileRequest.lower() == "medium":
            file = "taxi-trips-wrvz-psew-subset-medium.csv"
            asking = False
        elif fileRequest.lower() == "large":
            file = "taxi-trips-wrvz-psew-subset-large.csv"
            asking = False
        else:
            print(problem)
            fileRequest = input("¿Qué archivo desea cargar? (small, medium, large): ")
    print("\nCargando información de servicios...")
    controller.loadFile(cont,file)
    print('Número de servicios cargados: ' +str(controller.servicesSize(cont)))
    sys.setrecursionlimit(recursionLimit)
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))
    

def optionThree():
    cabsLimit = int(input("Ingrese el número de compañías que desea en su top de taxis afiliados: "))
    servicesLimit = int(input("Ingrese el número de compañías que desea en su top de servicios prestados: "))
    print("\n")
    totalCompanies,totalCabs,companyServicesD,servicesSorted,companyCabsD,cabsSorted=controller.topCompanies(cont)
    print(color.RED+"Número total de taxis en los servicios cargados: " +color.END+ str(totalCabs))
    print(color.RED+"Número total de compañías con al menos un taxi inscrito: " +color.END+ str(totalCompanies))
    print(color.GREEN +"======== Top " + str(cabsLimit) + ' de compañías según taxis afiliados ========'+color.END)
    cabsCount = 1
    for name in enumerate(cabsSorted):
        if cabsCount > cabsLimit: #Revisa que la impresión se haga hasta la compañía número N
            break
        else:
            print(str(cabsCount)+"- "+color.RED+'Empresa: ' +color.END+ name[1][0]+color.RED+
             ' Taxis afiliados: '+color.END+str(companyCabsD[name[1][0]]))
            cabsCount += 1
    print(color.GREEN +"=========================================================="+color.END)
    print(color.GREEN +"======== Top " + str(servicesLimit) + ' de compañías según servicios prestados ========'+color.END)
    servicesCount = 1
    for name in enumerate(servicesSorted):
        if servicesCount > servicesLimit: #Revisa que la impresión se haga hasta la compañía número N
            break
        else:
            print(str(servicesCount)+"- "+color.RED+'Empresa: ' +color.END+ name[1][0] + color.RED+' Servicios prestados: '
                    +color.END+ str(companyServicesD[name[1][0]]))
            servicesCount += 1
    print(color.GREEN +"=============================================================="+color.END)

def optionFour():
    N = int(input("Por favor indique los N taxis a consultar: "))
    date = input("Por favor indique la fecha a consultar (AAAA-MM-DD): ")
    topPoints,pointsSorted = controller.topCabsInDate(cont,date)
    if topPoints == 0 and pointsSorted == 1:
        print('La fecha ingresada no se encuentra dentro de la base de datos')
    else: 
        pointsCount = 1
        print(color.GREEN +"============= Top " + str(N) + ' de taxis con más puntos en ' + date +' ============='+color.END)
        for name in enumerate(pointsSorted):
            if pointsCount > N: #Revisa que la impresión se haga hasta el taxi número N
                break
            else:
                print(str(pointsCount)+"- "+ color.RED +'Taxi: '+ color.END + name[1][0]) 
                print(color.RED+' \tTotal de puntos: '+color.END+str(topPoints[name[1][0]]))
                pointsCount+=1
        print(color.GREEN +"===================================================================="+color.END)

def optionFive():
    M = int(input("Por favor indique los N taxis a consultar: "))
    print("A continuación le pediremos ingrese su rango de fechas a consultar")
    date1 = input("Por favor ingrese la fecha inicial: (AAAA-MM-DD): ")
    date2 = input("Por favor ingrese la fecha final: (AAAA-MM-DD): ")
    totalData,dataSorted = controller.topCabsInRange(cont,date1,date2)
    pointsCount = 1
    print(color.GREEN +"============= Top " + str(M) + ' de taxis con más puntos entre ' + date1 +' y '+date2+' ============='+color.END)
    for name in enumerate(dataSorted):
        if pointsCount > M:  #Revisa que la impresión se haga hasta el taxi número N
            break
        else:
            print(str(pointsCount)+"- "+ color.RED +'Taxi: '+ color.END + name[1][0])
            print(color.RED+' \tTotal de puntos: '+color.END+str(totalData[name[1][0]])) 
            pointsCount += 1
    print(color.GREEN +"===================================================================="+color.END)

def optionSix():
    origin = input("Por favor ingrese el área de origen: ")
    destiny = input("Por favor ingrese el área de destino: ")
    print("RANGO DE HORARIO")
    hora1 = input("Por favor ingrese la hora inicial (HH:MM): ")  
    hora2 = input("Por favor ingrese la hora final (HH:MM): ")    

    path,time = controller.mejorH(origin,destiny,hora1,hora2,cont)
    
    elemento1 = lt.getElement(path,1) #Sacamos de la lista el vertive inicial y final
    elemento2 = lt.lastElement(path)
    e1 = elemento1.split(" ")         #Separamos hora de vertice
    e2 = elemento2.split(" ") 
    tInicial = e1[1]                  #Hora de inicio
    tFinal   = e2[1]                  #Hora Final

    print("Buscando el mejor horario para iniciar el viaje...")
    print("\n")
    print(color.GREEN + "El mejor horario para iniciar el viaje es a las: "+color.END)
    print(tInicial)
    tamanio = lt.size(path)
    print("\n")
    print(color.GREEN + "RUTA MÁS APROPIADA" + color.END)
    for i in  range(1,int(tamanio)+1):

        a = lt.getElement(path,i)
        b = a.split(" ")
        vertice = b[0]
        print(color.BLUE + "Community Area número " + str(i) + ": "+color.END + vertice) 
    print("\n")
    print(color.GREEN + "El tiempo estimado de viaje es: "+color.END)
    controller.segundosAfecha(time)   #Tiempo de viaje en formato bonito
    print("\n")


"""
Menu principal
"""
while True:
    printMenu()
    opcion = input('Seleccione una opción para continuar: ')

    if int(len(opcion)==1) and int(opcion[0])==1:
        print("\nInicializando...")

        cont = controller.initCatalog()
        

    elif int(opcion[0])==2:

        tiempoEjecución = timeit.timeit(optionTwo, number=1)
        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')

    elif int(opcion[0])==3:

        tiempoEjecución = timeit.timeit(optionThree, number=1)
        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')

    elif int(opcion[0])==4:
        tiempoEjecución = timeit.timeit(optionFour, number=1)
        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')
    
    elif int(opcion[0])==5:
        tiempoEjecución = timeit.timeit(optionFive, number=1)
        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')

    elif int(opcion[0])==6:
        tiempoEjecución = timeit.timeit(optionSix, number=1)
        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')

    


    

    else: 
        sys.exit(0)
sys.exit(0)
