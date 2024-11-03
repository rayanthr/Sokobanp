import collections
from queue import PriorityQueue
import copy
import time
from deadlock import contains_deadlock_boxes


def Astar_own(board):
    boxRobot = []
    wallsStorageSpaces = []
    possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}

    maxRowLength = len(max(board, key=len))
    lines = len(board)

    time_start = time.perf_counter()
    
    # Compteur d'étapes
    steps_count = 0

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

    print(storages)
    boxRobtDistance = 9999999
    boxes = []
    storagesLeft = len(storages)
    for i in range(lines):
        for j in range(maxRowLength):
            if boxRobot[i][j] == 'B':
                if wallsStorageSpaces[i][j] == 'S':
                    print(i, j)
                    storagesLeft -= 1
                boxes.append([i, j])
    print(storagesLeft)

    for i in range(lines):
        for j in range(maxRowLength):
            if boxRobot[i][j] == 'R':
                for k in boxes:
                    if boxRobtDistance > abs(k[0] - i) + abs(k[1] - j):
                        boxRobtDistance += abs(k[0] - i) + abs(k[1] - j)

    def manhattan(state):
        distance = 0
        for i in range(lines):
            for j in range(maxRowLength):
                if state[i][j] == 'B':
                    temp = 9999999
                    for storage in storages:
                        distanceToNearest = abs(storage[0] - i) + abs(storage[1] - j)
                        if temp > distanceToNearest:
                            temp = distanceToNearest
                    distance += temp
        return distance

    print("Solving using Astar 1\n")

    movesList = []
    visitedMoves = []

    queue = PriorityQueue()
    source = [boxRobot, movesList]
    if boxRobot not in visitedMoves:
        visitedMoves.append(boxRobot)
    queue.put((boxRobtDistance, source))

    robot_x = -1
    robot_y = -1
    completed = 0

    while not queue.empty() and completed == 0:
        temp = queue.get()
        curPosition = temp[1][0]
        movesTillNow = temp[1][1]
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
                if contains_deadlock_boxes(curPositionCopy, wallsStorageSpaces):
                    print("Deadlock trouvee")
                    continue 
                if curPositionCopy[boxNew_x][boxNew_y] == 'B' or wallsStorageSpaces[boxNew_x][boxNew_y] == 'O':
                    continue
                else:
                    curPositionCopy[boxNew_x][boxNew_y] = 'B'
                    curPositionCopy[robotNew_x][robotNew_y] = 'R'
                    curPositionCopy[robot_x][robot_y] = ' '
                    if contains_deadlock_boxes(curPositionCopy, wallsStorageSpaces):
                        print("Deadlock")
                        continue

                    if curPositionCopy not in visitedMoves:
                        matches = 0
                        for k in range(lines):
                            for l in range(maxRowLength):
                                if wallsStorageSpaces[k][l] == 'S':
                                    if curPositionCopy[k][l] != 'B':
                                        matches = 1
                        movesTillNowCopy.append(key)
                        steps_count += 1  # Incrémente le compteur d'étapes
                        
                        if matches == 0:
                            completed = 1
                            print(movesTillNowCopy)
                            print("Solution trouvée avec {} étapes".format(steps_count))
                        else:
                            boxRobtDistance = 999999
                            boxes = []
                            storagesLeft = len(storages)
                            for i in range(lines):
                                for j in range(maxRowLength):
                                    if curPositionCopy[i][j] == 'B':
                                        if wallsStorageSpaces[i][j] == 'S':
                                            storagesLeft -= 1
                                        boxes.append([i, j])

                            for i in range(lines):
                                for j in range(maxRowLength):
                                    if curPositionCopy[i][j] == 'R':
                                        for k in boxes:
                                            if boxRobtDistance > abs(k[0] - i) + abs(k[1] - j):
                                                boxRobtDistance = abs(k[0] - i) + abs(k[1] - j)

                            storagesLeft = 0
                            queue.put((manhattan(curPositionCopy) + boxRobtDistance + storagesLeft * 2 + stepsTillNow, [curPositionCopy, movesTillNowCopy]))
                            visitedMoves.append(curPositionCopy)
            else:
                if wallsStorageSpaces[robotNew_x][robotNew_y] == 'O' or curPositionCopy[robotNew_x][robotNew_y] != ' ':
                    continue
                else:
                    curPositionCopy[robotNew_x][robotNew_y] = 'R'
                    curPositionCopy[robot_x][robot_y] = ' '
                    
                    if curPositionCopy not in visitedMoves:
                        movesTillNowCopy.append(key)
                        steps_count += 1  # Incrémente le compteur d'étapes
                       
                        
                        boxRobtDistance = 999999
                        boxes = []
                        storagesLeft = len(storages)
                        for i in range(lines):
                            for j in range(maxRowLength):
                                if curPositionCopy[i][j] == 'B':
                                    if wallsStorageSpaces[i][j] == 'S':
                                        storagesLeft -= 1
                                    boxes.append([i, j])

                        for i in range(lines):
                            for j in range(maxRowLength):
                                if curPositionCopy[i][j] == 'R':
                                    for k in boxes:
                                        if boxRobtDistance > abs(k[0] - i) + abs(k[1] - j):
                                            boxRobtDistance = abs(k[0] - i) + abs(k[1] - j)
                        storagesLeft = 0
                        queue.put((manhattan(curPositionCopy) + boxRobtDistance + storagesLeft * 2 + stepsTillNow, [curPositionCopy, movesTillNowCopy]))
                        visitedMoves.append(curPositionCopy)

    if completed == 0:
        print("Can't make it")
        return []

    time_end = time.perf_counter()
    print("Run time: " + str(time_end - time_start))
    print("Nombre d'étapes: " + str(steps_count))  # Affiche le nombre d'étapes
    return movesTillNowCopy