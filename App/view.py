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
file = "taxi-trips-wrvz-psew-subset-small.csv"

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
    print("\n")
    print(color.DARKCYAN + "FUNCIONES REQUERIMIENTO 1" + color.END)
    print(color.BOLD + "1-" + color.END + " Inicializar analizador.")
    print(color.BOLD + "2-" + color.END + " Cargar información de servicios.")
    print(color.BOLD + "3-" + color.END + " Mostrar el top de compañías.")
    print("\n")
    print(color.DARKCYAN + "FUNCIONES REQUERIMIENTO 2" + color.END)
    print(color.BOLD + "4- " + color.END + "Los N taxis con más puntos en una fecha")
    print(color.BOLD + "5- " + color.END + "Los M taxis con más puntos en un rango de fechas")
    print("\n")
    print(color.DARKCYAN + "FUNCIONES REQUERIMIENTO 3" + color.END)
    print(color.BOLD + "6- " + color.END + "Conecer el mejor horario para desplazarse entre dos " + color.UNDERLINE + "Community Area " + color.END)
    print("\n")
    print(color.BOLD + "0- SALIR" + color.END)
    print("************************************************")

def optionTwo():
    print("\nCargando información de servicios...")
    controller.loadFile(cont,file)
    print("Total de compañías cargadas: "+str(controller.companiesSize(cont)))
    print("Total de taxis cargados: "+str(controller.cabsSize(cont)))

def optionThree():
    controller.topCompanies(cont)

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
