def read_task_constraints(fichier: str) -> dict:
    taches = {}

    try:
        with open(fichier, 'r') as file:
            for line in file:
                if line.strip():
                    parts = line.split()
                    tache = int(parts[0])  
                    duree = int(parts[1])  
                    predecesseurs = [int(p) for p in parts[2:]]  
                    taches[tache] = {"duree": duree, "predecesseurs": predecesseurs}
    except FileNotFoundError:
        print(f"Le fichier '{fichier}' est introuvable.")
        return None

    # Ajout du sommet fictif 0
    taches[0] = {"duree": 0, "predecesseurs": []}
    for tache in taches:
        if tache != 0 and not taches[tache]["predecesseurs"]:
            taches[tache]["predecesseurs"].append(0)

    # Ajout du sommet fictif n+1
    tache_finale = max(taches) + 1
    taches[tache_finale] = {"duree": 0, "predecesseurs": []}
    for tache in taches:
        if tache != tache_finale:
            is_successor = any(
                tache in taches[other]["predecesseurs"]
                for other in taches
                if other != tache_finale
            )
            if not is_successor:
                taches[tache_finale]["predecesseurs"].append(tache)

    return taches


def afficher_graphe(graphe: dict):
    for tache, details in sorted(graphe.items()):
        print(f"Tache {tache}: Durée = {details['duree']}, Predecessors = {details['predecesseurs']}")


def create_adjacency_matrix(graphe: dict):
    taches = sorted(graphe.keys())
    taille = len(taches)

    # Initialisation de la matrice avec des "*"
    matrice_adjacence = [['*' for _ in range(taille)] for _ in range(taille)]

    # Populate the matrix with task durations
    for tache, details in graphe.items():
        for predecesseur in details["predecesseurs"]:
            ligne = taches.index(predecesseur)
            colonne = taches.index(tache)
            matrice_adjacence[ligne][colonne] = str(graphe[predecesseur]["duree"])

    return matrice_adjacence, taches


def afficher_matrice(matrice, taches):
    # Entête du haut
    print("    ", end="")
    for tache in taches:
        print(f"{tache:>3} ", end="")
    print()

    for i, row in enumerate(matrice):
        print(f"{taches[i]:>3} ", end="") #Entête de gauche 
        for value in row:
            print(f"{value:>3} ", end="")
        print()
