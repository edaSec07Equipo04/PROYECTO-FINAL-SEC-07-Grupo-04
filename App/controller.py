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

import config as cf
from App import model
import datetime
import csv

"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________

def initCatalog():
    """
    Llama la función de inicialización del catálogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________

def loadFile(catalog,informationFile):
    informationFile = cf.data_dir +informationFile
    inputFile = csv.DictReader(open(informationFile,encoding="utf-8-sig"),delimiter=",")
    for trip in inputFile:
        taxiId = trip['taxi_id']
        company = trip['company']
        
        if company == "":
            company = "Independent Owner"
        model.addService(catalog,trip)
        model.addCab(catalog,taxiId)
        model.addCompany(catalog,company)
        model.addCabInCompany(catalog,company,taxiId)
        model.addDate(catalog,trip)
# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def topCompanies(catalog):
    return model.topCompanies(catalog)

def topCabsInDate(catalog,date):
    dateTime = datetime.datetime.strptime(date,'%Y-%m-%d')
    return model.topCabsInDate(catalog,dateTime.date())

def topCabsInRange(catalog,initialDate,finalDate):
    initDate = datetime.datetime.strptime(initialDate,'%Y-%m-%d')
    finDate = datetime.datetime.strptime(finalDate,'%Y-%m-%d')
    return model.topCabsInRange(catalog,initDate.date(),finDate.date())

def servicesSize(catalog):
    return model.servicesSize(catalog)

def dateIndexHeight(catalog):
    return model.dateIndexHeight(catalog)

def dateIndexSize(catalog):
    return model.dateIndexSize(catalog)

def minKeyDate(catalog):
    return model.minKeyDate(catalog)

def maxKeyDate(catalog):
    return model.maxKeyDate(catalog)