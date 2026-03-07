# Import du module permettant la génération de nombres aléatoires
import random


#--- Générateur du labyrinthe avec les positions entre les murs de manière aléatoire ---
def generate_maze_16(seed: None, p_wall: float = 0.35) -> list[list[str]]:
    """
    Génère un labyrinthe 16x16 avec :
    - bords en murs '#'
    - S en (1,1)
    - G en (14,14)
    - murs internes aléatoires
    - chemin garanti entre S et G
    - reproductible via seed
    """
    rng = random.Random(seed)
    n = 16
    S = (1, 1)
    G = (14, 14)

    #--- Base: tout murs, puis intérieur en passages
    grid = [['#' for _ in range(n)] for _ in range(n)]
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            grid[i][j] = '.'

    #--- Protéger un chemin garanti entre S et G
    protected = set()
    r, c = S
    protected.add((r, c))

    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    #--- Marche “guidée” : favorise la descente/droite mais autorise des détours
    while (r, c) != G:
        candidates = []
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r + dr, c + dc
            if 1 <= nr <= 14 and 1 <= nc <= 14:
                candidates.append((nr, nc))

        #--- Pondération: préférer les moves qui rapprochent de G
        current_dist = manhattan((r, c), G)
        better = [p for p in candidates if manhattan(p, G) < current_dist]
        same_or_worse = [p for p in candidates if manhattan(p, G) >= current_dist]

        #--- Choix: la plupart du temps on progresse, parfois on fait un détour
        if better and rng.random() < 0.85:
            nr, nc = rng.choice(better)
        else:
            nr, nc = rng.choice(candidates)

        r, c = nr, nc
        protected.add((r, c))

    #--- Ajouter des murs aléatoires internes, sans casser le chemin protégé
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            if (i, j) in protected or (i, j) == S or (i, j) == G:
                continue
            if rng.random() < p_wall:
                grid[i][j] = '#'

    #--- Bords extérieurs = murs (de manière renforcé)
    for i in range(n):
        grid[0][i] = '#'
        grid[n-1][i] = '#'
        grid[i][0] = '#'
        grid[i][n-1] = '#'

    #--- Placer S et G
    grid[S[0]][S[1]] = 'S'
    grid[G[0]][G[1]] = 'G'
    return grid

#--- Labyrinthe généré ---
def print_maze(grid: list[list[str]]) -> None:
    for row in grid:
        print(' '.join(row))

