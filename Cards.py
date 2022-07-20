class Card(object):
    
    def __init__(self, c, n, p, pCondition, e):
        self.buildingColour = c
        self.Name = n
        self.points = p
        self.pointCondition = pCondition
        self.effect = e
    
        
class Cottage(Card):
    def __init__(self):
        super.__init__(c = "Blue", n = "Cottage", p = 3, pCondition = "Fed", e = None)
  
#Red cards      
class Farm(Card):
    
    def __init__(self):
        super().__init__(c = "Red", n = "Farm", p = 0, pCondition = "None", e = "Feed 4")
        
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
        super().__init__(c = "Red", n = "Greenhouse", p = 0, pCondition = "None", e = "Feeds 1 Contiguous Group")
        
    def feedBuildings(board, pos):
        pass
class Grainary(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Grainary", p = 0, pCondition = "None", e = "Feeds surrounding")
        
    def feedBuildings(board, pos):
        for i in range(max(0, pos[0]-1), min(4, pos[0]+1)):
            for j in range(max(0, pos[1]-1), min(4, pos[1]+1)):
                if board[i,j] == 0:
                    board[i,j] = 1
        return board

class Orchard(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Orchard", p = 0, pCondition = "None", e = "Feeds row and column")
        
    def feedBuildings(board, pos):
        for i in range(4):
            if board[pos[0], i] == 0:
                board[pos[0], i] = 1
            if board[i, pos[1]] == 0:
                board[i, pos[1]] = 1
        return board

class Almshouse(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Almshouse", p = [-1,5,-3,15,-5,26], pCondition = "Number in Town", e = "None")
        
    def scoreSelf(self, count):
        return self.p[min(count-1, 5)]

class Tavern(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Tavern", p = [2,5,9,14,20], pCondition = "Number in Town", e = "None")
    
    def scoreSelf(self, count):
        return self.p[min(count-1, 4)]
    
class Inn(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Inn", p = 3, pCondition = "Not in row/col as another", e = "None")
    
    def scoreSelf(count)