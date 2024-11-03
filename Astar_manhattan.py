import collections
import copy
import time
from queue import PriorityQueue


def Astar_man(board):
    
    boxRobot = []
    wallsStorageSpaces = []
    possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}

    maxRowLength = len(max(board, key=len))
    lines = len(board)

    time_start = time.perf_counter()

    for i in range(lines):
        boxRobot.append([])
        wallsStorageSpaces.append([])
        for j in range(maxRowLength):
            boxRobot[-1].append('-')
            wallsStorageSpaces[-1].append('-')

    for i in range(len(board)):
        if len(board[i]) < maxRowLength:
            board[i] += 'O' * (maxRowLength - len(board[i]))

    for i in range(len(board)):
        for j in range(maxRowLength):
            if board[i][j] == 'B' or board[i][j] == 'R':
                boxRobot[i][j] = board[i][j]
                wallsStorageSpaces[i][j] = ' '
            elif board[i][j] == 'S' or board[i][j] == 'O':
                wallsStorageSpaces[i][j] = board[i][j]
                boxRobot[i][j] = ' '
            elif board[i][j] == ' ':
                boxRobot[i][j] = ' '
                wallsStorageSpaces[i][j] = ' '
            elif board[i][j] == '*':
                boxRobot[i][j] = 'B'
                wallsStorageSpaces[i][j] = 'S'
            elif board[i][j] == '.':
                boxRobot[i][j] = 'R'
                wallsStorageSpaces[i][j] = 'S'

    storages = []
    for i in range(lines):
        for j in range(maxRowLength):
            if wallsStorageSpaces[i][j] == 'S':
                storages.append([i, j])

    def manhattan(state):
        distance = 0
        for i in range(lines):
            for j in range(maxRowLength):
                if state[i][j] == 'B':
                    temp = float('inf')
                    for storage in storages:
                        distanceToNearest = abs(storage[0] - i) + abs(storage[1] - j)
                        if temp > distanceToNearest:
                            temp = distanceToNearest
                    distance += temp
        return distance

    print("Solving using A* with Manhattan as heuristic\n")

    movesList = []
    visitedMoves = set()  # Using a set for fast look-up of visited positions

    queue = PriorityQueue()
    source = (manhattan(boxRobot), boxRobot, movesList)

    if tuple(map(tuple, boxRobot)) not in visitedMoves:
        visitedMoves.add(tuple(map(tuple, boxRobot)))
    queue.put(source)

    robot_x = -1
    robot_y = -1
    completed = 0

    while not queue.empty() and completed == 0:
        _, curPosition, movesTillNow = queue.get()
        stepsTillNow = len(movesTillNow)
        
        for i in range(lines):
            for j in range(maxRowLength):
                if curPosition[i][j] == 'R':
                    robot_y = j
                    robot_x = i
                    break
            else:
                continue
            break

        for key in possibleMoves:
            robotNew_x = robot_x + possibleMoves[key][0]
            robotNew_y = robot_y + possibleMoves[key][1]
            curPositionCopy = copy.deepcopy(curPosition)
            movesTillNowCopy = copy.deepcopy(movesTillNow)

            if curPositionCopy[robotNew_x][robotNew_y] == 'B':
                boxNew_x = robotNew_x + possibleMoves[key][0]
                boxNew_y = robotNew_y + possibleMoves[key][1]
                if curPositionCopy[boxNew_x][boxNew_y] == 'B' or wallsStorageSpaces[boxNew_x][boxNew_y] == 'O':
                    continue
                else:
                    curPositionCopy[boxNew_x][boxNew_y] = 'B'
                    curPositionCopy[robotNew_x][robotNew_y] = 'R'
                    curPositionCopy[robot_x][robot_y] = ' '
                    if tuple(map(tuple, curPositionCopy)) not in visitedMoves:
                        matches = 0
                        for k in range(lines):
                            for l in range(maxRowLength):
                                if wallsStorageSpaces[k][l] == 'S' and curPositionCopy[k][l] != 'B':
                                    matches = 1
                        movesTillNowCopy.append(key)
                        if matches == 0:
                            completed = 1
                            print("Solution found with moves:", movesTillNowCopy)
                        else:
                            queue.put((manhattan(curPositionCopy) + stepsTillNow, curPositionCopy, movesTillNowCopy))
                            visitedMoves.add(tuple(map(tuple, curPositionCopy)))
            else:
                if wallsStorageSpaces[robotNew_x][robotNew_y] == 'O' or curPositionCopy[robotNew_x][robotNew_y] != ' ':
                    continue
                else:
                    curPositionCopy[robotNew_x][robotNew_y] = 'R'
                    curPositionCopy[robot_x][robot_y] = ' '
                    if tuple(map(tuple, curPositionCopy)) not in visitedMoves:
                        movesTillNowCopy.append(key)
                        queue.put((manhattan(curPositionCopy) + stepsTillNow, curPositionCopy, movesTillNowCopy))
                        visitedMoves.add(tuple(map(tuple, curPositionCopy)))

    if completed == 0:
        print("Can't make it")
        return []

    time_end = time.perf_counter()
    print("Run time: " + str(time_end - time_start))
    
    # Display the number of steps
    total_steps = len(movesTillNowCopy)
    print(f"Total steps taken: {total_steps}")
    
    return movesTillNowCopy