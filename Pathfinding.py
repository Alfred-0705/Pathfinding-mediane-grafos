import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from heapq import heappush, heappop
import random

# ===========================
# Crear grafo tipo grilla
# ===========================

G = nx.grid_2d_graph(5, 5)
scale = 2  # Para que los nodos estén más separados visualmente
pos = {n: (n[0] * scale, n[1] * scale) for n in G.nodes()}

# Asignar pesos aleatorios a cada arista
for u, v in G.edges():
    G[u][v]['weight'] = random.randint(1, 10)

# ===========================
# Algoritmo A*
# ===========================

def heuristic(a, b):
    """Distancia Manhattan entre dos nodos"""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def reconstruct_path(came_from, current):
    """Reconstruye el camino desde el nodo final"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def a_star(graph, start, goal):
    """Algoritmo A* para grafos ponderados"""
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    visited = set()

    while open_set:
        current = heappop(open_set)[1]

        if current == goal:
            return reconstruct_path(came_from, current)

        if current in visited:
            continue
        visited.add(current)

        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor].get('weight', 1)
            tentative_g = g_score[current] + weight
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                heappush(open_set, (f_score[neighbor], neighbor))
    return None

# ===========================
# Visualización
# ===========================

clicks = []

def draw_graph():
    """Dibuja el grafo con pesos"""
    ax.clear()
    nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=600, ax=ax)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
    plt.title("Haz clic en dos nodos para encontrar el camino más barato")
    plt.axis("equal")
    fig.canvas.draw_idle()

def draw_path(path):
    """Dibuja el camino resultante"""
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='lightblue', ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=2, ax=ax)

def get_nearest_node(x, y, threshold=1.0):
    """Devuelve el nodo más cercano al punto clickeado"""
    for node, (nx_, ny_) in pos.items():
        if abs(x - nx_) < threshold and abs(y - ny_) < threshold:
            return node
    return None

# ===========================
# Interacción con el usuario
# ===========================

def on_click(event):
    if event.inaxes != ax or event.xdata is None or event.ydata is None:
        return

    node = get_nearest_node(event.xdata, event.ydata)
    if node and node in G.nodes():
        if len(clicks) < 2:
            clicks.append(node)
            print(f"Seleccionado: {node}")
        else:
            print("Ya seleccionaste dos nodos. Presiona 'Reiniciar'.")

        if len(clicks) == 2:
            start, goal = clicks
            path = a_star(G, start, goal)
            draw_graph()
            if path:
                draw_path(path)
                plt.title(f"Camino de {start} a {goal}")
            else:
                plt.title("No se encontró camino")
            fig.canvas.draw_idle()

def reset(event):
    clicks.clear()
    draw_graph()

# ===========================
# Inicialización de la figura
# ===========================

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)

draw_graph()

# Botón de reinicio
ax_btn = plt.axes([0.4, 0.05, 0.2, 0.075])
btn = Button(ax_btn, 'Reiniciar')
btn.on_clicked(reset)

# Evento de clic
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()