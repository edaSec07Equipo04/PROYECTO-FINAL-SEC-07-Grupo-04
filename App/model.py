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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
import datetime
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
                'services':None,
                'dates':None}
    catalog['totalCabs'] = m.newMap(20143,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCabsById)
    catalog['companies'] = m.newMap(4447,
                                    maptype='PROBING',
                                    loadfactor=0.5,
                                    comparefunction=compareCompaniesByName)
    catalog['services'] = lt.newList('ARRAY_LIST')
    catalog['dates']=om.newMap(omaptype='RBT',
                                comparefunction=compareDates)

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

def addDate(catalog,trip):
    updateDateIndex(catalog['dates'],trip)
    return catalog

def updateDateIndex(map,trip):
    ocurreddate = trip['trip_start_timestamp']
    taxi_date = ocurreddate[:10]
    tripdate = datetime.datetime.strptime(taxi_date,'%Y-%m-%d')
    entry = om.get(map,tripdate.date())
    if entry is None:
        dateEntry = newDataEntry(trip)
        om.put(map,tripdate.date(),dateEntry)
    else:
        dateEntry = me.getValue(entry)
    addDateIndex(dateEntry,trip)
    return map

def addDateIndex(dateEntry,trip):
    trip_miles = (trip['trip_miles'])
    trip_miles.replace(" ","")
    if trip_miles == "":
        trip_miles = 0
    else:
        trip_miles = float(trip_miles)
    trip_total = (trip['trip_total'])
    trip_total.replace(" ","")
    if trip_total == "":
        trip_total = 0
    else:
        trip_total=float(trip_total)
    if trip_miles > 0.0 and trip_total > 0.0:
        lst = dateEntry['lstTrips']
        lt.addLast(lst,trip)
        taxiIndex=dateEntry['taxiId']
        taxiEntry = m.get(taxiIndex,trip['taxi_id'])
        if taxiEntry is None:
            entry = newTaxiEntry(trip['taxi_id'],trip)
            entry['distance']+=trip_miles
            entry['cash'] +=trip_total
            lt.addLast(entry['lstTaxi'],trip)
            m.put(taxiIndex,trip['taxi_id'],entry)
        else:
            entry = me.getValue(taxiEntry)
            lt.addLast(entry['lstTaxi'],trip)
            entry['distance']+=trip_miles
            entry['cash'] +=trip_total
    return dateEntry

def newDataEntry(trip):
    entry = {'taxiId':None,'lstTrips':None}
    entry['taxiId'] = m.newMap(numelements=20143,
                                maptype='PROBING',
                                comparefunction=compareCabsById)
    entry['lstTrips'] = lt.newList('ARRAY_LIST',compareCabsById)
    return entry 

def newTaxiEntry(taxiId,taxi):
    taxiEntry = {'taxi':None,'lstTaxi':None,'distance':0.0,'cash':0.0}
    taxiEntry['taxi'] = taxiId
    taxiEntry['lstTaxi'] = lt.newList('ARRAY_LIST',compareCabsById)
    return taxiEntry

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

def topCabsInDate(catalog,date):
    """
    Identifica los N taxis con más puntos para en una fecha determinada.
    """
    topPoints = {}  
    taxiDate = om.get(catalog['dates'],date)
    if taxiDate:
        if taxiDate['key'] is not None:  #Se ingresa a la información en la fecha ingresada
            taxiMap = me.getValue(taxiDate)['taxiId']
            keySet = m.keySet(taxiMap)
            iteratorKS = it.newIterator(keySet)
            while it.hasNext(iteratorKS):  #Se recorre cada ID de taxi en la fecha ingresada y se calculan sus respectivos puntos
                taxiId = it.next(iteratorKS)
                info = m.get(taxiMap,taxiId)
                services = (m.size(me.getValue(info)['lstTaxi']))
                distance = (me.getValue(info)['distance'])
                cash = (me.getValue(info)['cash'])
                points = (distance/cash)*services
                topPoints[taxiId] = round(points,3)
            pointsSorted = sorted(topPoints.items(),key=operator.itemgetter(1),reverse=True) #Se ordenan los taxis de acuerdo a los puntos
            return topPoints,pointsSorted
    else:
        return 0,1

def topCabsInRange(catalog,initialDate,finalDate):
    totalData = {}
    values = om.values(catalog['dates'],initialDate,finalDate)
    iterator = it.newIterator(values)
    while it.hasNext(iterator): #Se visita cada una de las fechas dentro del rango ingresado
        topPoints = {}
        info = it.next(iterator)
        keySet = m.keySet(info['taxiId'])
        iteratorKS = it.newIterator(keySet)
        while it.hasNext(iteratorKS): #Se recorre cada ID de taxi en la fecha y se calculan sus respectivos puntos
            taxiId = it.next(iteratorKS)
            inf = m.get(info['taxiId'],taxiId)
            services = m.size(me.getValue(inf)['lstTaxi'])
            distance = me.getValue(inf)['distance']
            cash = me.getValue(inf)['cash']
            points = (distance/cash)*services
            topPoints[taxiId] = points
        for key,value in topPoints.items(): #Si el ID se encuentra en el conjunto de datos, se suman sus valores, de lo contrario se agrega
            if key in totalData.keys():
                totalData[key]+=value
            else:
                totalData[key] = value
    dataSorted = sorted(totalData.items(),key=operator.itemgetter(1),reverse=True) #Se ordenan los taxis de acuerdo a los puntos
    return totalData,dataSorted

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

def compareDates(date1, date2):
    """
    Compara dos ids de viajes, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1
