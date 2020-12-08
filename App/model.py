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
from DISClib.ADT import maxpq
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
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
                'companies':None}
    catalog['totalCabs'] = m.newMap(20143,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCabsById)
    catalog['companies'] = m.newMap(20143,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCompaniesByName)
    return catalog

def newCab(taxiId):
    """
    Crea una nueva estructura para modelar...
    """
    cab = {'id': '', 'trips':0}
    cab['id'] = taxiId
    return cab

def newCompany(companyName):
    """
    Crea una nueva estructura para modelar...
    """
    company = {'name': '','cabs':None, 'totalCabs':0}
    company['name'] = companyName
    company['cabs'] = m.newMap(17,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=compareCabsById)
    return company
# Funciones para agregar informacion al grafo

def addCompany(catalog,company):
    """
    Crea una nueva estructura para modelar...
    """
    companies = catalog['companies']
    existCompany = m.contains(companies,company)
    if existCompany:
        entry = m.get(companies,company)
        data = me.getValue(entry)
    else:
        data = newCompany(company)
        m.put(companies,company,data)

def addCabInCompany(catalog,company,taxiId):
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
    data['trips'] += 1
    me.getValue(info)['totalCabs'] += 1


def addCab(catalog,taxiId):
    """
    Crea una nueva estructura para modelar...
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
    companies = obtainCompanies(catalog)
    companiesMap = catalog['companies']
    mpq = maxpq.newMaxPQ(compareCabsQuantity) 
    iterator = it.newIterator(companies)
    total = 0
    while it.hasNext(iterator):
        companyName = it.next(iterator)
        print(companyName)
        print(m.size())
        info = m.get(catalog['companies'],companyName)
        value = me.getValue(info)
        total += m.size(value['cabs'])
    print(total)
        


def obtainCompanies(catalog):
    return m.keySet(catalog['companies'])

def companiesSize(catalog):
    size = m.size(catalog['companies'])
    return size

def cabsSize(catalog):
    size = m.size(catalog['totalCabs'])
    return size

# ==============================
# Funciones Helper
# ==============================

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

def compareCabsQuantity(value1,value2):
    if value1 == value2:
        return 0
    elif value1 > value2:
        return 1
    else:
        return -1