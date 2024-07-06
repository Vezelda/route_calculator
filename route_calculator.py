import random
import heapq

# Costos de terreno
costos = {
    'C': 1,  # Carreteras
    'E': float('infinity'),  # Edificios
    'A': 5,  # Agua
    'B': 7,  # Áreas bloqueadas temporalmente
}

# Función heurística (distancia Manhattan)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Algoritmo A* para una matriz
def a_star(mapa, start, end):
    filas, columnas = len(mapa), len(mapa[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Movimientos posibles (arriba, abajo, izquierda, derecha)
            neighbor = (x + dx, y + dy)
            if 0 <= neighbor[0] < filas and 0 <= neighbor[1] < columnas:
                terreno = mapa[neighbor[0]][neighbor[1]]
                if terreno != 'E':  # Ignorar edificios
                    tentative_g_score = g_score[current] + costos[terreno]
                    if tentative_g_score < g_score.get(neighbor, float('infinity')):
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end)
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return []

# Función para generar una matriz aleatoria con más caminos libres
def generar_matriz_aleatoria(filas, columnas):
    return [[random.choices(['C', 'E', 'A', 'B'], weights=[0.6, 0.1, 0.2, 0.1])[0] for _ in range(columnas)] for _ in range(filas)]

# Preguntar el tamaño de la matriz
def preguntar_tamano_matriz():
    while True:
        try:
            filas = int(input("Introduce el número de filas: "))
            columnas = int(input("Introduce el número de columnas: "))
            if filas > 0 and columnas > 0:
                return filas, columnas
            else:
                print("El número de filas y columnas debe ser mayor que 0.")
        except ValueError:
            print("Por favor, introduce números válidos.")

# Preguntar las coordenadas de inicio y fin
def preguntar_coordenadas(filas, columnas, tipo):
    while True:
        try:
            x = int(input(f"Introduce la coordenada x de {tipo} (0-{filas-1}): "))
            y = int(input(f"Introduce la coordenada y de {tipo} (0-{columnas-1}): "))
            if 0 <= x < filas and 0 <= y < columnas:
                return x, y
            else:
                print("Las coordenadas deben estar dentro del rango del mapa.")
        except ValueError:
            print("Por favor, introduce números válidos.")

# Función para agregar obstáculos en el mapa
def agregar_obstaculos(mapa):
    while True:
        try:
            num_obstaculos = int(input("Introduce el número de obstáculos que deseas agregar: "))
            for i in range(num_obstaculos):
                print(f"Agregando obstáculo {i+1} de {num_obstaculos}")
                tipo_obstaculo = input("Introduce el tipo de obstáculo ('E' para edificio, 'A' para agua, 'B' para bloqueo): ").upper()
                if tipo_obstaculo not in ('E', 'A', 'B'):
                    print("Tipo de obstáculo no válido. Intenta nuevamente.")
                    continue
                x, y = preguntar_coordenadas(len(mapa), len(mapa[0]), f"obstáculo {i+1}")
                mapa[x][y] = tipo_obstaculo
            break
        except ValueError:
            print("Por favor, introduce un número válido.")
    return mapa

# Función para imprimir el mapa con el camino recorrido
def imprimir_mapa_con_camino(mapa, path, start, end):
    mapa_con_camino = [fila[:] for fila in mapa]  # Hacer una copia del mapa
    for x, y in path:
        mapa_con_camino[x][y] = '*'
    
    mapa_con_camino[start[0]][start[1]] = 'S'  # Marcar el inicio
    mapa_con_camino[end[0]][end[1]] = 'F'  # Marcar el fin

    for fila in mapa_con_camino:
        print(' '.join(fila))

def main():
    # Ejecutar el programa
    filas, columnas = preguntar_tamano_matriz()
    mapa = generar_matriz_aleatoria(filas, columnas)

    print("Mapa generado:")
    for fila in mapa:
        print(' '.join(fila))

    # Preguntar las coordenadas de inicio y fin
    start = preguntar_coordenadas(filas, columnas, "inicio")
    end = preguntar_coordenadas(filas, columnas, "fin")

    # Agregar obstáculos al mapa
    mapa = agregar_obstaculos(mapa)

    print("Mapa con obstáculos:")
    for fila in mapa:
        print(' '.join(fila))

    # Verificar que el inicio y el fin sean transitables
    if mapa[start[0]][start[1]] in ('E', 'B') or mapa[end[0]][end[1]] in ('E', 'B'):
        print("El punto de inicio o fin está bloqueado.")
    else:
        # Ejecutar el algoritmo A*
        path = a_star(mapa, start, end)
        if path:
            print("Ruta más corta:", path)
            print("Mapa con el camino recorrido:")
            imprimir_mapa_con_camino(mapa, path, start, end)
        else:
            print("No se encontró una ruta desde el inicio hasta el fin.")

if __name__ == "__main__":
    main()
