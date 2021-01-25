import math

#Basado en el código del usuario adrigm (Razón Artificial)
#http://razonartificial.com/2010/03/pathfinding-a-en-python-parte-i/

class Nodo:
    def __init__(self, atributos=[0, "A", 0, 0], padre=None):
        self.indice = int(atributos[0])
        self.id = atributos[1]
        self.pos = [float(atributos[2]), float(atributos[3])]
        self.padre = padre
        self.h = distancia(self.pos, coordenadas(id_final))

        if self.padre == None:
            self.g = 0
        else:
            self.g = self.padre.g + matriz_adyacencia[self.indice - 1][self.padre.indice - 1]
        self.f = self.g + self.h


class AEstrella:
    def __init__(self, id_inicio, id_final):
        # self.mapa = mapa

        # Nodos de inicio y fin.
        self.inicio = Nodo(buscarPos(id_inicio))
        self.fin = Nodo(buscarPos(id_final))

        # Crea las listas abierta y cerrada.
        self.abierta = []
        self.cerrada = []

        # Añade el nodo inicial a la lista cerrada.
        self.cerrada.append(self.inicio)

        # Añade vecinos a la lista abierta
        self.abierta += self.vecinos(self.inicio)

        # Buscar mientras objetivo no este en la lista cerrada.
        while self.objetivo():
            self.buscar()

        self.costoTotal = 0
        self.camino = self.camino()

    # Devuelve una lista con los nodos vecinos transitables.
    def vecinos(self, nodo):
        vecinos = []
        for col in range(len(matriz_adyacencia)):
            if(matriz_adyacencia[nodo.indice - 1][col] > 0):
                vecinos.append(Nodo(lista_vertices[col], nodo))
        return vecinos

    # Pasa el elemento de f menor de la lista abierta a la cerrada.
    def f_menor(self):
        menor = self.abierta[0]
        indice_menor = 0
        for i in range(1, len(self.abierta)):
            if self.abierta[i].f < menor.f:
                menor = self.abierta[i]
                indice_menor = i
        self.cerrada.append(self.abierta[indice_menor])
        del self.abierta[indice_menor]

    # Comprueba si un nodo está en una lista.
    def en_lista(self, nodo, lista):
        for i in range(len(lista)):
            if nodo.pos == lista[i].pos:
                return 1
        return 0

    # Gestiona los vecinos del nodo seleccionado.
    def ruta(self):
        for i in range(len(self.nodos)):
            if self.en_lista(self.nodos[i], self.cerrada):
                continue
            elif not self.en_lista(self.nodos[i], self.abierta):
                self.abierta.append(self.nodos[i])
            else:
                if self.select.g + matriz_adyacencia[self.select.indice - 1][self.nodos[i].indice-1] < self.nodos[i].g:
                    for j in range(len(self.abierta)):
                        if self.nodos[i].pos == self.abierta[j].pos:
                            del self.abierta[j]
                            self.abierta.append(self.nodos[i])
                            break

    # Analiza el último elemento de la lista cerrada.
    def buscar(self):
        self.f_menor()
        self.select = self.cerrada[-1]
        self.nodos = self.vecinos(self.select)
        self.ruta()

    # Comprueba si el objetivo está en la lista abierta.
    def objetivo(self):
        for i in range(len(self.abierta)):
            if self.fin.pos == self.abierta[i].pos:
                return 0
        return 1

    # Retorna una lista con las posiciones del camino a seguir.
    def camino(self):
        for i in range(len(self.abierta)):
            if self.fin.pos == self.abierta[i].pos:
                objetivo = self.abierta[i]

        self.costoTotal = objetivo.g
        camino = []
        while objetivo.padre != None:
            camino.append(objetivo.id)
            objetivo = objetivo.padre
        camino.append(self.inicio.id)
        camino.reverse()
        return camino


# Funciones --------------

#Busca la posicion de un nodo específico y devielve un vector con los atributos:
#indice, id, coordenada x, coordenada y en caso de que exista
def buscarPos(id):
    for fila in lista_vertices:
        if fila[1] == id:
            return fila
    return None

#Busca las coordenadas x,y de un nodo específico
def coordenadas(id):
    atributos = buscarPos(id)
    if atributos is None:
        return None
    else:
        return [float(atributos[2]), float(atributos[3])]

#Mide la distancia entre dos nodos
def distancia(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)


# Crea una matriz con los vertices del grafo
def leer_vertices():
    matriz_vertices = []
    matriz_coordenadas = leer_coordenadas()
    for i in range(len(matriz_coordenadas)):
        matriz_vertices.append(matriz_coordenadas[i])
    return matriz_vertices

#Lee el archivo con las coordenadas de los nodos y los ingresa en una matriz de 4 columnas
#con los datos: índice, id, coordenada x, coordenada y
def leer_coordenadas(archivo="coordenadas.txt"):
    matriz_coordenadas = open(archivo, "r")
    matriz_coordenadas = matriz_coordenadas.readlines()
    matriz_coordenadas = quitarUltimo(matriz_coordenadas)
    for i in range(len(matriz_coordenadas)):
        matriz_coordenadas[i] = matriz_coordenadas[i].split(",")
    return matriz_coordenadas


# Lee el archivo de enlaces y lo ingresa en dos listas ligadas a modo de matriz (matriz de adyacencia)
def leerEnlaces(archivo="enlaces.txt"):
    matrizAdyacencia = open(archivo, "r")
    matrizAdyacencia = matrizAdyacencia.readlines()
    matrizAdyacencia = quitarUltimo(matrizAdyacencia)
    for i in range(len(matrizAdyacencia)):
        matrizAdyacencia[i] = cadenaAFloatList(matrizAdyacencia[i])
    return matrizAdyacencia


# Convierte una cadena de texto a una lista de floats
def cadenaAFloatList(cadena):
    lista = []
    strList = cadena.split("\t")
    for i in strList:
        lista.append(float(i))
    return lista


# Quita el ultimo caracter de una lista.
def quitarUltimo(lista):
    for i in range(len(lista) - 1):
        lista[i] = lista[i][:-1]
    return lista


lista_vertices = leer_vertices()
matriz_adyacencia = leerEnlaces()
id_inicio = "A"
id_final = "W"

def main():
    print("----- ALGORITMO A* ------")
    global id_inicio
    global id_final
    while True:
        while True:
            print("Ingrese el nombre del nodo inicial (Ej: A)")
            id_inicio = input().upper()
            print("Ingrese el nombre del nodo final (Ej: w)")
            id_final = input().upper()
            if(buscarPos(id_inicio) and buscarPos(id_final)) is not None:
                break;
            else:
                print("Al menos uno de los nodos ingresados no existe. Por favor vuelva a ingresar los datos")

        algoritmo = AEstrella(id_inicio, id_final)
        print("A continuación se muestra el camino óptimo y el costo de la ruta entre ambos nodos:\n")
        print(algoritmo.camino)
        print("Costo: " + str(algoritmo.costoTotal))
        print("\nSi desea ingresar dos nuevos nodos escriba 1, de lo contrario, el programa se cerrará.")
        if input() != "1":
            break
    return 0

if __name__ == '__main__':
	main()