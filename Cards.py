from operator import index


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
                if board[i,j] == self.pos:
                    positions.append([i,j])
        return positions
    
        
class Cottage(Card):
    def __init__(self):
        super.__init__(c = "Blue", n = "Cottage", p = 3, pCondition = "Fed", e = None, num = 0)
  
#Red cards      
class Farm(Card):
    
    def __init__(self):
        super().__init__(c = "Red", n = "Farm", p = 0, pCondition = "None", e = "Feed 4", num = 2)
        
    def feedBuildings(board, pos):
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
        
    def feedBuildings(board, pos):
        pass
class Grainary(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Grainary", p = 0, pCondition = "None", e = "Feeds surrounding", num = 2)
        
    def feedBuildings(board, pos):
        for i in range(max(0, pos[0]-1), min(4, pos[0]+1)):
            for j in range(max(0, pos[1]-1), min(4, pos[1]+1)):
                if board[i,j] == 0:
                    board[i,j] = 1
        return board

class Orchard(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Orchard", p = 0, pCondition = "None", e = "Feeds row and column", num = 2)
        
    def feedBuildings(board, pos):
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
        
    def scoreSelf(self, positions):
        count = len(positions)
        return self.p[min(count-1, 5)]

class Tavern(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Tavern", p = [2,5,9,14,20], pCondition = "Number in Town", e = "None", num = 3)
    
    def scoreSelf(self, positions):
        count = len(positions)
        return self.p[min(count-1, 4)]
    
class Inn(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Inn", p = 3, pCondition = "Not in row/col as another", e = "None", num = 3)
    
    def scoreSelf(positions):
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
        score = 3* sum(rowsDuped & colsDuped)
        return score
    
class Tavern(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Tavern", p = 2, pCondition = "+1 if you have more than the person on your right", e = "None", num = 3)
    
    def scoreSelf(positions):
        return 2*len(positions)

#Orange Cards
class Abbey(Card):
    pass
class Chapel(Card):
    pass
class Cloister(Card):
    pass
class Temple(Card):
    pass

#Yellow Cards
class Bakery(Card):
    pass
class Market(Card):
    pass
class Tailor(Card):
    pass
class Theatre(Card):
    pass

#Black Cards
class Bank(Card):
    pass
class Factory(Card):
    pass
class TradingPost(Card):
    pass
class Warehouse(Card):
    pass

#Grey Cards
class Fountain(Card):
    pass
class Millstone(Card):
    pass
class Shed(Card):
    def __init__(self):
        super().__init__("Grey", "Shed", 1, "None", "None", 7)
        
    def scoreSelf(positions):
        score = len(positions)
        return score
class Well(Card):
    pass
