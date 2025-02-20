def rangs(graphe, matrice):
    r = [None] * len(graphe)
    # Nombre de predecesseurs
    d = [0] * len(graphe)
    for tache, details in graphe.items():
        d[tache] = len(details["predecesseurs"])

    k = 0
    S = {0: [0]}
    while None in r:
        S[k+1] = []
        for i in S[k]:
            r[i] = k
            for j in range (len(matrice[i])):
                if matrice[i][j] != '*':  
                    d[j] -= 1
                    if d[j] == 0: 
                        S[k + 1].append(j)
        k += 1
    return S,r

def date_au_plus_tot(graph, ordre):
    tot = [0] * (len(graph))
    for task in ordre:
        for pred in range(len(graph)):
            if graph[pred][task] != '*': 
                tot[task] = max(tot[task], tot[pred] + int(graph[pred][task]))
    return tot


def date_au_plus_tard(graph, duree_totale, ordre):
    o = ordre.reverse()
    latest = [duree_totale] * (len(graph))
    for task in ordre:  
        for succ in range(len(graph)):  
            if graph[task][succ] != '*':
                latest[task] = min(latest[task], latest[succ] - int(graph[task][succ]))
    return latest

def find_longest_critical_paths(graph, earliest, latest, num_tasks):
    """
    Finds the longest critical path(s) by summing task durations along each path.
    If multiple paths have the same maximum length, all are returned.
    """
    longest_paths = []
    max_duration = 0
    current_path = []

    def dfs(task, current_duration):
        nonlocal max_duration

        # Add the current task to the path
        current_path.append(task)

        # If we reach Omega (N+1), check if the path is critical and update the longest paths
        if task == num_tasks + 1:
            if all(latest[t] - earliest[t] == 0 for t in current_path):  # Check if it's a critical path
                if current_duration > max_duration:
                    longest_paths.clear()  # Clear previous longest paths
                    longest_paths.append(current_path[:])  # Add the new longest path
                    max_duration = current_duration  # Update max duration
                elif current_duration == max_duration:
                    longest_paths.append(current_path[:])  # Add path if it's equal to the max length
        else:
            # Explore all valid successors
            for succ in range(num_tasks + 2):
                if graph[task][succ] != '*':  # Valid connection
                    duration = int(graph[task][succ])
                    dfs(succ, current_duration + duration)

        # Backtrack: remove the current task to explore other branches
        current_path.pop()

    # Start DFS from Alpha (0)
    dfs(0, 0)
    return longest_paths

def calculate_free_margins(graph, earliest, num_tasks):
    """
    Calculates the free margin (marge libre) for all tasks.
    """
    free_margins = [float('inf')] * (num_tasks + 2)  # Initialize with infinity

    for task in range(num_tasks + 2):  # Iterate over all tasks
        for succ in range(num_tasks + 2):  # Check all successors
            if graph[task][succ] != '*':  # Valid connection
                duration = int(graph[task][succ])
                free_margin = earliest[succ] - earliest[task] - duration
                free_margins[task] = min(free_margins[task], free_margin)

        # If no successors, free margin is the total margin
        if free_margins[task] == float('inf'):
            free_margins[task] = 0  # Set to 0 if no successors (default behavior)

    return free_margins


def calendriers(matrice, graphe):
    e = rangs(graphe, matrice)[0].values()
    ordre = [item for sublist in e for item in sublist]
    
    tot = date_au_plus_tot(matrice, ordre)
    duree_totale = tot[-1]
    tard = date_au_plus_tard(matrice, duree_totale, ordre)

    marge_totale = [tard[i] - tot[i] for i in range(len(matrice))]
    marge_libre = calculate_free_margins(matrice, tot, len(matrice)-2)

    longest_critical_paths = find_longest_critical_paths(matrice, tot, tard, len(matrice)-2)
    
    print("\nCalendrier des tâches :")
    print("Rangs des sommets :", rangs(graphe, matrice)[1])
    print(f"Dates au plus tôt : {tot}")
    print(f"Dates au plus tard : {tard}")
    print(f"Marge Totale : {marge_totale}")
    print(f"Marge Libre : {marge_libre}")
    print(f"Chemin critique : {longest_critical_paths}")  # Critical path includes alpha and omega
    for path in longest_critical_paths:
        print(" -> ".join(map(str, path)))
