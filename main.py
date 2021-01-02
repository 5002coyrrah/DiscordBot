import numpy as np
import discord
import random
import keras
from keras.utils.np_utils import to_categorical
from keras.models import Sequential
from keras.backend import reshape
from keras.layers import Dropout
from keras.layers import Dense

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
    model.load_weights('XOXO.hdf5')   
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['acc'])
    return model

model = getModel()

def initBoard():
    print("initBoard")
    board = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
    return board

def getMoves(board):
    moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                moves.append((i, j))
    return moves
def getWinner(board):
    #If this function outputs:
    #0 its a draw
    #1 Ai wins
    #2 Player Wins
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

def bestMove(board, model, player, rnd=0):
    scores = []
    moves = getMoves(board)
    
    # Make predictions for each possible move
    for i in range(len(moves)):
        future = np.array(board)
        future[moves[i][0]][moves[i][1]] = player
        prediction = model.predict(future.reshape((-1, 9)))[0]
        if player == 1:
            winPrediction = prediction[1]
            lossPrediction = prediction[2]
        else:
            winPrediction = prediction[2]
            lossPrediction = prediction[1]
        drawPrediction = prediction[0]
        if winPrediction - lossPrediction > 0:
            scores.append(winPrediction - lossPrediction)
        else:
            scores.append(drawPrediction - lossPrediction)

    # Choose the best move with a random factor
    bestMoves = np.flip(np.argsort(scores))
    for i in range(len(bestMoves)):
        if random.random() * rnd < 0.5:
            return moves[bestMoves[i]]

    # Choose a move completely at random
    return moves[random.randint(0, len(moves) - 1)]
 
    
client = discord.Client() #Create Conn With Discord

board = initBoard()

@client.event #Used To register Event
async def on_ready(): #Called When The bot is ready to be used
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message): #It triggers every time the bot recives a message
    async def printBoard(board):
        for i in range(len(board)):
            rowList = []
            for j in range(len(board[i])):
                mark = '    '
                if board[i][j] == 1:
                    mark = 'X '
                elif board[i][j] == 2:
                    mark = 'O '
                if (j == len(board[i]) - 1):
                    rowList.append(mark + "|") 
                else:
                    rowList.append(mark + "|")   
            if (i < len(board) - 1):
                rowList.append("-----")
                messagee = ' '.join(map(str, ["|", rowList[0], rowList[1], rowList[2]]))
                await message.channel.send(messagee)
            else:
                rowList.append("-----")
                messageee = ' '.join(map(str, ["|", rowList[0], rowList[1], rowList[2]]))
                await message.channel.send(messageee)
                
    async def iswin (board):
        winner = getWinner(board)
        if winner == 0:
            #Draw
            await message.channel.send("Draw")
            board[0][0] = 0
            board[0][1] = 0
            board[0][2] = 0
            board[1][0] = 0
            board[1][1] = 0
            board[1][2] = 0
            board[2][0] = 0
            board[2][1] = 0
            board[2][2] = 0
        elif winner == 1:
            #Ai Wins
            await message.channel.send("You Lose!")
            board[0][0] = 0
            board[0][1] = 0
            board[0][2] = 0
            board[1][0] = 0
            board[1][1] = 0
            board[1][2] = 0
            board[2][0] = 0
            board[2][1] = 0
            board[2][2] = 0
        elif winner == 2:
            #Player
            await message.channel.send("You Win!")
            board[0][0] = 0
            board[0][1] = 0
            board[0][2] = 0
            board[1][0] = 0
            board[1][1] = 0
            board[1][2] = 0
            board[2][0] = 0
            board[2][1] = 0
            board[2][2] = 0
        else:
            await printBoard(board)
            
    async def iswin1 (board):
        iswin = 0
        winner = getWinner(board)
        if winner == 0:
            #Draw
            await printBoard(board)
            await message.channel.send("Draw")
            iswin = 1
            board[0][0] = 0
            board[0][1] = 0
            board[0][2] = 0
            board[1][0] = 0
            board[1][1] = 0
            board[1][2] = 0
            board[2][0] = 0
            board[2][1] = 0
            board[2][2] = 0
        elif winner == 1:
            #Ai Wins
            await printBoard(board)
            await message.channel.send("'O' Loses!")
            iswin = 1
            board[0][0] = 0
            board[0][1] = 0
            board[0][2] = 0
            board[1][0] = 0
            board[1][1] = 0
            board[1][2] = 0
            board[2][0] = 0
            board[2][1] = 0
            board[2][2] = 0
        elif winner == 2:
            #Player
            await printBoard(board)
            await message.channel.send("'O' Wins!")
            iswin = 1
            board[0][0] = 0
            board[0][1] = 0
            board[0][2] = 0
            board[1][0] = 0
            board[1][1] = 0
            board[1][2] = 0
            board[2][0] = 0
            board[2][1] = 0
            board[2][2] = 0
        else:
            await printBoard(board)
        if iswin == 1:
            return 1
    
    if message.author == client.user:
        return

    if message.content.startswith('$hello'): #Check Message Content
        await message.channel.send('Hello!')
        
    if message.content.startswith('$XOXO'): #Check Message Content
        await message.channel.send("To Make Your Move:")
        await message.channel.send("Type in the coordinates of where you want to place your marker")
        await message.channel.send("This diagram shows the placement of coords, to send me your coordinates do it like this '$A1' Note the column is first then the row")
        await message.channel.send("To Begin the match just type '$Begin'")
        await message.channel.send("<>  A | B | C | \n 1  | \n 2 | \n 3 |") #Use \n for a line break
        
    if message.content.startswith('$Begin'):
        #Play game user against NN
        #1st move
        #Model Takes Their Move
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        getWinner(board)
        await printBoard(board)
        
            
    if message.content.startswith('$A1'):
        print("A1 Called")
        board[0][0] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
        
    if message.content.startswith('$A2'):
        print("A1 Called")
        board[1][0] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
        
    if message.content.startswith('$A3'):
        print("A1 Called")
        board[2][0] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
    
    if message.content.startswith('$B1'):
        print("A1 Called")
        board[0][1] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
        
    if message.content.startswith('$B2'):
        print("A1 Called")
        board[1][1] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)

    if message.content.startswith('$B3'):
        print("A1 Called")
        board[2][1] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
        
    if message.content.startswith('$C1'):
        print("A1 Called")
        board[0][2] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
        
    if message.content.startswith('$C2'):
        print("A1 Called")
        board[1][2] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
    
    if message.content.startswith('$C3'):
        print("A1 Called")
        board[2][2] = 2
        await iswin(board)
        move = bestMove(board, model, 1)
        board[move[0]][move[1]] = 1
        await iswin(board)
        
    if message.content.startswith('$Commands'):
        await message.channel.send("Here is a list of my commands")
        await message.channel.send("Tic Tac Toe:")
        await message.channel.send("$XOXO -- Start game")
        await message.channel.send("$ReleaseThe Ai -- Watch 2 Ai's Play Against Each Other \n \n")
        await message.channel.send("Note: If you have any feature requests:")
        await message.channel.send("Please Dm me @HarryOC493#5941")
        
    if message.content.startswith('$ReleaseTheAi'):
        p1 = model
        p2 = model
        rnd = 0.6
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
            iswin = await iswin1(board)
            await message.channel.send("-----")
            if iswin == 1:
                break

            # Add the move to the history
            history.append((playerToMove, move))

            # Switch the active player
            playerToMove = 1 if playerToMove == 2 else 2
        return history

client.run('123456xxxxxxx') --------------------------------------- Insert Bot Token Here ---------------------------------------


