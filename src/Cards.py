
# TODO: 
# pink cards


import numpy as np
from itertools import combinations

def homogenizeBoard(board):
    for i in range(4):
        for j in range(4):
            if board[i,j] == 0:
                board[i,j] = 1
            elif board[i,j] == 12 or board[i,j] == 13:
                board[i,j] = 11
    return board

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

    def findAdjacent(self, pos, board, returnPos = False):
        adj = []
        positions = []
        if pos[0] > 0:
            if returnPos:
                positions.append([pos[0]-1, pos[1]])
            adj.append(board[pos[0]-1, pos[1]])
        if pos[0] < 3:
            if returnPos:
                positions.append([pos[0]+1, pos[1]])
            adj.append(board[pos[0]+1, pos[1]])
        if pos[1] > 0:
            if returnPos:
                positions.append([pos[0], pos[1]-1])
            adj.append(board[pos[0], pos[1]-1])
        if pos[1] < 3:
            if returnPos:
                positions.append([pos[0], pos[1]+1])
            adj.append(board[pos[0], pos[1]+1])
        if returnPos:
            return adj, positions
        else:
            return adj
    
    def scoreSelf(self, positions, board):
        if isinstance(self.points, list):
            count = len(positions)
            return self.points[min(count, len(self.points))]
        elif isinstance(self.points, int):
            return self.points * len(positions)
        else:
            return 0

#Blue Cards
class Cottage(Card):
    def __init__(self):
        super().__init__(c = "Blue", n = "Cottage", p = 3, pCondition = "Fed", e = None, num = 0)

#Red cards      
class Farm(Card):
    
    def __init__(self):
        super().__init__(c = "Red", n = "Farm", p = 0, pCondition = None, e = "Feed 4", num = 2)
        
    def feedBuildings(self, board, positions, cards):
        orangePos = Temple().getPos(board)
        if isinstance(cards[3], Temple) and len(orangePos) > 0 and (len(Cottage().getPos(board)) > len(positions) * 4):
            numBuildingsFed = len(positions) * 4
            maxPoints = 0
            boardStates = [board]
            for comb in combinations(Cottage().getPos(board), r = numBuildingsFed):
                boardTemp = board.copy()
                for pos in comb:
                    boardTemp[pos[0], pos[1]] = 1
                points = numBuildingsFed * 3 + Temple().scoreSelf(orangePos, boardTemp)
                if points > maxPoints:
                    maxPoints = points
                    boardStates.append(boardTemp)
            board = boardStates[-1].copy()
        else:
            for pos in positions:
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
        super().__init__(c = "Red", n = "Greenhouse", p = 0, pCondition = None, e = "Feeds 1 Contiguous Group", num = 2)
        
    def feedBuildings(self, board, positions, cards):
        for rpos in positions:
            toFeedPos = Cottage().getPos(board)
            if len(toFeedPos) > 0:
                setIndicator = 1001
                for pos in toFeedPos:
                    if board[pos[0], pos[1]] == 0:
                        board[pos[0], pos[1]] = setIndicator
                        board = self.recursiveSearchAdjacent(pos, board, setIndicator)
                        setIndicator += 1
                setIndicator = 1001
                setSize = np.count_nonzero(board == setIndicator)
                if isinstance(cards[3], Temple) and len(Temple().getPos(board)) > 0: 
                    boardStates = [board]
                    maxPoints = 0
                    while(setSize > 0):
                        boardTemp = board.copy()
                        points = 0
                        for i in range(4):
                            for j in range(4):
                                if boardTemp[i,j] == setIndicator:
                                    boardTemp[i,j] = 1
                                    points += 3
                        templePos = Temple().getPos(board)
                        points = points +  Temple().scoreSelf(templePos, boardTemp)
                        if (points > maxPoints):
                            maxPoints = points
                            boardStates.append(boardTemp)
                        setIndicator += 1
                        setSize = np.count_nonzero(board == setIndicator)
                    board = boardStates[-1].copy()
                    for i in range(4):
                        for j in range(4):
                            if board[i,j] > 1000:
                                board[i,j] = 0
                else:
                    largestSetSize = setSize
                    largestSetIndicator = 1001 
                    while(setSize > 0):
                        setIndicator += 1
                        setSize = np.count_nonzero(board == setIndicator)
                        if setSize > largestSetSize:
                            largestSetSize = setSize
                            largestSetIndicator = setIndicator
                    for i in range(4):
                        for j in range(4):
                            if board[i,j] == largestSetIndicator:
                                board[i,j] = 1
                            elif board[i,j] > 1000:
                                board[i,j] = 0
        return board

    def recursiveSearchAdjacent(self, pos, board, setIndicator):
        adj, positions = self.findAdjacent(pos, board, returnPos=True)
        for i in range(len(adj)):
            if adj[i] == 0:
                positioni = positions[i]
                board[positioni[0], positioni[1]] = setIndicator
                board = self.recursiveSearchAdjacent(positions[i], board, setIndicator)
        return board

