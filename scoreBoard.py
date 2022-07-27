''''
Calculates a players final score

inputs:
cards - array, set of cards corresponding to the buildings used. Order - (blue, red, green, orange, yellow, black, grey, pink)
board - 4x4 matrix Key:
        -1: no building
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
    score, board = scoreBlue(cards[1], board, score, cards)
    for card in cards[2:]:
        score = scoreCard(card, board, score)
    for i in range(4):
        for j in range(4):
            if board[i,j]==-1:
                score -= 1
    return score
    
def scoreBlue(rcard, board, score, cards):
    rPositions = rcard.getPos(board)
    board = rcard.feedBuildings(board, rPositions, cards)
    for i in range(4):
        for j in range(4):
            if board[i, j] == 1:
                score = score + 3
    return score, board

def scoreCard(card, board, score):
    positions = card.getPos(board)
    score = score + card.scoreSelf(positions, board)
    return score


