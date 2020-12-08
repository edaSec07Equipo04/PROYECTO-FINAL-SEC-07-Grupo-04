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

# ___________________________________________________
#  Menu principal
# ___________________________________________________
def printMenu():
    print("\n")
    print("************************************************")
    print("BIENVENIDO")
    print("1- Inicializar analizador.")
    print("2- Cargar información de servicios.")
    print("3- Mostrar el top de compañías.")
    print("************************************************")

def optionTwo():
    print("\nCargando información de servicios...")
    controller.loadFile(cont,file)
    print("Total de compañías cargadas: "+str(controller.companiesSize(cont)))
    print("Total de taxis cargados: "+str(controller.cabsSize(cont)))

def optionThree():
    controller.topCompanies(cont)

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

        #OJO CON TIEMPO DE EJECUCION#
        tiempoEjecución = timeit.timeit(optionTwo, number=1)
        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')

    elif int(opcion[0])==3:

        #OJO CON TIEMPO DE EJECUCION#
        tiempoEjecución = timeit.timeit(optionThree, number=1)
        print("El tiempo de ejecución de la función fue: " + str(tiempoEjecución)+ ' segundos')
    else: 
        sys.exit(0)
sys.exit(0)