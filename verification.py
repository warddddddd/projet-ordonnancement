def a_cycle(matrice):
    # Initialize reachability matrix based on connections in the graph
    reachability = [[1 if matrice[i][j] != '*' else 0 for j in range(len(matrice))] for i in range(len(matrice))]

    # Apply Roy-Warshall algorithm to calculate reachability
    taille = len(matrice)
    for k in range(taille):
        for i in range(taille):
            for j in range(taille):
                if reachability[i][k] and reachability[k][j]:
                    reachability[i][j] = 1

    # Check for cycles (self-loops in reachability matrix)
    for i in range(taille):
        if reachability[i][i] == 1:  # A self-loop indicates a cycle
            print(f"Circuit détecté au sommet {i}")
            return True

    print("Aucun circuit détecté.")
    return False

def a_arete_negative(graphe):
    for _, details in graphe.items():
        if details["duree"] < 0:
            return True
    return False
