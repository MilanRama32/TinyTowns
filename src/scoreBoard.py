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

class Board:

    def __init__(self, cards):
        self.grid = [[Cell() for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                if j < 3:
                    self.grid[i][j].setRight(self.grid[i][j+1])
                if i < 3:
                    self.grid[i][j].setDown(self.grid[i+1][j])
        self.score = self.scoreBoard()
    
    def scoreBoard(self):
        return sum(self.grid[i][j].score for i in range(4) for j in range(4))
    


class Cell:
    def __init__(self):
        self.building = None
        self.resource = None
        self.left = None
        self.right = None
        self.up = None
        self.down = None
        self.score = -1
        
 
    def setRight(self, cell):
        self.right = cell
        cell.left = self
    def setDown(self, cell):
        self.down = cell
        cell.up = self
    
    def countNeighbors(self, buildingTypes):
        count = 0
        for neighbor in [self.left, self.right, self.up, self.down]:
            if neighbor and neighbor.building in buildingTypes:
                count += 1
        return count

    def addResource(self, resource):
        self.resource = resource
    def removeResource(self):
        self.resource = None
    def placeBuilding(self, building):
        self.building = building
        self.score = building.card.score
    def removeBuilding(self):
        self.building = None
        self.score = -1



def scoreBoard(cards, board, landmark=None):
    
    # initialize score list
    scores = [0]

    # blue card scoring
    scores[0], board = scoreBlue(board, cards)

    # other card scoring
    for card in cards[2:]:
        scores.append(scoreCard(card, board))

    if landmark is not None:
        scores.append(scoreCard(landmark, board))
    else:
        scores.append(0)

    # empty spaces negative points
    scores.append(0)
    for i in range(4):
        for j in range(4):
            if board[i,j]==-1:
                scores[-1] -= 1
    return scores
    
def scoreBlue(board, cards):
    rcard = cards[1]
    score = 0
    rPositions = rcard.getPos(board)
    board = rcard.feedBuildings(board, rPositions, cards)
    for i in range(4):
        for j in range(4):
            if board[i, j] == 1:
                score = score + 3
    return score, board

def scoreCard(card, board):
    positions = card.getPos(board)
    score = card.scoreSelf(positions, board)
    return score