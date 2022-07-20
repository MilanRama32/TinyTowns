''''
Calculates a players final score

inputs:
cards - array, set of cards corresponding to the buildings used. Order - (blue, red, green, orange, yellow, black, grey, pink)
board - 4x4 matrix Key:
        0: unfed cottage
        1: fed cottage
        2: Red Building
        3: Green Building
        4: Orange Building
        5: Yellow Building
        6: Black Building
        7: Grey Building
        8: Pink Building
'''


def scoreBoard(cards, board):
    
    score = 0
    score = scoreBlue(cards(1), board, score)
    score = scoreGreen(cards(2), board, score)
    
def scoreBlue(rcard, board, score):
    for i in range(4):
        for j in range(4):
            if board[i,j] == 2:
                board = rcard.feedBuildings(board, [i,j])
    for i in range(4):
        for j in range(4):
            if board[i, j] == 1:
                score = score + 3
    return score

def scoreGreen(gcard, board, score):
    count = 0
    for i in range(4):
        for j in range(4):
            if board[i,j] == 3:
                count = count + 1
    score = score + gcard.scoreSelf(count)
    return score