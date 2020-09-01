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
from DataStructures import arraylist as a
from Sorting import insertionsort as iss
from Sorting import selectionsort as sss
from Sorting import quicksort as qs
from Sorting import mergesort as ms
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
        if dato['genres'].lower().strip()==criteria.lower().strip():
            lt.addLast(lista,dato)
    if lt.size(lista) > 0:
        retorno = lista.copy()
    else:
        retorno = -1
    return retorno

def crear_ranking(lst,function):
    iterador=it.newIterator(lst)
    lista = lt.newList()
    while it.hasNext(iterador)==True:
        dato = it.next(iterador)
        lt.addLast(lista,dato)
    if lt.size(lista) > 0:
        ms.mergesort(lista,function)
        return lista
    else:
        return -1

def compareRecordVotes (recordA, recordB):
    return int(recordA['vote_count']) > int(recordB['vote_count'])

def compareRecordAverage (recordA, recordB):
    return float(recordA['vote_average']) > float(recordB['vote_average'])

def compareRecordIds (recordA, recordB):
    if int(recordA['id']) == int(recordB['id']):
        return 0
    elif int(recordA['id']) > int(recordB['id']):
        return 1
    return -1
    
def loadCSVFile (file, cmpfunction,type):
    lst=lt.newList(type, cmpfunction)
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

def loadMovies (file,type):
    lst = loadCSVFile(file,compareRecordIds,type) 
    print("Datos cargados, " + str(lt.size(lst)) + " elementos cargados")
    return lst

def menu_cargar():
    print('Menu de opciones: ')
    print('1. Cargar Archivos Pequeños')
    print('2. Cargar Archivos Grandes')

def conocerUnDirector(lst1, lst2, name):
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
    return (movies,average,size)

def conocer_un_actor(lista1,lista2,name):
    retorno = {'ids':[],'movies_names':[], 'average':0.0, 'director_name':[]}
    it_list1 = it.newIterator(lista1)
    mayor = ""
    res = 0
    while it.hasNext(it_list1) == True:
        data = it.next(it_list1)
        for i in range(1,6):
            if data['actor'+str(i)+'_name'].lower().strip()==name:
                retorno['ids'].append(data["id"])
                retorno["director_name"].append(data["director_name"])
    for i in retorno['ids']:
        pos = lt.isPresent(lista2,{'id': i})
        retorno['movies_names'].append(lt.getElement(lista2,pos)['original_title'])
        retorno['average'] += float(lt.getElement(lista2,pos)['vote_average'])
    for i in retorno['director_name']:
        if retorno['director_name'].count(i) > res:
            res = retorno['director_name'].count(i)
            mayor = i
    if len(retorno['ids']) > 0:
        return (retorno['movies_names'],round(retorno['average']/len(retorno['ids']),2),mayor)
    else:
        return -1

def entender_genero(lista,genre):
    lst = filtrar_por_genero(lista,genre)
    i = 0
    iterador = it.newIterator(lst)
    while it.hasNext(iterador) == True:
        dato = it.next(iterador)
        i += float(dato["vote_count"])
    if lt.size(lst) > 0:
        promedio = round(i / lt.size(lst),2)
        return (lst, promedio)
    else:
        return -1

