
# TODO: 
# Greenhouse
# change feeding to be friendly for temple
# pink cards


class Card(object):
    
    def __init__(self, c, n, p, pCondition, e, num):
        self.buildingColour = c
        self.Name = n
        self.points = p
        self.pointCondition = pCondition
        self.effect = e
        self.boardNum = num
        
    def getPos(self, board):
        positions = []
        for i in range(4):
            for j in range(4):
                if self.boardNum == 11 and (board[i,j]==12 or board[i,j]==13):
                    positions.append([i,j])
                elif board[i,j] == self.boardNum:
                    positions.append([i,j])
        return positions

    def findAdjacent(self, pos, board):
        adj = []
        if pos[0] > 0:
            adj.append(board[pos[0]-1, pos[1]])
        if pos[0] < 3:
            adj.append(board[pos[0]+1, pos[1]])
        if pos[1] > 0:
            adj.append(board[pos[0], pos[1]-1])
        if pos[1] < 3:
            adj.append(board[pos[0], pos[1]+1])
        return adj
    
        
class Cottage(Card):
    def __init__(self):
        super().__init__(c = "Blue", n = "Cottage", p = 3, pCondition = "Fed", e = None, num = 0)
  
#Red cards      
class Farm(Card):
    
    def __init__(self):
        super().__init__(c = "Red", n = "Farm", p = 0, pCondition = "None", e = "Feed 4", num = 2)
        
    def feedBuildings(self, board, pos):
        count = 0
        for i in range(4):
            for j in range(4):
                if board[i,j] == 0:
                    board[i,j] = 1
                    count = count + 1
                    if count == 4:
                        break
            if count == 4:
                break
        return board

