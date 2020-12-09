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
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import operator
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------

def newCatalog():
    catalog = {'totalCabs':None,
                'companies':None,
                'services':None}
    catalog['totalCabs'] = m.newMap(20143,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCabsById)
    catalog['companies'] = m.newMap(4447,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCompaniesByName)
    catalog['services'] = lt.newList('ARRAY_LIST')
    return catalog

def newCab(taxiId):
    """
    Crea una nueva estructura para modelar el número de taxis en los servicios reportados.
    """
    cab = {'id': '', 'trips':0}
    cab['id'] = taxiId
    return cab

def newCompany(companyName):
    """
    Crea una nueva estructura para modelar el número de compañías con al menos un taxi afiliado.
    """
    company = {'name': '','cabs':None, 'totalCabs':0,'totalServices':0}
    company['name'] = companyName
    company['cabs'] = m.newMap(31,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareCabsById)
    return company
# Funciones para agregar informacion al catálogo

def addService(catalog,service):
    services = catalog['services']
    lt.addLast(services,service)

def addCompany(catalog,company):
    """
    Crea una nueva estructura para modelar el número de compañías con al menos un taxi afiliado.
    """
    companies = catalog['companies']
    existCompany = m.contains(companies,company)
    if existCompany:
        entry = m.get(companies,company)
        data = me.getValue(entry)
    else:
        data = newCompany(company)
        m.put(companies,company,data)
    data['totalServices'] += 1

def addCabInCompany(catalog,company,taxiId):
    """
    Relaciona un taxi a la compañía a la cual está afiliado.
    """
    companies = catalog['companies']
    info = m.get(companies,company)
    companyCabs = me.getValue(info)['cabs']
    existCab = m.contains(companyCabs,taxiId)
    if existCab:
        entry = m.get(companyCabs,taxiId)
        data = me.getValue(entry)       
    else:
        data = newCab(taxiId)
        m.put(companyCabs,taxiId,data)
        me.getValue(info)['totalCabs'] += 1
    data['trips'] += 1

def addCab(catalog,taxiId):
    """
    Crea una nueva estructura para modelar el número de taxis en los servicios reportados.
    """
    cabs = catalog['totalCabs']
    existCab = m.contains(cabs,taxiId)
    if existCab:
        entry = m.get(cabs,taxiId)
        data = me.getValue(entry)
    else:
        data = newCab(taxiId)     
        m.put(cabs,taxiId,data)
    data['trips'] += 1

# ==============================
# Funciones de consulta
# ==============================
def topCompanies(catalog):
    """
    Informa:
    - El número total de taxis en los servicios reportados.
    - El número total de compañías que tienen al menos un taxi inscrito.
    - El top M de compañías ordenada por la cantidad de taxis afiliados. 
    - El top N de compañías que más servicios prestaron.
    """
    totalCompanies = companiesSize(catalog) #Número de compañías
    totalCabs = cabsSize(catalog) #Número de taxis
    companies = obtainCompanies(catalog) #Se obtienen los nombres de las compañías
    companiesMap = catalog['companies']
    companyCabsD = {}
    companyServicesD = {}
    iterator = it.newIterator(companies)
    companiesList = lt.newList("ARRAY_LIST")
    while it.hasNext(iterator):  #Se organizan de mayor a menor las compañías según su número de taxis y servicios prestados
        lst = lt.newList('ARRAY_LIST')
        companyName = it.next(iterator)
        info = m.get(companiesMap,companyName)
        valueCabs = me.getValue(info)['totalCabs']
        valueServices = me.getValue(info)['totalServices']
        companyCabsD[companyName] = valueCabs
        companyServicesD[companyName] = valueServices
    servicesSorted = sorted(companyServicesD.items(),key=operator.itemgetter(1),reverse=True)
    cabsSorted = sorted(companyCabsD.items(),key=operator.itemgetter(1),reverse=True)
    return totalCompanies,totalCabs,companyServicesD,servicesSorted,companyCabsD,cabsSorted

def servicesSize(catalog):
    """
    Informa el número de servicios reportados
    """
    return lt.size(catalog['services'])

def companiesSize(catalog):
    """
    Informa el número de compañías con al menos un taxi inscrito
    """
    size = m.size(catalog['companies'])
    return size

def cabsSize(catalog):
    """
    Informa el número total de taxis en los servicios reportados
    """
    size = m.size(catalog['totalCabs'])
    return size


# ==============================
# Funciones Helper
# ==============================

def obtainCompanies(catalog):
    """
    Obtiene los nombres de las compañías (llaves) en el catálogo
    """
    return m.keySet(catalog['companies'])

# ==============================
# Funciones de Comparacion
# ==============================
def compareCompaniesByName(keyname, company):
    """
    Compara dos nombres de compañías. El primero es una cadena
    y el segundo un entry de un map
    """
    companyEntry = me.getKey(company)
    if (keyname == companyEntry):
        return 0
    elif (keyname > companyEntry):
        return 1
    else:
        return -1

def compareCabsById(keyname, cab):
    """
    Compara dos nombres de compañías. El primero es una cadena
    y el segundo un entry de un map
    """
    cabEntry = me.getKey(cab)
    if (keyname == cabEntry):
        return 0
    elif (keyname > cabEntry):
        return 1
    else:
        return -1

