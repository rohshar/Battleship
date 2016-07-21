from random import randint
from graphics import *

allsquares = []
allships = []

class GridPoint:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def draw(self, graphics_window):
        p = Point(3 + 2 * self.x, 2 + 2 * self.y)
        p.draw(graphics_window)


class GridSquare:
    def __init__(self, top_x, top_y, size):
        self.top_x = top_x
        self.top_y = top_y
        self.size = size
        self.r = None
        self.coords = (top_x + 1, 10 - top_y)

    def draw(self, graphics_window):
        p1 = Point(2 * (self.top_x + 1), 2 * (self.top_y) + 1)
        p2 = Point(2 * (self.top_x + 2), 2 * (self.top_y) + 3)
        self.r = Rectangle(p1, p2)
        self.r.draw(graphics_window)

    def within(self, point):
        p_x = point.getX()
        p_y = point.getY()
        if (2 * (self.top_x + 1)) <= p_x <= (2 * (self.top_x + 2)):
            if (2 * (self.top_y) + 1) <= p_y <= (2 * (self.top_y) + 3):
                return True

    def getRectangle(self):
        return self.r

    def getCoords(self):
        return self.coords


class Ship:
    def __init__(self, length, coord1, coord2, increment):
        self.length = length
        self.coord1 = coord1
        self.coord2 = coord2
        self.increment = increment
        self.allPoints = []
        for i in range(length):
            self.allPoints.append((coord1[0] + increment[0] * i, coord1[1] + increment[1] * i))
        print(self.allPoints)

    def getPoints(self):
        return self.allPoints

    def checkOverlap(self, other_ship):
        other_points = other_ship.getPoints()
        for point in self.getPoints():
            if point in other_points:
                return True
        return False



def drawBoard(size, window):
    rect = Rectangle(Point(2, 1), Point(22, 21))
    rect.setFill("deep sky blue")
    rect.draw(window)

    for i in range(10):
        for j in range(10):
            gp = GridPoint(i, j, size)
            gp.draw(window)

    for i in range(10):
        for j in range(10):
            gs = GridSquare(i, j, size)
            gs.draw(window)
            allsquares.append(gs)

    Text(Point(1, 2), "J").draw(window)
    Text(Point(1, 4), "I").draw(window)
    Text(Point(1, 6), "H").draw(window)
    Text(Point(1, 8), "G").draw(window)
    Text(Point(1, 10), "F").draw(window)
    Text(Point(1, 12), "E").draw(window)
    Text(Point(1, 14), "D").draw(window)
    Text(Point(1, 16), "C").draw(window)
    Text(Point(1, 18), "B").draw(window)
    Text(Point(1, 20), "A").draw(window)

    Text(Point(3, 22), "1").draw(window)
    Text(Point(5, 22), "2").draw(window)
    Text(Point(7, 22), "3").draw(window)
    Text(Point(9, 22), "4").draw(window)
    Text(Point(11, 22), "5").draw(window)
    Text(Point(13, 22), "6").draw(window)
    Text(Point(15, 22), "7").draw(window)
    Text(Point(17, 22), "8").draw(window)
    Text(Point(19, 22), "9").draw(window)
    Text(Point(21, 22), "10").draw(window)


def placeUserShips(window):
    pt=Point(12,25)

    ship5=Text(pt, "Click two squares on the grid so "
    "that\n the resulting ship will be five squares long.")

    ship4=Text(pt, "Click two squares on the grid so "
    "that\n the resulting ship will be four squares long.")

    ship3=Text(pt, "Click two squares on the grid so "
    "that\n the resulting ship will be three squares long.")

    ship32=Text(pt, "Click two squares on the grid so "
    "that\n the resulting ship will also be three squares long.")

    ship2=Text(pt, "Click two squares on the grid so "
    "that\n the resulting ship will be two squares long.")

    ship5.draw(window)
    s5 = placeShip(window, 5, None)
    ship5.undraw()

    ship4.draw(window)    
    s4 = placeShip(window, 4, [s5])
    ship4.undraw()    

    ship3.draw(window)    
    s3_1 = placeShip(window, 3, [s5, s4])
    ship3.undraw()    

    ship32.draw(window)    
    s3_2 = placeShip(window, 3, [s5, s4, s3_1])
    ship32.undraw()    

    ship2.draw(window)    
    s2 = placeShip(window, 2, [s5, s4, s3_1, s3_2])
    ship2.undraw()    

    


def placeShip(window, length, other_ships):
    while True:
        correct_len = False
        p = window.getMouse()
        for square in allsquares:
            if square.within(p):
                square.getRectangle().setOutline('red')
                break
        p2 = window.getMouse()
        for square2 in allsquares:
            if square2.within(p2):
                square2.getRectangle().setOutline('green')
                break
        if (square.getCoords()[0] + length - 1) == (square2.getCoords()[0]) and (square.getCoords()[1]) == (square2.getCoords()[1]):
            correct_len = True
            ship =  Ship(length, square.getCoords(), square2.getCoords(), (1, 0))
        elif (square.getCoords()[0]) == (square2.getCoords()[0] + length - 1) and (square.getCoords()[1]) == (square2.getCoords()[1]):
            correct_len = True
            ship = Ship(length, square.getCoords(), square2.getCoords(), (-1, 0))
        elif (square.getCoords()[1] + length - 1) == (square2.getCoords()[1]) and (square.getCoords()[0]) == (square2.getCoords()[0]):
            correct_len = True
            ship =  Ship(length, square.getCoords(), square2.getCoords(), (0, 1))
        elif (square.getCoords()[1]) == (square2.getCoords()[1] + length - 1) and (square.getCoords()[0]) == (square2.getCoords()[0]):
            correct_len = True
            ship = Ship(length, square.getCoords(), square2.getCoords(), (0, -1))
        if correct_len == False:
            print("The ship is not the correct length")
            square.getRectangle().setOutline('black')
            square2.getRectangle().setOutline('black')
            continue
        if other_ships is not None:
            for other in other_ships:
                if other.checkOverlap(ship):
                    print("Overlapping ship, please try placing th ship again!")
                    square.getRectangle().setOutline('black')
                    square2.getRectangle().setOutline('black')
                    continue
        return ship





def main():
    while True:
        size = input('How large do you want the BattleShip window to be? (from 150-550 px) ')
        if (150 <= size <= 550):
            break
        else:
            print('Your size must be between 150 and 550! Please try again.\n')

    window = GraphWin("BattleShip", size * 141 / 100.0, size * 131 / 100.0)
    window.setCoords(0, 0, 28, 28)
    drawBoard(size, window)

    check = placeUserShips(window)
    print(check)

    window.getMouse()
    window.close()

if __name__ == '__main__':
    main()