from heapq import heappush, heappop
from time import perf_counter


# --- Heuristique Manhattan ---
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# --- A* avec suivi de trace ---
def astar_with_trace(grid):
    """
    Retourne:
      exploration_order: liste des noeuds explorés (ordre A*: noeuds extraits du tas)
      path: chemin trouvé (liste de coordonnées) ou [] si aucun chemin
    """
    n, m = len(grid), len(grid[0])
    S, G = find_positions(grid)

    # g_score = coût réel depuis S
    INF = 10**9
    g_score = [[INF] * m for _ in range(n)]
    g_score[S[0]][S[1]] = 0

    # Closed = noeuds définitivement traités (sortis du tas)
    closed = [[False] * m for _ in range(n)]

    parent = {}
    exploration_order = []

    # Tas de priorité: (f = g + h, g, (r,c))
    heap = []
    heappush(heap, (manhattan(S, G), 0, S))

    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    found = False

    while heap:
        f, g, (r, c) = heappop(heap)

        #--- Si déjà fermé, on ignore (doublons possibles dans le tas)
        if closed[r][c]:
            continue

        closed[r][c] = True
        exploration_order.append((r, c))

        #--- Objectif atteint
        if (r, c) == G:
            found = True
            break

        #--- Explorer les voisins
        for dr, dc in moves:
            nr, nc = r + dr, c + dc

            #--- Vérifier les bornes
            if not (0 <= nr < n and 0 <= nc < m):
                continue

            #--- Ignorer les murs
            if grid[nr][nc] == '#':
                continue

            #--- Si déjà fermé, ignorer
            if closed[nr][nc]:
                continue

            tentative_g = g_score[r][c] + 1

            #--- Mise à jour si on trouve un meilleur chemin vers (nr,nc)
            if tentative_g < g_score[nr][nc]:
                g_score[nr][nc] = tentative_g
                parent[(nr, nc)] = (r, c)
                h = manhattan((nr, nc), G)
                heappush(heap, (tentative_g + h, tentative_g, (nr, nc)))

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

# --- A* + métriques (noeuds, longueur, temps) ---
def astar_with_metrics(grid):
    """
    Retourne:
      explored: liste des noeuds explorés (ordre A*: noeuds extraits du tas)
      path: liste des coordonnées du chemin (S..G) ou None si pas trouvé
      metrics: dict {nodes_explored, path_length, exec_time_ms}
    """
    start_time = perf_counter()
    n, m = len(grid), len(grid[0])
    S, G = find_positions(grid)

    INF = 10**9
    g_score = [[INF] * m for _ in range(n)]
    g_score[S[0]][S[1]] = 0

    closed = [[False] * m for _ in range(n)]
    parent = {}
    explored = []

    heap = []
    heappush(heap, (manhattan(S, G), 0, S))

    moves = [(-1,0), (1,0), (0,-1), (0,1)]
    found = False

    while heap:
        f, g, (r, c) = heappop(heap)

        if closed[r][c]:
            continue

        closed[r][c] = True
        explored.append((r, c))

        if (r, c) == G:
            found = True
            break

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n and 0 <= nc < m):
                continue
            if grid[nr][nc] == '#':
                continue
            if closed[nr][nc]:
                continue

            tentative_g = g_score[r][c] + 1
            if tentative_g < g_score[nr][nc]:
                g_score[nr][nc] = tentative_g
                parent[(nr, nc)] = (r, c)
                heappush(heap, (tentative_g + manhattan((nr, nc), G), tentative_g, (nr, nc)))

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

#--- Affichage des resultats A* pour le tableau comparatif ---
def print_final_results_astar(metrics):
    print(f"A* (Manhattan) \t\t\t\t {metrics['nodes_explored']} \t\t\t {metrics['path_length']} \t\t\t {metrics['exec_time_ms']:.3f} ms")

