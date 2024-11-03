
possibleMoves = {   'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}   # Déplacements possibles

def contains_deadlock_boxes(state, walls):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 'B':  # Si c'est une boîte
                blocked = True
                # Vérifie les directions pour voir si la boîte est bloquée
                for move in possibleMoves.values():  # Haut, Bas, Gauche, Droite
                    ni, nj = i + move[0], j + move[1]
                    if 0 <= ni < len(state) and 0 <= nj < len(state[i]):
                        # Si la case est vide ou un espace de stockage
                        if state[ni][nj] == ' ' or walls[ni][nj] == 'S':
                            blocked = False
                if blocked:
                    print(f"Deadlock détecté à la position ({i}, {j})")
                    return True  # Une boîte est bloquée
    return False 



# board =[
#             list("  OOOOOO "),
#             list("OOOSO  O "),
#             list("O    B OO"),
#             list("O B R  SO"),
#             list("OOO O OOO"),
#             list("  OBO O  "),
#             list("  O  SO  "),
#             list("  OOOOO  ")
#         ]

# board =[
#             list("  OOOOOO "),
#             list("OOO O  O "),
#             list("O      OO"),
#             list("O   S  SO"),
#             list("OOO O OOO"),
#             list("  O O O  "),
#             list("  O   O  "),
#             list("  OOOOO  ")
#         ]

# deadlock_detected = contains_deadlock_boxes(board, walls)
# print("Deadlock detected:", deadlock_detected)  # Doit afficher: True