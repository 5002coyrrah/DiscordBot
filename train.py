import keras
import random
import numpy as np

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.backend import reshape
from keras.utils.np_utils import to_categorical

def initBoard():
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    return board

def movesToBoard(moves):
    board = initBoard()
    for move in moves:
        player = move[0]
        coords = move[1]
        board[coords[0]][coords[1]] = player
    return board

def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i, j))
    return moves

def getModel():
    numCells = 9
    outcomes = 3
    model = Sequential()
    model.add(Dense(200, activation='relu', input_shape=(9, )))
    model.add(Dropout(0.2))
    model.add(Dense(125, activation='relu'))
    model.add(Dense(75, activation='relu'))
    model.add(Dropout(0.1))
    model.add(Dense(25, activation='relu'))
    model.add(Dense(outcomes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    return model

def getWinner(board):
    candidate = 0
    won = 0
    
    # Check rows
    for i in range(len(board)):
        candidate = 0
        for j in range(len(board[i])):
            
            # Make sure there are no gaps
            if board[i][j] == 0:
                break
            
            # Identify the front-runner
            if candidate == 0:
                candidate = board[i][j]
            
            # Determine whether the front-runner has all the slots
            if candidate != board[i][j]:
                break
            elif j == len(board[i]) - 1:
                won = candidate
    
    if won > 0:
        return won
    
    # Check columns
    for j in range(len(board[0])):
        candidate = 0
        for i in range(len(board)):
            
            # Make sure there are no gaps
            if board[i][j] == 0:
                break
            
            # Identify the front-runner
            if candidate == 0:
                candidate = board[i][j]
            
            # Determine whether the front-runner has all the slots
            if candidate != board[i][j]:
                break
            elif i == len(board) - 1:
                won = candidate
    
    if won > 0:
        return won
    
    # Check diagonals
    candidate = 0
    for i in range(len(board)):
        if board[i][i] == 0:
            break
        if candidate == 0:
            candidate = board[i][i]
        if candidate != board[i][i]:
            break
        elif i == len(board) - 1:
            won = candidate
    
    if won > 0:
        return won
    
    candidate = 0
    for i in range(len(board)):
        if board[2 - i][2 - i] == 0:
            break
        if candidate == 0:
            candidate = board[2 - i][2 - i]
        if candidate != board[2 - i][2 - i]:
            break
        elif i == len(board) - 1:
            won = candidate
    
    if won > 0:
        return won
    
    # Still no winner?
    if (len(getMoves(board)) == 0):
        # It's a draw
        return 0
    else:
        # Still more moves to make
        return -1

def gamesToWinLossData(games):
    X = []
    y = []
    for game in games:
        winner = getWinner(movesToBoard(game))
        for move in range(len(game)):
            X.append(movesToBoard(game[:(move + 1)]))
            y.append(winner)

    X = np.array(X).reshape((-1, 9))
    y = to_categorical(y)
    
    # Return an appropriate train/test split
    trainNum = int(len(X) * 0.8)
    return (X[:trainNum], X[trainNum:], y[:trainNum], y[trainNum:])

def simulateGame(p1=None, p2=None, rnd=0):
    history = []
    board = initBoard()
    playerToMove = 1
    
    while getWinner(board) == -1:
        
        # Chose a move (random or use a player model if provided)
        move = None
        if playerToMove == 1 and p1 != None:
            move = bestMove(board, p1, playerToMove, rnd)
        elif playerToMove == 2 and p2 != None:
            move = bestMove(board, p2, playerToMove, rnd)
        else:
            moves = getMoves(board)
            move = moves[random.randint(0, len(moves) - 1)]
        
        # Make the move
        board[move[0]][move[1]] = playerToMove
        
        # Add the move to the history
        history.append((playerToMove, move))
        
        # Switch the active player
        playerToMove = 1 if playerToMove == 2 else 2
        print("Simuating Games Please Stand By.....")
        
    return history

print("Simulating Games .....")
games = [simulateGame() for _ in range(10000)]
print("Finished Simulating Games")

print("Begin Modle Compile")
print("Compiling Model .....")
model = getModel()
print("Model Compiled Successfully")
X_train, X_test, y_train, y_test = gamesToWinLossData(games)
print("Beginning Training")
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=100, batch_size=100)
print("Training Finished")
