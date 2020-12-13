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
    while asking:
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

    numedges = controller.totalConnections(cont)        #Número de arcos
    numvertex = controller.totalStops(cont)             #Número de vértices
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
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
        if cabsCount > cabsLimit:
            break
        else:
            print(str(cabsCount)+"- "+color.RED+'Empresa: ' +color.END+ name[1][0]+color.RED+
             ' Taxis afiliados: '+color.END+str(companyCabsD[name[1][0]]))
            cabsCount += 1
    print(color.GREEN +"=========================================================="+color.END)
    print(color.GREEN +"======== Top " + str(servicesLimit) + ' de compañías según servicios prestados ========'+color.END)
    servicesCount = 1
    for name in enumerate(servicesSorted):
        if servicesCount > servicesLimit:
            break
        else:
            print(str(servicesCount)+"- "+color.RED+'Empresa: ' +color.END+ name[1][0] + color.RED+' Servicios prestados: '
                    +color.END+ str(companyServicesD[name[1][0]]))
            servicesCount += 1
    print(color.GREEN +"=============================================================="+color.END)

#def optionFour():
     #N = input("Por favor indique los N taxis a consultar: ")
     #date = input("Por favor indique la fecha a consultar: ")
#    controller.

#def optionFive():
     #M = input("Por favor indique los N taxis a consultar: ")
     #print("A continuación le pediremos ingrese su rango de fechas a consultar")
     #date1 = input("Por favor ingrese la fecha inicial: ")
     #date2 = input("Por favor ingrese la fecha final: ")
#    controller.

#def optionSix():
    #origin = input("Por favor ingrese el área de origen: ")
    #destiny = input("Por favor ingrese el área de destino: ")
    #print("RANGO DE FECHAS")
    #fecha1 = input("Por favor ingrese la fecha inicial: ")  
    #fecha2 = input("Por favor ingrese la fecha final: ")    

#    controller.


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

#    elif int(opcion[0])==4:
#        tiempoEjecución = timeit.timeit(opcionFour, number=1)
#        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')
    
#    elif int(opcion[0])==5:
#        tiempoEjecución = timeit.timeit(opcionFive, number=1)
#        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')
    
#    elif int(opcion[0])==4:
#        tiempoEjecución = timeit.timeit(opcionSix, number=1)
#        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')
    

    else: 
        sys.exit(0)
sys.exit(0)
