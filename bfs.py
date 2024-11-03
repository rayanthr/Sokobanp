import collections
import copy 
import time

def bfs_solver(board):
	boxRobot = []
	wallsStorageSpaces = []
	possibleMoves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1]}

	maxRowLength = len(max(board, key=len))
	line = len(board)

	time_start = time.perf_counter()
	for i in range(line):
		boxRobot.append(['-'] * maxRowLength)
		wallsStorageSpaces.append(['-'] * maxRowLength)

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

	print("Solving using BFS\n")

	movesList = []
	visitedMoves = []

	queue = collections.deque([])
	source = [boxRobot, movesList]
	if boxRobot not in visitedMoves:
		visitedMoves.append(boxRobot)
	queue.append(source)

	completed = 0
	while queue and not completed:
		temp = queue.popleft()
		curPosition = temp[0]
		movesTillNow = temp[1]

		robot_x, robot_y = -1, -1
		for i in range(line):
			for j in range(maxRowLength):
				if curPosition[i][j] == 'R':
					robot_x, robot_y = i, j
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
					if curPositionCopy not in visitedMoves:
						matches = 0
						for k in range(line):
							for l in range(maxRowLength):
								if wallsStorageSpaces[k][l] == 'S' and curPositionCopy[k][l] != 'B':
									matches = 1
						movesTillNowCopy.append(key)
						if matches == 0:
							completed = 1
							solution_steps = len(movesTillNowCopy)
						else:
							queue.append([curPositionCopy, movesTillNowCopy])
							visitedMoves.append(curPositionCopy)
			elif wallsStorageSpaces[robotNew_x][robotNew_y] != 'O':
				curPositionCopy[robotNew_x][robotNew_y] = 'R'
				curPositionCopy[robot_x][robot_y] = ' '
				if curPositionCopy not in visitedMoves:
					movesTillNowCopy.append(key)
					queue.append([curPositionCopy, movesTillNowCopy])
					visitedMoves.append(curPositionCopy)

	if completed == 0:
		print("Can't make it")
	else:
		print(f"Solution found in {solution_steps} steps.")

	time_end = time.perf_counter()
	print("Run time: " + str(time_end - time_start))
	return movesTillNowCopy