class Greenhouse(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Greenhouse", p = 0, pCondition = "None", e = "Feeds 1 Contiguous Group", num = 2)
        
    def feedBuildings(self, board, pos):
        pass
class Grainary(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Grainary", p = 0, pCondition = "None", e = "Feeds surrounding", num = 2)
        
    def feedBuildings(self, board, pos):
        for i in range(max(0, pos[0]-1), min(4, pos[0]+2)):
            for j in range(max(0, pos[1]-1), min(4, pos[1]+2)):
                if board[i,j] == 0:
                    board[i,j] = 1
        return board

class Orchard(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Orchard", p = 0, pCondition = "None", e = "Feeds row and column", num = 2)
        
    def feedBuildings(self, board, pos):
        for i in range(4):
            if board[pos[0], i] == 0:
                board[pos[0], i] = 1
            if board[i, pos[1]] == 0:
                board[i, pos[1]] = 1
        return board

#Green Cards

class Almshouse(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Almshouse", p = [-1,5,-3,15,-5,26], pCondition = "Number in Town", e = "None", num = 3)
        
    def scoreSelf(self, positions, board):
        count = len(positions)
        return self.points[min(count-1, 5)]

class Tavern(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Tavern", p = [2,5,9,14,20], pCondition = "Number in Town", e = "None", num = 3)
    
    def scoreSelf(self, positions, board):
        count = len(positions)
        return self.points[min(count-1, 4)]
    
class Inn(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Inn", p = 3, pCondition = "Not in row/col as another", e = "None", num = 3)
    
    def scoreSelf(self, positions, board):
        rowsUsed, colsUsed, rowsDuped, colsDuped = [],[],[],[]
        for pos in positions:
            if pos[0] in rowsUsed:
                rowsDuped[rowsUsed.index(pos[0])] = 0
                rowsDuped.append(0)
            else:
                rowsDuped.append(1)
                rowsUsed.append(pos[0])
            if pos[1] in colsUsed:
                colsDuped[colsUsed.index(pos[1])] = 0
                colsDuped.append(0)
            else:
                colsDuped.append(1)
                colsUsed.append(pos[1])
        score = 3* sum(rowsDuped and colsDuped)
        return score
    
class FeastHall(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Tavern", p = 2, pCondition = "+1 if you have more than the person on your right", e = "None", num = 3)
    
    def scoreSelf(self, positions, board):
        return 2*len(positions)

#Orange Cards
class Abbey(Card):
    def __init__(self):
        super().__init__(c = "Orange", n = "Abbey", p = 3, pCondition = "Not adjacent to Black, Green or Yellow", e = "None", num = 4)

    def scoreSelf(self, positions, board):
        score = 0
        for pos in positions:
            adj = self.findAdjacent(pos, board)
            if (adj.count(3) + adj.count(5) + adj.count(6)) == 0:
                score += 3
        return score
            
class Chapel(Card):
    def __init__(self):
        super().__init__(c = "Orange", n = "Chapel", p = 1, pCondition = "1 per fed cottage", e = "None", num = 4)

    def scoreSelf(self, positions, board):
        score = 0
        for i in range(4):
            for j in range(4):
                if board[i,j] == 1:
                    score += len(positions)
        return score

class Cloister(Card):
    def __init__(self):
        super().__init__(c = "Orange", n = "Cloister", p = 1, pCondition = "1 per Cloister in a corner", e = "None", num = 4)

    def scoreSelf(self, positions, board):
        scorePer = 0
        for pos in positions:
            if (pos[0] == 0 or pos[0] == 3) and (pos[1] == 0 or pos[1] == 3):
                scorePer += 1
        score = scorePer * len(positions)
        return score

class Temple(Card):
    def __init__(self):
        super().__init__(c = "Orange", n = "Temple", p = 4, pCondition = "Adjacent to 2 fed cottages", e = "None", num = 4)

    def scoreSelf(self, postitions, board):
        for pos in postitions:
            adjs = self.findAdjacent(pos, board)
            fedCottageCount = 0
            for adji in adjs:
                if adji == 1:
                    fedCottageCount += 1
            if fedCottageCount >= 2:
                score += 4
        return score

            

#Yellow Cards
class Bakery(Card):
    def __init__(self):
        super().__init__(c = "Yellow", n = "Bakery", p = 3, pCondition = "Adjacent to Black or Red", e = "None", num = 5)

    def scoreSelf(self, positions, board):
        score = 0
        for pos in positions:
            adj = self.findAdjacent(pos, board)
            if adj.count(2) + adj.count(6) > 0:
                score += 3
        return score

class Market(Card):
    def __init__(self):
        super().__init__(c = "Yellow", n = "Market", p = 1, pCondition = "1 Per Market in same row or column but not both", e = "None", num = 5)

    def scoreSelf(self, positions, board):
        score = 0
        for pos in positions:
            inRow, inCol = 0, 0
            for i in range(4):
                if board[pos[0], i] == 5:
                    inRow += 1
                if board[i, pos[1]] == 5:
                    inCol += 1
            score += max(inRow, inCol)
        return score

class Tailor(Card):
    def __init__(self):
        super().__init__(c = "Yellow", n = "Tailor", p = 1, pCondition = "1 point + 1 extra Per Tailor in one of the center 4 squares", e = "None", num = 5)

    def scoreSelf(self, positions, board):
        scorePer = 1
        for pos in positions:
            if (pos[0] == 1 or pos[0] == 2) and (pos[1] == 1 or pos[1] == 2):
                scorePer += 1
        score = scorePer * len(positions)
        return score
        
class Theatre(Card):
    def __init__(self):
        super().__init__(c = "Yellow", n = "Theatre", p = 1, pCondition = "1 point per other unique building type in the same row and column", e = "None", num = 5)

    def scoreSelf(self, positions, board):
        for i in range(4):
            for j in range(4):
                if board[i,j] == 0:
                    board[i,j] = 1
                elif board[i,j] == 12 or board[i,j] == 13:
                    board[i,j] = 11
        score = 0
        for pos in positions:
            rowColBuildings = []
            for i in range(4):
                if i != pos[0] and board[i, pos[1]] != -1:
                    rowColBuildings.append(board[i, pos[1]])
                if i != pos[1] and board[pos[0], i] != -1:
                    rowColBuildings.append(board[pos[0], i])
            score += len(set(rowColBuildings))
        return score

#Black Cards
class Bank(Card):
    def __init__(self):
        super().__init__(c = "Black", n = "Bank", p = 4, pCondition = None, e = "Can't place resource placed ontop of this building", num = 6)

    def scoreSelf(self, positions, board):
        score = 4 * len(positions)
        return score

class Factory(Card):
    def __init__(self):
        super().__init__(c = "Black", n = "Factory", p = 0, pCondition = None, e = "When the resource on this building is called, player may instead place another resource", num = 6)

    def scoreSelf(self, positions, board):
        score = 0
        return score
        
class TradingPost(Card):
    def __init__(self):
        super().__init__(c = "Black", n = "Bank", p = 1, pCondition = None, e = "Treat as wild resource", num = 6)

    def scoreSelf(self, positions, board):
        score = len(positions)
        return score

class Warehouse(Card):
    def __init__(self):
        super().__init__(c = "Black", n = "Warehouse", p = -1, pCondition = "-1 point per resource stored here", e = "Can store resource or swap resource from here instead of placing it.", num = 11)

    def scoreSelf(self, positions, board):
        score = 0
        for pos in positions:
            score += -1 * board[pos[0], pos[1]] + 10
        return score

#Grey Cards
class Fountain(Card):
    def __init__(self):
        super().__init__(c = "Grey", n = "Fountain", p = 2, pCondition = "Adjacent to Grey", e = None, num = 7)
        
    def scoreSelf(self, positions, board):
        score = 0
        for pos in positions:
            adj = self.findAdjacent(pos, board)
            if adj.count(7) > 0:
                score += 2
        return score

class Millstone(Card):
    def __init__(self):
        super().__init__(c = "Grey", n = "Millstone", p = 2, pCondition = "Adjacent to red or Yellow", e = None, num = 7)
        
    def scoreSelf(self, positions, board):
        score = 0
        for pos in positions:
            adj = self.findAdjacent(pos, board)
            if adj.count(2) + adj.count(5) > 0:
                score += 2
        return score

class Shed(Card):
    def __init__(self):
        super().__init__(c = "Grey", n = "Shed", p = 1, pCondition = "None", e = "Can be placed anywhere in town", num = 7)
        
    def scoreSelf(self, positions, board):
        score = len(positions)
        return score

class Well(Card):
    def __init__(self):
        super().__init__(c = "Grey", n = "Well", p = 1, pCondition = "1 per adjacent Cottage", e = None, num = 7)
        
    def scoreSelf(self, positions, board):
        score = 0
        for pos in positions:
            adjs = self.findAdjacent(pos, board)
            for adji in adjs:
                if adji == 0 or adji == 1:
                    score += 1
        return score