class Grainary(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Grainary", p = 0, pCondition = None, e = "Feeds surrounding", num = 2)
        
    def feedBuildings(self, board, positions, cards):
        for pos in positions:
            for i in range(max(0, pos[0]-1), min(4, pos[0]+2)):
                for j in range(max(0, pos[1]-1), min(4, pos[1]+2)):
                    if board[i,j] == 0:
                        board[i,j] = 1
        return board

class Orchard(Card):
    def __init__(self):
        super().__init__(c = "Red", n = "Orchard", p = 0, pCondition = None, e = "Feeds row and column", num = 2)
        
    def feedBuildings(self, board, positions, cards):
        for pos in positions:
            for i in range(4):
                if board[pos[0], i] == 0:
                    board[pos[0], i] = 1
                if board[i, pos[1]] == 0:
                    board[i, pos[1]] = 1
        return board

#Green Cards
class Almshouse(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Almshouse", p = [0,-1,5,-3,15,-5,26], pCondition = "Number in Town", e = "None", num = 3)

class Tavern(Card):
    def __init__(self):
        super().__init__(c = "Green", n = "Tavern", p = [0,2,5,9,14,20], pCondition = "Number in Town", e = "None", num = 3)
    
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
    
class FeastHall(Card): #TODO
    def __init__(self):
        super().__init__(c = "Green", n = "Feast Hall", p = 2, pCondition = "+1 if you have more than the person on your right", e = "None", num = 3)

    # def scoreSelf(self, positions, board):
    #     return 2*len(positions)

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
        score = 0
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
        board = homogenizeBoard(board)
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

class Factory(Card):
    def __init__(self):
        super().__init__(c = "Black", n = "Factory", p = 0, pCondition = None, e = "When the resource on this building is called, player may instead place another resource", num = 6)
        
class TradingPost(Card):
    def __init__(self):
        super().__init__(c = "Black", n = "Bank", p = 1, pCondition = None, e = "Treat as wild resource", num = 6)

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
        super().__init__(c = "Grey", n = "Shed", p = 1, pCondition = None, e = "Can be placed anywhere in town", num = 7)

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

#Pink Cards

class Architects_Guild(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Architect's Guild", p = 1, pCondition = None, e = "When constructed, replace up to 2 buildings in your town with any other building types.", num = 8)
    
class Archive_of_the_Second_Age(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Archive of the Second Age", p = 1, pCondition = "1 per unique building type (other than this) in your town", e = None, num = 8)
        
    def scoreSelf(self, positions, board):
        board = homogenizeBoard(board)
        buildingTypes = []
        for i in range(4):
            for j in range(4):
                if board[i,j] not in buildingTypes and board[i,j] != 8 and board[i,j] != -1:
                    buildingTypes.append(board[i,j])
        score = len(buildingTypes)
        return score
    
class Barrett_Castle(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Barrett Castle", p = 5, pCondition = "Fed", e = None, num = 8)
        
    def scoreSelf(self, positions, board): #TODO
        pass

class Cathedral_of_Caterina(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Cathedral of Caterina", p = 2, pCondition = None, e = "Empty squares are worth 0 (instead of -1)", num = 8)

    def scoreSelf(self, positions, board):
        score = 2
        for i in range(4):
            for j in range(4):
                if board[i,j]==-1:
                    score += 1
        return score
    
class Fort_Ironweed(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Fort Ironweed", p = 7, pCondition = None, e = "Once Built, you no longer take turns as the Master Builder", num = 8)

class Grand_Mausoleum_of_the_Rodina(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Grand Mauseleum of the Rodina", p = 0, pCondition = "3 per unfed cottage", e = None, num = 8)

    def scoreSelf(self, positions, board):
        score = 0
        for i in range(4):
            for j in range(4):
                if board[i,j] == 0:
                    score += 3
        return score
    
class Grove_University(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Grove University", p = 3, pCondition = "When built, immediately place a building on an empty square in your town", e = None, num = 8)

class Mandras_Palace(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Mandras Palace", p = 2, pCondition = "2 Points for each unique adjacent building type", e = None, num = 8)

    def scoreSelf(self, positions, board):
        adj = self.findAdjacent(positions[0], board)
        uniqueTypes = set()
        for a in adj:
            if a != -1:
                uniqueTypes.add(a)
        score = 2 * len(uniqueTypes)
        return score
    
class Obelisk_of_the_Crescent(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Obelisk of the Crescent", p = 0, pCondition = None, e = "You may place all future buildings on any empty square in your town", num = 8)

class Opaleyes_Watch(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Opaleye's Watch", p = 0, pCondition = None, e = "Immediately place 3 unique buildings on this card. Whenever a player on the left or right of you constructs 1 of those buildings, take the building from here and place it on an empty square in your town.", num = 8)

class Shrine_of_the_Elder_Tree(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Shrine of the Elder Tree", p = [1,2,3,4,5,8], pCondition = "Points based on the number of buildings in your town when constructed", e = None, num = 8)
    
    def scoreSelf(self, positions, board): #TODO
        pass

class Silva_Forum(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Silva Forum", p = 1, pCondition = "1 +1 for each building in your largest contiguous group of buildings of the same type in your town", e = None, num = 8)

    def scoreSelf(self, positions, board): #TODO
        pass

class The_Sky_Baths(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "The Sky Baths", p = 2, pCondition = "2 points for each building type your town is missing", e = None, num = 8)

    def scoreSelf(self, positions, board):
        board = homogenizeBoard(board)
        buildingTypes = set()
        for i in range(4):
            for j in range(4):
                if board[i,j] != -1 and board[i,j] != 8:
                    buildingTypes.add(board[i,j])
        score = 2 * (7 - len(buildingTypes))
        return score
    
class The_Starloom(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "The Starloom", p = [6,3,2,0,0,0], pCondition = "Points based on when you complete your town", e = None, num = 8)

    def scoreSelf(self, positions, board): #TODO
        pass

class Statue_of_the_Bondmaker(Card):
    def __init__(self):
        super().__init__(c = "Pink", n = "Statue of the Bondmaker", p = 0, pCondition = None, e = "When another player names a resource, you may choose to place it on a square with a cottage. Each of your Cottages can hold 1 resource.", num = 8)