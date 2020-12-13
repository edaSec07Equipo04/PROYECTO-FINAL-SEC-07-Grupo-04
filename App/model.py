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
import datetime
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import edge as e
from DISClib.ADT import stack as st
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
    try:
        catalog = {'totalCabs':None,
                    'companies':None,
                    'services':None,
                    'graph'   :None,
                    'paths'   :None}
        catalog['totalCabs'] = m.newMap(20143,
                                        maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareCabsById)
        catalog['companies'] = m.newMap(4447,
                                        maptype='PROBING',
                                        loadfactor=0.5,
                                        comparefunction=compareCompaniesByName)
        catalog['services'] = lt.newList('ARRAY_LIST')
        catalog['graph']=gr.newGraph(datastructure='ADJ_LIST',
                                            directed=True,
                                            size=1000,
                                            comparefunction=compareStations)
        return catalog
    except Exception as exp:
        error.reraise(exp, 'model:newCatalog')

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
#############################################

def addTrip(catalog, trip):
    """
    """
    origin = trip['pickup_community_area']
    destination = trip['dropoff_community_area']
    
    if origin != destination:        
        if trip['trip_seconds'] != "" and trip['trip_seconds']!= None:
            if origin != None and destination != None:
                if origin != "" and destination != "":
                    origin = str(int(float(origin)))
                    destination = str(int(float(destination)))
                    d = float(trip['trip_seconds'])
                    
                    duration = int(d)
                              
                    ocurredhour_initial = trip['trip_start_timestamp']
                    taxi_hour_initial = ocurredhour_initial[11:16]
                    

                    ocurredhour_final= trip['trip_end_timestamp']
                    taxi_hour_final= ocurredhour_final[11:16]

                    valueI = origin + " " + taxi_hour_initial
                    valueF = destination + " " + taxi_hour_final
                    addStation(catalog,valueI)
                    addStation(catalog,valueF)
                    addConnection(catalog,valueI,valueF,duration)
                else:
                    pass
            else:
                pass
        else: 
            pass
    else:
        pass

def addStation(catalog,stationId):
    """
    Adiciona una estación como un vértice del grafo
    """
    if not gr.containsVertex(catalog['graph'],stationId):
        gr.insertVertex(catalog['graph'],stationId)
    return catalog

def addConnection(catalog,origin,destination,duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(catalog['graph'],origin,destination)
    if edge is None:
        gr.addEdge(catalog['graph'],origin,destination,duration)
    else:
        e.updateAverageWeight(edge,duration)
    return catalog

# ====================================
# Funciones de consulta para el GRAFO
# ====================================

def totalStops(catalog):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(catalog['graph'])


def totalConnections(catalog):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(catalog['graph'])   

def numSCC(graph):
    """
    Informa cuántos componentes fuertemente conectados se encontraron
    """
    sc = scc.KosarajuSCC(graph)
    return scc.connectedComponents(sc)

def sameCC(graph,station1,station2):
    """
    Informa si dos estaciones están en el mismo componente conectado.
    """
    sc = scc.KosarajuSCC(graph)
    return scc.stronglyConnected(sc,station1,station2)

def stationsSize(graph):
    return lt.size(graph['stations'])

def minimumCostPaths(catalog,station):
    """
    Calcula los caminos de costo mínimo desde la estación
    a todos los demas vertices del grafo
    """
    if gr.containsVertex(catalog['graph'],station):
        catalog['paths'] = djk.Dijkstra(catalog['graph'],station)
        return catalog
    else:
        return -1
       
def minimumCostPath(catalog,station):
    """
    Retorna el camino de costo mínimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    if gr.containsVertex(catalog['graph'],station):
        path = djk.pathTo(catalog['paths'],station)
        return path
    else:
        return -1



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

def funcion(origen,destino,horaI,horaF,catalog):

    menor=100000000000000000000000
    menorp=''        
    inicio = origen + " " + horaI
    i = datetime.datetime.strptime(horaI, '%H:%M')
    f = datetime.datetime.strptime(horaF, '%H:%M') 
    
    while i < f:       
        inicio = origen + " " + horaI
        i = datetime.datetime.strptime(horaI, '%H:%M')
        caminos = minimumCostPaths(catalog,inicio)       
        if caminos != -1:
            variable = "00:00"           
            contador = 0
            while contador < 95:    
                final = destino + " " + variable
                x = datetime.datetime.strptime(variable, '%H:%M')               
                path = minimumCostPath(caminos, final)
                retorno = lt.newList('ARRAY_LIST',compareValues)                
                if path!=-1:                  
                    if path is not None:                        
                        suma=0
                        while (not st.isEmpty(path)):
                            stop=st.pop(path)
                            if lt.isPresent(retorno,stop['vertexA'])==0:
                                lt.addLast(retorno,stop['vertexA'])
                            if lt.isPresent(retorno,stop['vertexB'])==0:
                                lt.addLast(retorno,stop['vertexB'])
                            if stop['weight']is not None:
                                suma+=stop['weight']
                        if suma < menor:                           
                            menor=suma
                            menorp=retorno                            
                tiempo_f= x+datetime.timedelta(0,900)
                variable= str(tiempo_f)[11:16]
                contador+=1
        t=i+datetime.timedelta(0,900)
        horaI=str(t)[11:16]

    return menorp,menor


# ==============================
# Funciones Helper
# ==============================

def obtainCompanies(catalog):
    """
    Obtiene los nombres de las compañías (llaves) en el catálogo
    """
    return m.keySet(catalog['companies'])

def convertSecondsToDate(seconds):
    """
    Transforma segundos a días, horas, minutos y segundos.
    """
    days = seconds//(24*60*60)
    seconds = seconds % (24*60*60)
    hours = seconds // (60*60)
    seconds = seconds %(60*60)
    minutes = seconds // 60 
    seconds = seconds % 60
    print('Días: {} - Horas: {} - Minutos: {} - Segundos: {}'.format(int(days),int(hours),int(minutes),int(seconds)))

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
def compareStations(station, keyvaluestation):
    """
    Compara dos estaciones
    """
    stationId = keyvaluestation['key']
    if (station == stationId):
        return 0
    elif (station > stationId):
        return 1
    else:
        return -1

def compareValues(v1,v2):
    if v1 == v2:
        return 0
    elif v1 > v2:
        return 1
    else:
        return -1
