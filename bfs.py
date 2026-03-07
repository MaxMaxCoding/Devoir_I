
import random
from maze import generate_maze_16, print_maze
from collections import deque
from time import perf_counter


# --- BFS avec suivi de trace ---
def bfs_with_trace(grid):
    n, m = len(grid), len(grid[0])
    S = G = None

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'S':
                S = (i, j)
            elif grid[i][j] == 'G':
                G = (i, j)

    if not S or not G:
        raise ValueError("S ou G manquant.")

    visited = [[False]*m for _ in range(n)]
    parent = {}
    exploration_order = []

    q = deque([S])
    visited[S[0]][S[1]] = True
    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    while q:
        r, c = q.popleft()
        exploration_order.append((r, c))

        if (r, c) == G:
            break

        #--- Pour DFS: on empile les voisins en (FIFO)
        #--- (Option: inverser l'ordre pour contrôler le chemin)
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m:
                if not visited[nr][nc] and grid[nr][nc] != '#':
                    visited[nr][nc] = True
                    parent[(nr, nc)] = (r, c)
                    q.append((nr, nc))

    #--- Reconstruction du chemin
    path = []
    if G in parent or G == S:
        cur = G
        path.append(cur)
        while cur != S:
            cur = parent[cur]
            path.append(cur)
        path.reverse()

    return exploration_order, path

#--- Trouver le point de depart S et d'arriver G ---
def find_positions(grid):
    S = G = None
    for i, row in enumerate(grid):
        for j, ch in enumerate(row):
            if ch == 'S':
                S = (i, j)
            elif ch == 'G':
                G = (i, j)
    if S is None or G is None:
        raise ValueError("Le labyrinthe doit contenir 'S' et 'G'.")
    return S, G

#--- Chemins explorés (cases marquées par P)
def display_exploration(grid, explored):
    display = [row[:] for row in grid]

    for (r, c) in explored:
        if display[r][c] not in ('S', 'G'):
            display[r][c] = 'p'

    for row in display:
        print(' '.join(row))

#--- Chemin solution (cases marquées par *) ---
GREEN = "\033[92m"  #--- Option couleur verte pour le chemin solution
RESET = "\033[0m"
def display_solution(grid, path):
    display = [row[:] for row in grid]

    for (r, c) in path:
        if display[r][c] not in ('S', 'G'):
            display[r][c] = '*'
    for row in display:
        print(' '.join(f"{GREEN}*{RESET}" if cell == '*' else cell for cell in row))

#--- Coordonnées du chemin solution sous forme: (S(1, 1) -> (2, 1) ->...->G(14, 14)) ---
def display_path_coordinates(path):
    formatted = "Chemin : "
    for i, (r, c) in enumerate(path):
        if i == 0:
            formatted += f"S({r}, {c})"
        elif i == len(path) - 1:
            formatted += f" -> G({r}, {c})"
        else:
            formatted += f" -> ({r}, {c})"
    print(formatted)

#--- BFS + métriques (noeuds, longueur, temps) ---
def bfs_with_metrics(grid):
    """
    Retourne:
      explored: liste des noeuds explorés (ordre BFS)
      path: liste des coordonnées du chemin (de S à G) 
      metrics: dict {nodes_explored, path_length, exec_time_ms}
    """
    start_time = perf_counter()

    n, m = len(grid), len(grid[0])
    S, G = find_positions(grid)

    visited = [[False]*m for _ in range(n)]
    parent = {}
    explored = []

    q = deque([S])  #--- 
    visited[S[0]][S[1]] = True

    moves = [(-1,0),(1,0),(0,-1),(0,1)]

    found = False
    while q:
        r, c = q.popleft()
        explored.append((r, c))

        if (r, c) == G:
            found = True
            break

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and not visited[nr][nc] and grid[nr][nc] != '#':
                visited[nr][nc] = True
                parent[(nr, nc)] = (r, c)
                q.append((nr, nc))

    #--- Reconstruire le chemin
    path = None
    if found:
        path = [G]
        cur = G
        while cur != S:
            cur = parent[cur]
            path.append(cur)
        path.reverse()

    exec_time_ms = (perf_counter() - start_time) * 1000.0   #--- Calcul du temps
    nodes_explored = len(explored)  #--- Nombre de pas ou noeuds exploré
    path_length = (len(path) - 1) if path else 0    #--- Nombre de pas ou de noeuds solution

    metrics = {
        "nodes_explored": nodes_explored,
        "path_length": path_length,
        "exec_time_ms": exec_time_ms
    }
    return explored, path, metrics

#--- Affichage des resultats DFS pour le tableau comparatif ---
def print_final_results(metrics):
    print(f"BFS \t\t\t\t\t {metrics['nodes_explored']} \t\t\t {metrics['path_length']} \t\t\t {metrics['exec_time_ms']:.3f} ms")
