import random
from graphics import *

class Player:
    def __init__(self):
        self.all_squares = []

    def turn(self):
        pass

    def placeShips(self):
        pass

    def drawBoard(self, size, window):
        rect = Rectangle(Point(2, 1), Point(22, 21))
        rect.setFill("deep sky blue")
        rect.draw(window)

        for i in range(10):
            for j in range(10):
                gp = GridPoint(i, j, size)
                gp.draw(window)
                gs = GridSquare(i, j, size)
                gs.draw(window)
                gs.setMidpoint(gp)
                self.all_squares.append(gs)

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


class HumanPlayer(Player):
    def __init__(self):
        self.all_user_ships = []
        self.all_occupied_points = []
        self.hit_points = []

        Player.__init__(self)

    def placeShips(self, window):
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
        s5 = self.placeShip(window, 5, None)
        s5.draw(window)
        ship5.undraw()

        ship4.draw(window)    
        s4 = self.placeShip(window, 4, [s5])
        s4.draw(window)
        ship4.undraw()    

        ship3.draw(window)    
        s3_1 = self.placeShip(window, 3, [s5, s4])
        s3_1.draw(window)
        ship3.undraw()    

        ship32.draw(window)    
        s3_2 = self.placeShip(window, 3, [s5, s4, s3_1])
        s3_2.draw(window)
        ship32.undraw()    

        ship2.draw(window)    
        s2 = self.placeShip(window, 2, [s5, s4, s3_1, s3_2])
        s2.draw(window)
        ship2.undraw() 

        for ship in self.all_user_ships:
            self.all_occupied_points += ship.getPoints()

    def placeShip(self, window, length, other_ships):
        while True:
            correct_len = False
            overlapping = False
            p = window.getMouse()
            for square in self.all_squares:
                if square.within(p):
                    break
            if (2 > p.getX()) or (22 < p.getX()) or (1 > p.getY()) or (21 < p.getY()):
                print("You clicked out of the ship placement area. Please try again.")
                continue
            p2 = window.getMouse()
            for square2 in self.all_squares:
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
                self.all_user_ships.append(ship)    
                return ship   

    def getOccupiedPoints(self):
        return self.all_occupied_points

    def getAllSquares(self):
        return self.all_squares

    def hit(self, location):
        self.hit_points.append(location)

    def removeSquare(self, square):
        self.all_squares.remove(square)

    def hasLost(self):
        if set(self.all_occupied_points) == set(self.hit_points):
            return True
        return False

    def turn(self, opponent, other_window):
        is_repeat = True
        while is_repeat == True:
            p = other_window.getMouse()
            for square in opponent.getAllSquares():
                if square.within(p):
                    is_repeat = False
                    opponent.removeSquare(square)
                    break
        opponent_points = opponent.getOccupiedPoints()
        if square.getCoords() in opponent_points:
            square.getMidpoint().changeColor('red', other_window)
            opponent.hit(square.getCoords())
        else:
            square.getMidpoint().changeColor('white', other_window)



class ComputerPlayer(Player):
    def __init__(self):
        self.all_computer_ships = []
        self.all_occupied_points = []
        self.hit_points = []

        Player.__init__(self)

    def placeShips(self, window):
        comp5 = self.placeShip(5, None)
        comp5.draw(window)

        comp4 = self.placeShip(4, [comp5])
        comp4.draw(window)

        comp3_1 = self.placeShip(3, [comp5, comp4])
        comp3_1.draw(window)

        comp3_2 = self.placeShip(3, [comp5, comp4, comp3_1])
        comp3_2.draw(window)

        comp2 = self.placeShip(2, [comp5, comp4, comp3_1, comp3_2])
        comp2.draw(window)

        for ship in self.all_computer_ships:
            self.all_occupied_points += ship.getPoints()
        print(self.all_occupied_points)

    def getAllSquares(self):
        return self.all_squares

    def placeShip(self, length, other_ships):
        while True:
            overlapping = False
            while True:
                anchor_point = random.choice(self.all_squares)
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
                self.all_computer_ships.append(ship)
                return ship

    def getOccupiedPoints(self):
        return self.all_occupied_points

    def removeSquare(self, square):
        self.all_squares.remove(square)

    def hit(self, location):
        self.hit_points.append(location)

    def hasLost(self):
        if set(self.all_occupied_points) == set(self.hit_points):
            return True
        return False

    def turn(self, opponent, other_window):
        square = random.choice(opponent.getAllSquares())
        opponent.removeSquare(square)
        opponent_points = opponent.getOccupiedPoints()
        if square.getCoords() in opponent_points:
            square.getMidpoint().changeColor('red', other_window)
            opponent.hit(square.getCoords())
        else:
            square.getMidpoint().changeColor('white', other_window)



class GridPoint:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.p = None

    def draw(self, graphics_window):
        self.p = Circle(Point(3 + 2 * self.x, 2 + 2 * self.y), .15)
        self.p.draw(graphics_window)

    def changeColor(self, color, graphics_window):
        self.p.setFill(color)
        self.p.undraw()
        self.p.draw(graphics_window)


class GridSquare:
    def __init__(self, top_x, top_y, size):
        self.top_x = top_x
        self.top_y = top_y
        self.size = size
        self.r = None
        self.coords = (top_x + 1, 10 - top_y)
        self.midpoint = None

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

    def setMidpoint(self, point):
        self.midpoint = point

    def getMidpoint(self):
        return self.midpoint


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


def main():
    while True:
        size = input('How large do you want the BattleShip window to be? (from 150-550 px) ')
        if (150 <= size <= 550):
            break
        else:
            print('Your size must be between 150 and 550! Please try again.\n')

    user = HumanPlayer()
    computer = ComputerPlayer()

    window = GraphWin("User BattleShip", size * 141 / 100.0, size * 131 / 100.0)
    window.setCoords(0, 0, 28, 28)
    user.drawBoard(size, window)
    user.placeShips(window)

    window2 = GraphWin("Computer BattleShip", size * 121 / 100.0, size * 111 / 100.0)
    window2.setCoords(0, 0, 23, 23)
    computer.drawBoard(size, window2)
    computer.placeShips(window2)

    finished = False
    while not user.hasLost() and not computer.hasLost():
        user.turn(computer, window2)
        computer.turn(user, window)

    print('Game is finished!\n\n')
    if window.getMouse() or window2.getMouse():
        window.close()
        window2.close()

if __name__ == '__main__':
    main()