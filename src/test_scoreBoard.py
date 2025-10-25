from Cards import *
from scoreBoard import *
import numpy as np

'''
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

def test_scoreBoard1():
    cards = [Cottage(), Farm(), Tavern(), Abbey(), Market(), TradingPost(), Well()]

    board1 = np.array([[7,4,7,0],
                       [4,0,0,3],
                       [5,0,6,0],
                       [5,5,5,2]])
    score1 = scoreBoard(cards, board1)
    print("Score 1 should be 31")
    print(f'{score1} \n {sum(score1)}')

    board2 = np.array([[3,0,2,5],
                       [3,7,0,5],
                       [3,0,7,5],
                       [3,3,0,5]])
    score2 = scoreBoard(cards, board2)
    print("Score 2 should be 48")
    print(f'{score2} \n {sum(score2)}')

def test_scoreBoard2():
    cards = [Cottage(), Grainary(), Inn(), Chapel(), Theatre(), Bank(), Millstone()]

    board1 = np.array([[7,5,4,7],
                       [0,0,6,3],
                       [0,2,6,3],
                       [0,3,0,0]])
    score1 = scoreBoard(cards, board1)
    print("Score 1 should be 38")
    print(f'{score1} \n {sum(score1)}')

    board2 = np.array([[7,5,4,3],
                       [0,0,-1,5],
                       [0,2,7,-1],
                       [0,3,0,0]])
    score2 = scoreBoard(cards, board2)
    print("Score 2 should be 35")
    print(f'{score2} \n {sum(score2)}')

def test_scoreBoard3():
    cards = [Cottage(), Orchard(), Almshouse(), Cloister(), Tailor(), Warehouse(), Fountain()]

    board1 = np.array([[4,4,5,4],
                       [0,5,5,3],
                       [7,5,0,12],
                       [7,0,2,4]])
    score1 = scoreBoard(cards, board1)
    print("Score 1 should be 35")
    print(f'{score1} \n {sum(score1)}')

    board2 = np.array([[11,4,5,4],
                       [-1,7,5,3],
                       [7,5,0,12],
                       [7,0,2,4]])
    score2 = scoreBoard(cards, board2)
    print("Score 2 should be 20")
    print(f'{score2} \n {sum(score2)}')

def test_scoreBoard4():
    cards = [Cottage(), Greenhouse(), Almshouse(), Temple(), Tailor(), Warehouse(), Fountain()]

    board1 = np.array([[0,7,2,7],
                       [0,0,7,0],
                       [0,7,0,0],
                       [0,0,7,0]])
    score1 = scoreBoard(cards, board1)
    print("Score 1 should be 18")
    print(f'{score1} \n {sum(score1)}')

    board2 = np.array([[0,7,2,7],
                       [0,0,4,4],
                       [0,4,0,0],
                       [0,0,7,0]])
    score2 = scoreBoard(cards, board2)
    print("Score 2 should be 22")
    print(f'{score2} \n {sum(score2)}')

    board3 = np.array([[0,7,2,4],
                       [0,0,4,0],
                       [0,7,0,0],
                       [0,0,4,0]])
    score3 = scoreBoard(cards, board3)
    print("Score 3 should be 20")
    print(f'{score3} \n {sum(score3)}')

def test_scoreBoard5():
    cards = [Cottage(), Farm(), Almshouse(), Temple(), Tailor(), Warehouse(), Fountain()]

    board1 = np.array([[0,7,2,7],
                       [0,0,7,0],
                       [0,4,0,4],
                       [7,0,7,0]])
    score1 = scoreBoard(cards, board1)
    print("Score 1 should be 20")
    print(f'{score1} \n {sum(score1)}')

def test_scoreBoard6():
    cards = [Cottage(), Orchard(), Almshouse(), Cloister(), Tailor(), Warehouse(), Fountain()]

    board1 = np.array([[4,4,5,4],
                       [0,5,5,3],
                       [7,5,0,12],
                       [7,0,8,4]])
    score1 = scoreBoard(cards, board1, landmark=Grand_Mausoleum_of_the_Rodina())
    print("Score 1 should be 38")
    print(f'{score1} \n {sum(score1)}')

    board2 = np.array([[4,-1,-1,4],
                       [0,-1,5,3],
                       [7,8,0,12],
                       [7,0,2,4]])
    score2 = scoreBoard(cards, board2, landmark=Cathedral_of_Caterina())
    print("Score 2 should be 20")
    print(f'{score2} \n {sum(score2)}')

if __name__ == "__main__":
    test_scoreBoard1()
    test_scoreBoard2()
    test_scoreBoard3()
    test_scoreBoard4()
    test_scoreBoard5()
    test_scoreBoard6()