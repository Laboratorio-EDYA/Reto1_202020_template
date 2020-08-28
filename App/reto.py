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

from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt

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
    print("6- Crear ranking")
    print("0- Salir")

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
        with open(file, encoding="utf-8-sig") as csvfile:
            row = csv.DictReader(csvfile, dialect=dialect)
            for elemento in row: 
                lt.addLast(lst,elemento)
    except:
        print("Hubo un error con la carga del archivo")
    return lst

def loadMovies (file):
    lst = loadCSVFile(file,compareRecordIds) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def menu_cargar():
    print('Menu de opciones: ')
    print('1. Cargar Archivos Pequeños')
    print('2. Cargar Archivos Grandes')

def conocerUnDirector(lst1, lst2, name):
    t1_start = process_time() #tiempo inicial
    retorno = {'ids': [], 'movies_names': [], 'average': 0.0}
    it_list1 = it.newIterator(lst1)
    while it.hasNext(it_list1) == True:
        data = it.next(it_list1)
        if data['director_name'].lower().strip() == name:
            retorno['ids'].append(data['id'])
    for i in retorno['ids']:
        pos = lt.isPresent(lst2,{'id': i})
        retorno['movies_names'].append(lt.getElement(lst2,pos)['original_title'])
        retorno['average'] += float(lt.getElement(lst2,pos)['vote_average'])
    try:
        size = len(retorno['movies_names'])
        movies = retorno['movies_names']
        average = round(retorno['average']/size,2)
    except:
        return -1

    t1_stop = process_time() #tiempo final
    print("Tiempo de ejecución ",t1_stop-t1_start," segundos ") 
    return (movies,average,size)

def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None 
    """

    lista1 = lt.newList("SINGLE_LINKED", conocerUnDirector) #Lista de Casting
    lista2 = lt.newList("SINGLE_LINKED", conocerUnDirector) #Lista de Detalles Movies
    while True:
        printMenu() #imprimir el menu de opciones en consola
        inputs =input('Seleccione una opción para continuar: \n') #leer opción ingresada
        if len(inputs)>0:
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
                        print('Opcion no valida: ')
                        print('')      

            elif int(inputs[0])==2: #opcion 2
                if lt.size(lista1) == 0 or lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    pass
            elif int(inputs[0])==3: #opcion 3
                if lt.size(lista1) == 0 or lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    name = input('Ingrese el nombre del director: ').lower().strip()
                    data = conocerUnDirector(lista1,lista2,name)
                    if data == -1:
                        print('No se encuentra el director')
                    else:
                        print('Nombre de las peliculas que ha dirigido ',name)
                        print(data[2])
                        for i in range(data[2]):
                            print(i+1,'. ',data[0][i])
                        print('Promedio de votación de las peliculas: ',data[1])
                        print('Para una cantidad de ',data[2],' peliculas')
                        input('Presione enter para continuar -------------------------->:')

            elif int(inputs[0])==4: #opcion 4
                if lt.size(lista1) == 0 or lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    pass
            elif int(inputs[0])==3: #opcion 5
                if lt.size(lista1) == 0 or lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    pass
            elif int(inputs[0])==4: #opcion 6
                if lt.size(lista1) == 0 or lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    pass
            elif int(inputs[0])==0: #opcion 0, salir
                sys.exit(0)
            else:
                print('Eliga una opcio  valida')
            
if __name__ == "__main__":
    main()