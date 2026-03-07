# Import du module permettant de calculer le temps d'exécution 
from time import perf_counter


# --- DFS avec suivi de trace ---
def dfs_with_trace(grid):
    """
    Retourne:
      exploration_order: liste des noeuds explorés (ordre DFS)
      path: chemin trouvé (liste de coordonnées) ou [] si aucun chemin
    """
    n, m = len(grid), len(grid[0])
    S, G = find_positions(grid)

    visited = [[False] * m for _ in range(n)]
    parent = {}
    exploration_order = []

    stack = [S]
    visited[S[0]][S[1]] = True
    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    found = False

    while stack:
        r, c = stack.pop()
        exploration_order.append((r, c))

        if (r, c) == G:
            found = True
            break

        #--- Pour DFS: on empile les voisins en (LIFO)
        #--- (Option: inverser l'ordre pour contrôler le chemin)
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m:
                if not visited[nr][nc] and grid[nr][nc] != '#':
                    visited[nr][nc] = True
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))

    #--- Reconstruction du chemin
    path = []
    if found:
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

#--- Chemins exploré (cases marquées par P) ---
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

#--- DFS + métriques (noeuds, longueur, temps) ---
def dfs_with_metrics(grid):
    """
    Retourne:
      explored: liste les noeuds explorés (ordre DFS)
      path: liste les coordonnées du chemin (de S à G) 
      metrics: dict {nodes_explored, path_length, exec_time_ms}
    """
    start_time = perf_counter()

    n, m = len(grid), len(grid[0])
    S, G = find_positions(grid)

    visited = [[False] * m for _ in range(n)]
    parent = {}
    explored = []

    stack = [S]     #--- 
    visited[S[0]][S[1]] = True

    moves = [(-1,0), (1,0), (0,-1), (0,1)]

    found = False

    while stack:
        r, c = stack.pop()
        explored.append((r, c))

        if (r, c) == G:
            found = True
            break

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m:
                if not visited[nr][nc] and grid[nr][nc] != '#':
                    visited[nr][nc] = True
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))

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
    path_length = (len(path) - 1) if path else 0  # --- Nombre de pas ou de noeuds solution 

    metrics = {
        "nodes_explored": nodes_explored,
        "path_length": path_length,
        "exec_time_ms": exec_time_ms
    }
    return explored, path, metrics

# --- Affichage des resultats DFS pour le tableau comparatif ---
def print_final_results_dfs(metrics):
    print(f"DFS \t\t\t\t\t {metrics['nodes_explored']} \t\t\t {metrics['path_length']} \t\t\t {metrics['exec_time_ms']:.3f} ms")


