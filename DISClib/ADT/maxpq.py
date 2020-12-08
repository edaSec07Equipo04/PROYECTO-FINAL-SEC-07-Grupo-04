"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 * Desarrollado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
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
 *
 * Contribución de:
 *
 * Dario Correal
 *
 """

import config
from DISClib.Utils import error as error
from DISClib.DataStructures import heap as h
assert config


"""
Implementación de una cola de prioridad orientada a menor

Este código está basados en la implementación
propuesta por R.Sedgewick y Kevin Wayne en su libro
Algorithms, 4th Edition
"""


def newMaxPQ(cmpfunction):
    """
    Crea un cola de prioridad orientada a mayor

    Args:
        cmpfunction: La funcion de comparacion
        size: El numero de elementos
    Returns:
       El heap
    Raises:
        Exception
    """
    try:
        pq = {'heap': None}
        pq['heap'] = h.newHeap(cmpfunction)
        return pq

    except Exception as exp:
        error.reraise(exp, 'newMaxPQ')


def size(maxpq):
    """
    Retorna el número de elementos en la MaxPQ
    Args:
        maxpq: la cola de prioridad
    Returns:
       El tamaño de la MaxPQ
    Raises:
        Exception
    """
    try:
        return (h.size(maxpq['heap']))
    except Exception as exp:
        error.reraise(exp, 'maxpq:size')


def isEmpty(maxpq):
    """
    Indica si la MaxPQ está vacía

    Args:
        heap: El arreglo con la informacion
    Returns:
      True si esta vacia
    Raises:
        Exception
    """
    try:
        return (h.isEmpty(maxpq['heap']))
    except Exception as exp:
        error.reraise(exp, 'maxpq:isEmpty')


def max(maxpq):
    """
    Retorna el primer elemento de la MaxPQ, es decir el menor elemento

    Args:
        maxpq: La cola de prioridad
    Returns:
      El menor elemento de la MinPQ
    Raises:
        Exception
    """
    try:
        return h.min(minpq['heap'])
    except Exception as exp:
        error.reraise(exp, 'maxpq:min')


def insert(maxpq, element):
    """
    Guarda el elemento 'element' en la cola de prioridad.
    Lo guarda en la última posición y luego hace swim del elemento

    Args:
        maxpq: El arreglo con la informacion
        element: El elemento a guardar
    Returns:
        La MaxPQ con el nuevo elemento
    Raises:
        Exception
    """
    try:
        maxpq['heap'] = h.insert(maxpq['heap'], element)
        return maxpq
    except Exception as exp:
        error.reraise(exp, 'maxpq:insert')


def delMax(maxpq):
    """
    Retorna el menor elemento de la MaxPQ y lo elimina.
    Se reemplaza con el último elemento y se hace sink.

    Args:
        maxpq: La cola de prioridad

    Returns:
        El menor elemento eliminado
    Raises:
        Exception
    """
    try:
        return (h.delMin(maxpq['heap']))
    except Exception as exp:
        error.reraise(exp, 'maxpq:delMax')