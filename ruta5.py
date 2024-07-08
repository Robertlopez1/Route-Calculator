import heapq
import random

# Definimos constantes para los tipos de terreno
CAMINO = 0
EDIFICIO = 1
AGUA = 2
BACHE = 3

# Solicitamos el número de filas y columnas al usuario
filas = int(input("Ingrese el número de filas: "))
columnas = int(input("Ingrese el número de columnas: "))

# Definimos la función para crear una matriz inicial vacía
def crear_matriz(filas, columnas):
    return [[CAMINO for _ in range(columnas)] for _ in range(filas)]

# Función para imprimir la matriz
def imprimir_matriz(matriz):
    simbolos = {CAMINO: '.', EDIFICIO: 'E', AGUA: 'A', BACHE: 'B', 'X': 'X'}
    for fila in matriz:
        for elemento in fila:
            print(simbolos[elemento], end=' ')
        print()

# Función para introducir obstáculos en el mapa
def introducir_obstaculos(mapa, tipo, cantidad):
    filas = len(mapa)
    columnas = len(mapa[0])
    for _ in range(cantidad):
        while True:
            fila = random.randint(0, filas - 1)
            columna = random.randint(0, columnas - 1)
            if mapa[fila][columna] == CAMINO:
                mapa[fila][columna] = tipo
                break

# Clase para representar un nodo en el algoritmo A*
class Nodo:
    def __init__(self, posicion, g=0, h=0, padre=None):
        self.posicion = posicion  # Asegurar que posicion es una tupla (fila, columna)
        self.g = g  # Costo desde el inicio
        self.h = h  # Costo heurístico al objetivo
        self.padre = padre
    
    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

# Función heurística (distancia Manhattan)
def heuristica(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Función para obtener los vecinos transitables
def obtener_vecinos(mapa, nodo):
    vecinos = []
    direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for direccion in direcciones:
        fila = nodo.posicion[0] + direccion[0]
        columna = nodo.posicion[1] + direccion[1]
        if 0 <= fila < len(mapa) and 0 <= columna < len(mapa[0]) and mapa[fila][columna] == CAMINO:
            vecinos.append(Nodo((fila, columna)))
    return vecinos

# Implementación del algoritmo A*
def a_estrella(mapa, inicio, fin):
    inicio_nodo = Nodo(inicio)
    fin_nodo = Nodo(fin)
    
    open_list = []
    closed_list = set()
    heapq.heappush(open_list, inicio_nodo)
    
    while open_list:
        nodo_actual = heapq.heappop(open_list)
        closed_list.add(nodo_actual.posicion)
        
        if nodo_actual.posicion == fin:
            camino = []
            while nodo_actual:
                camino.append(nodo_actual.posicion)
                nodo_actual = nodo_actual.padre
            return camino[::-1]
        
        vecinos = obtener_vecinos(mapa, nodo_actual)
        for vecino in vecinos:
            if vecino.posicion in closed_list:
                continue
            
            vecino.g = nodo_actual.g + 1
            vecino.h = heuristica(vecino.posicion, fin_nodo.posicion)
            vecino.padre = nodo_actual
            
            for nodo in open_list:
                if vecino.posicion == nodo.posicion and vecino.g > nodo.g:
                    break
            else:
                heapq.heappush(open_list, vecino)
    
    return None

# Generamos la matriz inicial
mapa = crear_matriz(filas, columnas)

# Imprimimos la matriz inicial
print("Mapa inicial:")
imprimir_matriz(mapa)

# Introducimos obstáculos en el mapa
tipo_obstaculo = int(input("Ingrese el tipo de obstáculo (1: Edificio, 2: Agua, 3: Bache): "))
cantidad_obstaculos = int(input("Ingrese la cantidad de obstáculos: "))
introducir_obstaculos(mapa, tipo_obstaculo, cantidad_obstaculos)

# Imprimimos la matriz con los obstáculos
print("Mapa con obstáculos:")
imprimir_matriz(mapa)

# Definimos el punto de inicio y fin
inicio = (0, 0)  # Esquina superior izquierda
fin = (filas - 1, columnas - 1)  # Esquina inferior derecha

print(f"Punto de inicio: {inicio}")
print(f"Punto de fin: {fin}")

# Ejecutamos el algoritmo A*
camino = a_estrella(mapa, inicio, fin)

# Imprimimos el camino encontrado en la matriz
if camino:
    for posicion in camino:
        if posicion != inicio and posicion != fin:
            mapa[posicion[0]][posicion[1]] = 'X'
    print("Mapa con el camino encontrado:")
    imprimir_matriz(mapa)
else:
    print("No se encontró un camino desde el inicio hasta el fin.")
