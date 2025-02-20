from graph import read_task_constraints, create_adjacency_matrix, afficher_matrice
from verification import a_cycle, a_arete_negative
from scheduling import calendriers

def main():
    while True:
        fichier = input("Entrez le chemin du fichier contenant les contraintes (ex: tests/test.txt) : ").strip()

        # Lecture des contraintes et stockage en mémoire
        graphe = read_task_constraints(fichier)
        if not graphe:
            print("Erreur : Impossible de lire les contraintes des tâches.")
            return

        # Création de la matrice de valeurs
        matrice, taches = create_adjacency_matrix(graphe)

        # Affichage de la matrice
        print("\nMatrice d'adjacence :")
        afficher_matrice(matrice, taches)


        # Verifications des conditions d'ordonnancement
        if a_arete_negative(graphe):
            print("Le graphe contient une arête à valuer négative. L'ordonnancement n'est pas possible.")
            return
        if a_cycle(matrice):
            print("Le graphe contient un circuit. L'ordonnancement n'est pas possible.")
            return
        
        print("Le graphe ne contient ni circuits ni arêtes négatives . Calcul des calendriers en cours...")
             
        # Calcule et affichage des calendriers, des marges et des chemins critiques
        calendriers(matrice, graphe)

        print("\nOrdonnancement terminé avec succès!")
        recommencer = input("Voulez vous tester un nouveau tableau de contraintes? (y/n)")
        if recommencer == 'n':
            break

if __name__ == "__main__":
    main()
