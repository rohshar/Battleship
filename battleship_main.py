import random
from graphics import *

allsquares = []
all_user_ships = []
all_computer_ships = []


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
            self.allPoints.append((self.coord1[0] + increment[0] * i, self.coord1[1] + increment[1] * i))

    def getPoints(self):
        return self.allPoints

    def checkOverlap(self, other_ship):
        other_points = other_ship.getPoints()
        for point in self.getPoints():
            if point in other_points:
                return True
        return False

    def draw(self, graphics_window):
        if self.increment == (1, 0) or self.increment == (0, 1):
            p1 = Point(2 * self.coord1[0], 23 - 2 * self.coord1[1])
            p2 = Point(2 + 2 * self.coord2[0], 21 - 2 * self.coord2[1])
        elif self.increment == (-1, 0):
            p1 = Point(2 + 2 * self.coord1[0], 23 - 2 * self.coord1[1])
            p2 = Point(2 * self.coord2[0], 21 - 2 * self.coord2[1])
        elif self.increment == (0, -1):
            p1 = Point(2 + 2 * self.coord1[0], 21 - 2 * self.coord1[1])
            p2 = Point(2 * self.coord2[0], 23 - 2 * self.coord2[1])

        o = Oval(p1, p2)
        o.setFill("black")
        o.draw(graphics_window)



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
    s5.draw(window)
    ship5.undraw()

    ship4.draw(window)    
    s4 = placeShip(window, 4, [s5])
    s4.draw(window)
    ship4.undraw()    

    ship3.draw(window)    
    s3_1 = placeShip(window, 3, [s5, s4])
    s3_1.draw(window)
    ship3.undraw()    

    ship32.draw(window)    
    s3_2 = placeShip(window, 3, [s5, s4, s3_1])
    s3_2.draw(window)
    ship32.undraw()    

    ship2.draw(window)    
    s2 = placeShip(window, 2, [s5, s4, s3_1, s3_2])
    s2.draw(window)
    ship2.undraw()    

    


def placeShip(window, length, other_ships):
    while True:
        correct_len = False
        overlapping = False
        p = window.getMouse()
        for square in allsquares:
            if square.within(p):
                break
        if (2 > p.getX()) or (22 < p.getX()) or (1 > p.getY()) or (21 < p.getY()):
            print("You clicked out of the ship placement area. Please try again.")
            continue
        p2 = window.getMouse()
        for square2 in allsquares:
            if square2.within(p2):
                break
        if (2 > p2.getX()) or (22 < p2.getX()) or (1 > p2.getY()) or (21 < p2.getY()):
            print("You clicked out of the ship placement area. Please try again.")
            continue

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
            print("The ship is not the correct length. Please try again.")
            continue
        if other_ships is not None:
            for other in other_ships:
                if other.checkOverlap(ship):
                    print("You tried to place your ship on top of another one, please try placing the ship again!")
                    overlapping = True
                    break
        if correct_len == True and overlapping == False:
            all_user_ships.append(ship)    
            return ship


def placeComputerShips(window):
    comp5 = placeComputerShip(5, None)
    comp5.draw(window)

    comp4 = placeComputerShip(4, [comp5])
    comp4.draw(window)

    comp3_1 = placeComputerShip(3, [comp5, comp4])
    comp3_1.draw(window)

    comp3_2 = placeComputerShip(3, [comp5, comp4, comp3_1])
    comp3_2.draw(window)

    comp2 = placeComputerShip(2, [comp5, comp4, comp3_1, comp3_2])
    comp2.draw(window)


def placeComputerShip(length, other_ships):
    while True:
        overlapping = False
        while True:
            anchor_point = random.choice(allsquares)
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            direction = random.choice(directions)
            end_point = (anchor_point.getCoords()[0] + direction[0] * (length - 1), anchor_point.getCoords()[1] + direction[1] * (length - 1))
            if (1 <= end_point[0] <= 10) and (1 <= end_point[1] <= 10):
                break

        ship = Ship(length, anchor_point.getCoords(), end_point, direction)
        if other_ships is not None:
            for other in other_ships:
                if other.checkOverlap(ship):
                    overlapping = True
                    break
        if overlapping == False:
            return ship



def main():
    while True:
        size = input('How large do you want the BattleShip window to be? (from 150-550 px) ')
        if (150 <= size <= 550):
            break
        else:
            print('Your size must be between 150 and 550! Please try again.\n')

    window = GraphWin("User BattleShip", size * 141 / 100.0, size * 131 / 100.0)
    window.setCoords(0, 0, 28, 28)
    drawBoard(size, window)

    placeUserShips(window)

    window2 = GraphWin("Computer BattleShip", size * 121 / 100.0, size * 111 / 100.0)
    window2.setCoords(0, 0, 23, 23)
    drawBoard(size, window2)

    placeComputerShips(window2)


    window.getMouse()
    window.close()

if __name__ == '__main__':
    main()