def longitudRanking():
    try:
        x = int(input('Digite la longitud del ranking: '))
    except:
        print('¡Digite un NÚMERO ENTERO!')
        x = int(input('Digite la longitud del ranking: '))
    while x < 10:
        print('Eliga un valor valido mayor o igual a 10...')
        x = int(input('Digite la longitud del ranking: '))
    return x

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
        inputs = input('Seleccione una opción para continuar: \n') #leer opción ingresada
        if len(inputs)>0:
            if int(inputs)==1: #opcion 1
                continuar = True
                while continuar == True:
                    menu_cargar()
                    opcion = input('Digite su opción: ')
                    t1_start = process_time() #tiempo inicial
                    if opcion == '1':
                        lista1 = loadMovies('Data/themoviesdb/MoviesCastingRaw-small.csv','SINGLE_LINKED')
                        lista2 = loadMovies('Data/themoviesdb/SmallMoviesDetailsCleaned.csv','SINGLE_LINKED')
                        lista2_a = loadMovies('Data/themoviesdb/SmallMoviesDetailsCleaned.csv','ARRAY_LIST')
                        continuar = False
                    elif opcion == '2':
                        lista1 = loadMovies('Data/themoviesdb/AllMoviesCastingRaw.csv','SINGLE_LINKED')
                        lista2 = loadMovies('Data/themoviesdb/AllMoviesDetailsCleaned.csv','SINGLE_LINKED')
                        lista2_a = loadMovies('Data/themoviesdb/AllMoviesDetailsCleaned.csv','ARRAY_LIST')
                        continuar = False
                    else:
                        print('Opcion no valida: ')
                        print('')
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")       

            elif int(inputs)==2: #opcion 2
                if lt.size(lista1) == 0 or lt.size(lista2_a) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    t1_start = process_time() #tiempo inicial
                    x = longitudRanking() + 1
                    lst = lista2_a.copy()
                    data1 = crear_ranking(lst,compareRecordVotes)
                    print('El ranking por votos es:')
                    for i in range(1,x):
                        print(i,'- ',lt.getElement(data1,i)['original_title'],lt.getElement(data1,i)['vote_count'])    
                    data2 = crear_ranking(lst,compareRecordAverage)
                    input('Digite enter para ver el siguiente ranking ---------->:')
                    print('El ranking por promedio es:')
                    for i in range(1,x):
                        print(i,'- ',lt.getElement(data2,i)['original_title'],lt.getElement(data2,i)['vote_average'])
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")       
                    
            elif int(inputs)==3: #opcion 3
                if lt.size(lista1) == 0 or lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    t1_start = process_time() #tiempo inicial
                    name = input('Ingrese el nombre del director: ').lower().strip()
                    data = conocerUnDirector(lista1,lista2,name)
                    if data == -1:
                        print('No se encuentra el director')
                    else:
                        print('Nombre de las peliculas que ha dirigido ',name)
                        for i in range(data[2]):
                            print(i+1,'- ',data[0][i])
                        print("El director ha dirigido ",data[2]," películas")
                        print('Promedio de votación de las peliculas: ',data[1])
                        input('Presione enter para continuar -------------------------->:')
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")       

            elif int(inputs)==4: #opcion 4
                if lt.size(lista1) == 0 or lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    t1_start = process_time() #tiempo inicial
                    name = str(input("Digita el nombre del actor a buscar: ")).lower().strip()
                    data = conocer_un_actor(lista1, lista2, name)
                    if data == -1:
                        print("¿Ese actor existe? ")
                    else:
                        print(name.title()," ha actuado en las siguientes películas: ")
                        for i in range(0,len(data[0])):
                            print(i+1,'- ',data[0][i])
                        print("El actor ha actuado en ",len(data[0])," películas")
                        print("El promedio de las películas actuadas por",name.title()," es de ",data[1])
                        print("El director con el que ha hecho más colaboraciones es ",data[2])
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")       


            elif int(inputs)==5: #opcion 5
                if lt.size(lista2) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    t1_start = process_time() #tiempo inicial
                    genre = str(input("Ditgita el género que deseas buscar: ")).lower().strip()
                    data = entender_genero(lista2,genre)
                    if data == -1:
                        print("Asegurate de haber escrito bien el género")
                    else:
                        print("Se han encontrado estas péliculas con el género " ,genre,": ")
                        for i in range(1,(lt.size(data[0])) + 1):
                            print(i,'- ',lt.getElement(data[0],i)['original_title'])
                        print("Se encontraron ", lt.size(data[0]), " péliculas")
                        print("El promedio de votación es de " ,data[1])
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")

            elif int(inputs)==6: #opcion 6
                if lt.size(lista1) == 0 or lt.size(lista2_a) == 0:
                    print('¡Debe cargar los archivos primero!')
                else:
                    t1_start = process_time() #tiempo inicial
                    x = longitudRanking() + 1
                    y = input('Digite el genero a filtrar: ')
                    lst = filtrar_por_genero(lista2_a,y)
                    data = [crear_ranking(lst,compareRecordVotes),crear_ranking(lst,compareRecordAverage)]
                    if data[0] == -1 or data[1] == -1:
                        print('El genero no existe')
                    else:
                        print('El ranking por votos para el genero ',y,' es:')
                        for i in range(1,x):
                            print(i,'- ',lt.getElement(data[0],i)['original_title'],lt.getElement(data[0],i)['vote_count'])    
                        input('Digite enter para ver el siguiente ranking ---------->:')
                        print('El ranking por promedio para el genero ',y,' es:')
                        for i in range(1,x):
                            print(i,'- ',lt.getElement(data[1],i)['original_title'],lt.getElement(data[1],i)['vote_average'])
                    t1_stop = process_time() #tiempo final
                    print("Tiempo de ejecución ",t1_stop-t1_start," segundos ")
            
            elif int(inputs)==0: #opcion 0, salir
                sys.exit(0)
            else:
                print('Eliga una opción  valida')
            
if __name__ == "__main__":
    main()