"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
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
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos, y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv

from ADT import lss as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import quicksort as qs
from time import process_time 



def printMenu():
    """
    Imprime el menu de opciones
    """
    print("\nBienvenido")
    print("1- Cargar Datos")
    print("2- Ranking de peliculas")
    print("3- Conocer un director")
    print("4- Conocer un actor")
    print("5- Entender un genero")
    print("6- Crear ranking por genero")
    print("0- Salir")



def filtrar_por_genero(lst,criteria):
    iterador=it.newIterator(lst)
    lista = lt.newList()
    while it.hasNext(iterador)==True:
        dato = it.next(iterador)
        if dato['genre'].lower().strip()==criteria:
            lt.addLast(lista,dato)
    if lt.size(lista) > 0:
        retorno = lista
    else:
        retorno = -1
    return retorno

def crear_ranking_de_genero(criteria, lst):
    filtered = filtrar_por_genero(lst)
    qs.quickSort(filtered,compareRecordVotes)
    ranking_votes = filtered.copy()
    qs.quickSort(filtered,compareRecordAverage)
    ranking_average = filtered.copy()
    return (ranking_votes,ranking_average)


def compareRecordVotes (recordA, recordB):
    if int(recordA['vote_count']) == int(recordB['vote_count']):
        return 0
    elif int(recordA['vote_count']) > int(recordB['vote_count']):
        return 1
    return -1

def compareRecordAverage (recordA, recordB):
    if int(recordA['vote_average']) == int(recordB['vote_average']):
        return 0
    elif int(recordA['vote_average']) > int(recordB['vote_average']):
        return 1
    return -1
         

def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1


def loadCSVFile (file, cmpfunction):
    lst=lt.newList("SINGLE_LINKED", cmpfunction)
    dialect = csv.excel()
    dialect.delimiter=";"
    try:
        with open(cf.data_dir + file, encoding="utf-8-sig") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    print(lst)
    return lst


def loadMovies (file):
    lst = loadCSVFile(file,compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def menu_cargar():
    print('Menu de opciones: ')
    print('1. Cargar Archivos Pequeños')
    print('2. Cargar Archivos Grandes')

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """


    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar\n') #leer opción ingresada
        if len(inputs)>0:
            lista1 = {}
            lista2 = {}
            if int(inputs[0])==1: #opcion 1
                continuar = True
                while continuar == True:
                    menu_cargar()
                    opcion = input('Digite su opción: ')
                    if opcion == '1':
                        lista1 = loadMovies('Data/themoviesdb/MoviesCastingRaw-small.csv')
                        lista2 = loadMovies('Data/themoviesdb/SmallMoviesDetailsCleaned.csv')
                        continuar = False
                    elif opcion == '2':
                        lista1 = loadMovies('Data/themoviesdb/AllMoviesCastingRaw.csv')
                        lista2 = loadMovies('Data/themoviesdb/AllMoviesDetailsCleaned.csv')
                        continuar = False
                    else:
                        print('Opcion no valida')
                        menu_cargar()
                        opcion = input('Digite su opción: ')

            elif int(inputs[0])==2: #opcion 2
                pass

            elif int(inputs[0])==3: #opcion 3
                pass

            elif int(inputs[0])==4: #opcion 4
                pass

            elif int(inputs[0])==3: #opcion 5
                pass

            elif int(inputs[0])==4: #opcion 6
                'No'

                x=input('Digite la longitud del ranking: ')
                y=input('Digite el genero a filtrar: ')
                data = crear_ranking_de_genero(y,lista2)
                if data == -1:
                    print('El genero no existe')
                else:
                    print('El ranking por votos para el genero ',y,' es:')
                    for i in range(x):
                        print(x+1,'- ',lt.getElement(data[0],x)['original_title'])    
                    input('Digite enter para ver el siguiente ranking ---------->:')
                    print('El ranking por promedio para el genero ',y,' es:')
                    for i in range(x):
                        print(x+1,'- ',lt.getElement(data[1],x)['original_title'])
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
                
if __name__ == "__main__":
    main()