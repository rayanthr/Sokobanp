import time
import copy
import collections
from bfs import *  # Ensure your BFS implementation is correct
import pygame
import os
from Astar_manhattan import Astar_man
from Astar_OwnHeuristic import Astar_own
from deadlock import contains_deadlock_boxes

# Possible moves for the robot
possibleMoves = {'U': [0,-1 ], 'R': [1, 0], 'D': [0, 1], 'L': [-1, 0]}


def print_board(board):
    for row in board:
        print("".join(row))
    print("\n" + "-" * 20 + "\n")


def determine_walls_storage_spaces(board):
    max_length = max(len(row) for row in board)  # Get the maximum row length
    walls_storage_spaces = []
    
    for row in board:
        # Create a new row with appropriate length
        new_row = []
        for cell in row:
            if cell in ('O', 'S'):  # Walls ('O') and Storage Spaces ('S')
                new_row.append(cell)
            else:  # Empty spaces and boxes should be treated as empty in this context
                new_row.append(' ')
        # Fill the row to the max length
        new_row += [' '] * (max_length - len(new_row))  
        walls_storage_spaces.append(new_row)
    
    return walls_storage_spaces


def display_board(screen,board,skin):
    w = skin.get_width() / 4  # Largeur de chaque case
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == 'O':  # Mur
                screen.blit(skin, (col_idx*w, row_idx*w), (0,2*w,w,w))
            elif cell == ' ':  # Espace vide
                screen.blit(skin, (col_idx*w, row_idx*w), (0,0,w,w))
            elif cell == 'R':  # Robot
                screen.blit(skin, (col_idx*w, row_idx*w), (w,0,w,w))
            elif cell == 'B':  # Boîte
                screen.blit(skin, (col_idx*w, row_idx*w), (2*w,0,w,w))
            elif cell == 'S':  # Zone de stockage
                screen.blit(skin, (col_idx*w, row_idx*w), (0,w,w,w))
    pygame.display.flip()



   

def find_robot_position(board):
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == 'R':
                return (row_idx, col_idx)
    return None  

def animate_solution(screen, board, moves, initial_pos, skin):

    robot_y, robot_x = initial_pos

   
    # board[robot_y][robot_x] = 'R'  # Place le robot à la position initiale
    
    for move in moves:
        dx, dy = possibleMoves[move]
        new_robot_x, new_robot_y = robot_x + dx, robot_y + dy

        if not (0 <= new_robot_y < len(board) and 0 <= new_robot_x < len(board[0])):
            print(f"Déplacement hors limites détecté : ({new_robot_x}, {new_robot_y})")
            break

        if board[new_robot_y][new_robot_x] in [' ', 'S']:
            board[new_robot_y][new_robot_x] = 'R'
            board[robot_y][robot_x] = ' '
            
        elif board[new_robot_y][new_robot_x] == 'B':
            box_new_x, box_new_y = new_robot_x + dx, new_robot_y + dy
            if board[box_new_y][box_new_x] in [' ', 'S']:
                board[box_new_y][box_new_x] = 'B'
                board[new_robot_y][new_robot_x] = 'R'
                board[robot_y][robot_x] = ' '
            else:
                print(f"Impossible de déplacer la boîte à ({box_new_x}, {box_new_y})")
                break 
        elif board[new_robot_y][new_robot_x] == 'O':    
            print(f"Impossible de déplacer le robot à ({new_robot_x}, {new_robot_y})")
            break
        else:
            print(f"Impossible de déplacer le robot à ({new_robot_x}, {new_robot_y})")
            break
 
        display_board(screen,board,skin)
        pygame.time.delay(115)

        robot_x, robot_y = new_robot_x, new_robot_y

           





def main():
    # Define your initial board configuration
    board = [
    list("OOOO"),
    list("  OOS O"),
    list("OOO R OOOO"),
    list("OS BBBB SO"),
    list("OOOO   OOO"),
    list("   O S O"),
    list("   OOOOO")
]


    
   
    
    
    
    
    print("Initial Board Configuration:")
    print_board(board)

    # Menu for selecting algorithm
    print("Select an algorithm:")
    print("1. BFS")
    print("2. A* with Manhattan heuristic")
    print("3. A* with custom heuristic")
    
    choice = input("Enter the number of your choice: ") 
    pygame.init()
    screen = pygame.display.set_mode((400, 350),pygame.NOFRAME)
    pygame.display.set_caption("Sokoban Game")
    skinfilename = os.path.join('borgar.png')
    try:
        skin = pygame.image.load(skinfilename)
    except pygame.error:
        print('Cannot load skin')
        raise SystemExit
    skin = skin.convert()
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))
   
    
   
    # Run the chosen algorithm
    if choice == '1':
        moves_list = bfs_solver(board)
    elif choice == '2':
        moves_list = Astar_man(board)  # Replace with your actual A* Manhattan function
    elif choice == '3':
        moves_list = Astar_own(board)  # Replace with your actual A* custom function
    else:
        print("Invalid choice.")
        pygame.quit()
        return
    
    
    
    for event in pygame.event.get():
        if moves_list:
            print("REUSSI Moves List:", moves_list)
            animate_solution(screen, board, moves_list, find_robot_position(board), skin)   
        else:
            print("Can't make it")
            
        pygame.display.flip()  # Update display
    pygame.quit()
        
if __name__ == "__main__":
    main()