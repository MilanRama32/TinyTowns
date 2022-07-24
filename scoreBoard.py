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

        11: Warehouse with 1 resource
        12: Warehouse with 2 resources
        13: Warehouse with 3 resources
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
    positions = gcard.getPos(board)
    score = score + gcard.scoreSelf(positions)
    return score