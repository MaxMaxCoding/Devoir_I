# Import 
import random
from maze import generate_maze_16, print_maze
# Import des 3 fonctions de recherche
from dfs import (
    dfs_with_trace,
    dfs_with_metrics,
    print_final_results_dfs,
    display_exploration as dfs_display_exploration,
    display_solution as dfs_display_solution,
    display_path_coordinates as dfs_display_path_coordinates
)
from bfs import (
    bfs_with_trace,
    display_exploration,
    display_solution,
    display_path_coordinates,
    bfs_with_metrics,
    print_final_results
)
from astar import (
    astar_with_trace,
    astar_with_metrics,
    print_final_results_astar,
    display_exploration as astar_display_exploration,
    display_solution as astar_display_solution,
    display_path_coordinates as astar_display_path_coordinates
)

# Fonction main() qui regroupe toutes les autres pour une bonne execution 
def main():

    print("\n===== ALGORITHME DE RECHERCHE DU LABYRINTHE =====\n")
    # Seed aléatoire à chaque exécution
    seed = random.randrange(1_000_000_000)

    # Génération du labyrinthe
    maze = generate_maze_16(seed=seed, p_wall=0.35)
    #print(f"Seed utilisée : {seed}\n")
    print("\tLabyrinthe généré :")
    print("\t=================\n")
    print_maze(maze)

#--- AFFICHAGE
    explored_dfs, path_dfs = dfs_with_trace(maze)   #--- DFS
    explored, path = bfs_with_trace(maze)   #--- BFS
    explored_a, path_a = astar_with_trace(maze) #--- A*
                    #--- Resultats de l'agorithme DFS
    print("\n\t\t\t=== ============== ===")
    print("\t\t\t=== Algorithme DFS ===")
    print("\t\t\t=== ============== ===")
    #--- Chemin exploré
    print("\n=== Algorithme DFS EXPLORATION (p) === ===")
    dfs_display_exploration(maze, explored_dfs)
    # Chemin solution
    print("\n=== Algorithme DFS SOLUTION (*) ===")
    dfs_display_solution(maze, path_dfs)
    # Cordonnées chemin solution
    print("\n=== Algorithme DFS Coordonnées CHEMIN ===")
    dfs_display_path_coordinates(path_dfs)

                    #--- Resultats de l'agorithme BFS
    print("\n\t\t\t=== ============== ===")
    print("\t\t\t=== Algorithme BFS ===")
    print("\t\t\t=== ============== ===")
    #--- Chemin exploré
    print("\n=== Algorithme BFS EXPLORATION (p) ===")
    display_exploration(maze, explored)
    #--- Chemin solution
    print("\n=== Algorithme BFS SOLUTION (*) ===")
    display_solution(maze, path)
    #--- Cordonnées chemin solution
    print("\n=== Algorithme BFS Coordonnées CHEMIN ===")
    display_path_coordinates(path)

                   #--- Resultats de l'agorithme A* (Manhattan)
    print("\n\t\t\t=== ========================= ===")
    print("\t\t\t=== Algorithme A* (Manhattan) ===")
    print("\t\t\t=== ========================= ===")
    # Chemin exploré et solution
    print("\n=== Algorithme A* (Manhattan) EXPLORATION (p) === ===")
    astar_display_exploration(maze, explored_a)
     # Chemin solution
    print("\n=== Algorithme A* (Manhattan) SOLUTION (*) ===")
    astar_display_solution(maze, path_a)
    # Cordonnées chemin solution
    print("\n=== Algorithme A* (Manhattan) Coordonnées CHEMIN ===")
    astar_display_path_coordinates(path_a)

                    #--- Resultats tableau compartif
    print("\n\t\t\t\t\t===== ================== =====")
    print("\t\t\t\t\t===== TABLEAU COMPARATIF =====")
    print("\t\t\t\t\t===== ================== =====")
    print(f"ALGORITHME \t\t\t\tNOEUDS \t\t\tLONGUEUR \t\tTEMPS(ms)")
    #--- Exécution DFS + métriques
    explored_dfs, path_dfs, metrics_dfs = dfs_with_metrics(maze)
    print_final_results_dfs(metrics_dfs)
    #--- Exécution BFS + métriques
    explored, path, metrics = bfs_with_metrics(maze)
    print_final_results(metrics)
    #--- Exécution A* (Manhattan) + métriques
    explored_a, path_a, metrics_a = astar_with_metrics(maze)
    print_final_results_astar(metrics_a)

    #--- OPTIONNEL METTRE EN EVIDENCE L'ALGORITHME OPTIMAL (COUT=TEMPS)
    print("-" *145)
    print("\n\t\t\t\t\t OPTIMISATION COUTS")
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    min_temps = min(metrics["exec_time_ms"], metrics_dfs["exec_time_ms"], metrics_a["exec_time_ms"])
    algo_min_temps = min(metrics["exec_time_ms"], metrics_dfs["exec_time_ms"], metrics_a["exec_time_ms"])
    max_temps = max(metrics["exec_time_ms"], metrics_dfs["exec_time_ms"], metrics_a["exec_time_ms"])
    print(f"TEMPS OPTIMAL \t\t\t\t\t\t\t {GREEN}{min_temps:.3f}{RESET}")
    print(f"TEMPS NON OPTIMAL \t\t\t\t\t\t {RED}{max_temps:.3f}{RESET}")

    print()

if __name__ == "__main__":
    main()