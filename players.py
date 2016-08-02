from graphics import *
from drawables import GridPoint, GridSquare, Ship
from parse_matrix import getSpotOrdering
from matrix_parser import getSquareOrdering
from ship_placement import getPlacementNumbers
import random


class Player:
    def __init__(self):
        self.all_squares = []
        self.parity_squares = []
        self.ships_left = [5, 4, 3, 3, 2]
        self.all_opponent_guesses = []
        self.all_occupied_points = []
        self.hit_points = []
        self.all_ship_objects = []

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
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self.parity_squares.append(gs)

        start_char = ord("J")
        start_num = ord("1")
        for i in range(9):
            Text(Point(1, 2 + 2 * i), chr(start_char - i)).draw(window)
            Text(Point(3 + 2 * i, 22), chr(start_num + i)).draw(window)
        Text(Point(1, 20), "A").draw(window)
        Text(Point(21, 22), "10").draw(window)

    def removeShip(self, length):
        self.ships_left.remove(length)

    def getShipLengthsLeft(self):
        return self.ships_left

    def getParitySquares(self):
        return self.parity_squares

    def removeParitySquare(self, square):
        if square in self.parity_squares:
            self.parity_squares.remove(square)

    def getGuesses(self):
        return self.all_opponent_guesses

    def addGuess(self, guess):
        self.all_opponent_guesses.append(guess)

    def getAllSquares(self):
        return self.all_squares

    def removeSquare(self, square):
        self.all_squares.remove(square)

    def getOccupiedPoints(self):
        return self.all_occupied_points

    def hit(self, location):
        self.hit_points.append(location)

    def getShips(self):
        return self.all_ship_objects

    def sinkShip(self, ship):
        self.all_ship_objects.remove(ship)

    def hasLost(self):
        if set(self.all_occupied_points) == set(self.hit_points):
            return True
        return False


class HumanPlayer(Player):
    def __init__(self):

        Player.__init__(self)

    def placeShips(self, window):
        pt = Point(12, 25)

        ship5 = Text(pt, "Click two squares on the grid so "
                     "that\n the resulting ship will be five squares long.")

        ship4 = Text(pt, "Click two squares on the grid so "
                     "that\n the resulting ship will be four squares long.")

        ship3 = Text(pt, "Click two squares on the grid so "
                     "that\n the resulting ship will be three squares long.")

        ship32 = Text(pt, "Click two squares on the grid so "
                      "that\n the resulting ship will also be three squares long.")

        ship2 = Text(pt, "Click two squares on the grid so "
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

        for ship in self.all_ship_objects:
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
                print(
                    "You clicked out of the ship placement area. Please try again.")
                continue
            p2 = window.getMouse()
            for square2 in self.all_squares:
                if square2.within(p2):
                    break
            if (2 > p2.getX()) or (22 < p2.getX()) or (1 > p2.getY()) or (21 < p2.getY()):
                print(
                    "You clicked out of the ship placement area. Please try again.")
                continue

            if (square.getCoords()[0] + length - 1) == (square2.getCoords()[0]) and (square.getCoords()[1]) == (square2.getCoords()[1]):
                correct_len = True
                ship = Ship(
                    length, square.getCoords(), square2.getCoords(), (1, 0))
            elif (square.getCoords()[0]) == (square2.getCoords()[0] + length - 1) and (square.getCoords()[1]) == (square2.getCoords()[1]):
                correct_len = True
                ship = Ship(
                    length, square.getCoords(), square2.getCoords(), (-1, 0))
            elif (square.getCoords()[1] + length - 1) == (square2.getCoords()[1]) and (square.getCoords()[0]) == (square2.getCoords()[0]):
                correct_len = True
                ship = Ship(
                    length, square.getCoords(), square2.getCoords(), (0, 1))
            elif (square.getCoords()[1]) == (square2.getCoords()[1] + length - 1) and (square.getCoords()[0]) == (square2.getCoords()[0]):
                correct_len = True
                ship = Ship(
                    length, square.getCoords(), square2.getCoords(), (0, -1))
            if correct_len == False:
                print("The ship is not the correct length. Please try again.")
                continue
            if other_ships is not None:
                for other in other_ships:
                    if other.checkOverlap(ship):
                        print(
                            "You tried to place your ship on top of another one, please try placing the ship again!")
                        overlapping = True
                        break
            if correct_len == True and overlapping == False:
                self.all_ship_objects.append(ship)
                return ship

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
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.found_target = False
        self.last_point = None
        self.remaining_directions = None
        self.all_viable_points = {}
        self.naive_ordering = getSpotOrdering()
        self.can_theorize = True

        Player.__init__(self)

    def placeShips(self, window):
        comp5 = self.placeShip(5, None)
        # comp5.draw(window)

        comp4 = self.placeShip(4, [comp5])
        # comp4.draw(window)

        comp3_1 = self.placeShip(3, [comp5, comp4])
        # comp3_1.draw(window)

        comp3_2 = self.placeShip(3, [comp5, comp4, comp3_1])
        # comp3_2.draw(window)

        comp2 = self.placeShip(2, [comp5, comp4, comp3_1, comp3_2])
        # comp2.draw(window)

        for ship in self.all_ship_objects:
            self.all_occupied_points += ship.getPoints()

    def placeShip(self, length, other_ships):
        while True:
            overlapping = False
            while True:
                anchor_point = random.choice(self.all_squares)
                directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                direction = random.choice(directions)
                end_point = (anchor_point.getCoords()[
                             0] + direction[0] * (length - 1), anchor_point.getCoords()[1] + direction[1] * (length - 1))
                if (1 <= end_point[0] <= 10) and (1 <= end_point[1] <= 10):
                    break

            ship = Ship(length, anchor_point.getCoords(), end_point, direction)
            if other_ships is not None:
                for other in other_ships:
                    if other.checkOverlap(ship):
                        overlapping = True
                        break
            if overlapping == False:
                self.all_ship_objects.append(ship)
                return ship

    def nextPriorityGuess(self):
        return self.naive_ordering.pop(0)

    def hitAction(self, square, opponent, other_window):
        square.getMidpoint().changeColor('red', other_window)
        opponent.hit(square.getCoords())
        self.last_point = square.getCoords()
        self.remaining_directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        self.found_target = True
        self.all_viable_points[self.last_point] = self.remaining_directions
        for ship in opponent.getShips():
            if set(ship.getPoints()).issubset(set(self.getGuesses())):
                opponent.sinkShip(ship)
                opponent.removeShip(ship.getLength())

    def cleanDictionary(self, opponent, other_window):
        if self.last_point in self.all_viable_points:
            del self.all_viable_points[self.last_point]
        if self.all_viable_points:
            self.last_point = random.choice(self.all_viable_points.keys())
            self.remaining_directions = self.all_viable_points[self.last_point]
            self.turn(opponent, other_window)
            return
        else:
            self.found_target = False
            self.turn(opponent, other_window)
            return

    def turn(self, opponent, other_window):

        # random guessing
        if self.difficulty == 1:
            square = random.choice(opponent.getAllSquares())
            opponent.removeSquare(square)
            opponent_points = opponent.getOccupiedPoints()
            if square.getCoords() in opponent_points:
                square.getMidpoint().changeColor('red', other_window)
                opponent.hit(square.getCoords())
            else:
                square.getMidpoint().changeColor('white', other_window)

        # random guessing until a hit, then targets points blindly around it
        elif self.difficulty == 2:
            if not self.found_target:
                square = random.choice(opponent.getAllSquares())
                opponent.removeSquare(square)
                opponent_points = opponent.getOccupiedPoints()
                opponent.addGuess(square.getCoords())
                if square.getCoords() in opponent_points:
                    self.hitAction(square, opponent, other_window)
                else:
                    square.getMidpoint().changeColor('white', other_window)
            else:
                next_point = None
                while True:
                    if not self.remaining_directions or self.remaining_directions == []:
                        self.cleanDictionary(opponent, other_window)
                        break

                    try:
                        direction = random.choice(self.remaining_directions)
                        self.remaining_directions.remove(direction)
                        next_point = (self.last_point[0] + direction[0], self.last_point[1] + direction[1])
                        if next_point not in opponent.getGuesses():
                            break
                    except:
                        self.cleanDictionary(opponent, other_window)
                        break

                if next_point:
                    if (1 <= next_point[0] <= 10) and (1 <= next_point[1] <= 10):
                        opponent.addGuess(next_point)
                        if next_point in opponent.getOccupiedPoints():
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    self.hitAction(square, opponent, other_window)
                                    break
                        else:
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    square.getMidpoint().changeColor('white', other_window)
                                    if not self.remaining_directions:
                                        del self.all_viable_points[
                                            self.last_point]
                                        if self.all_viable_points:
                                            self.last_point = random.choice(
                                                self.all_viable_points.keys())
                                            self.remaining_directions = self.all_viable_points[self.last_point]
                                        else:
                                            self.found_target = False
                                    break
                    else:
                        self.turn(opponent, other_window)

        # parity guessing, then targets points around it
        elif self.difficulty == 2.5:
            if not self.found_target:
                if opponent.getParitySquares():
                    square = random.choice(opponent.getParitySquares())
                    opponent.removeParitySquare(square)
                else:
                    square = random.choice(opponent.getAllSquares())
                opponent.removeSquare(square)
                opponent_points = opponent.getOccupiedPoints()
                opponent.addGuess(square.getCoords())
                if square.getCoords() in opponent_points:
                    self.hitAction(square, opponent, other_window)
                else:
                    square.getMidpoint().changeColor('white', other_window)
            else:
                next_point = None
                while True:
                    if not self.remaining_directions or self.remaining_directions == []:
                        self.cleanDictionary(opponent, other_window)
                        break

                    try:
                        direction = random.choice(self.remaining_directions)
                        self.remaining_directions.remove(direction)
                        next_point = (self.last_point[0] + direction[0], self.last_point[1] + direction[1])
                        if next_point not in opponent.getGuesses():
                            break
                    except:
                        self.cleanDictionary(opponent, other_window)
                        break

                if next_point:
                    if (1 <= next_point[0] <= 10) and (1 <= next_point[1] <= 10):
                        opponent.addGuess(next_point)
                        if next_point in opponent.getOccupiedPoints():
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    self.hitAction(square, opponent, other_window)
                                    break
                        else:
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    square.getMidpoint().changeColor('white', other_window)
                                    if not self.remaining_directions:
                                        del self.all_viable_points[self.last_point]
                                        if self.all_viable_points:
                                            self.last_point = random.choice(self.all_viable_points.keys())
                                            self.remaining_directions = self.all_viable_points[
                                                self.last_point]
                                        else:
                                            self.found_target = False
                                    break
                    else:
                        self.turn(opponent, other_window)

        # parity guessing, then targets points around it, when it gets a second
        # hit, goes in that direction
        elif self.difficulty == 3:
            if not self.found_target:
                if opponent.getParitySquares():
                    square = random.choice(opponent.getParitySquares())
                    opponent.removeParitySquare(square)
                else:
                    square = random.choice(opponent.getAllSquares())
                opponent.removeSquare(square)
                opponent_points = opponent.getOccupiedPoints()
                opponent.addGuess(square.getCoords())
                if square.getCoords() in opponent_points:
                    self.hitAction(square, opponent, other_window)
                else:
                    square.getMidpoint().changeColor('white', other_window)
            else:
                next_point = None
                while True:
                    if not self.remaining_directions or self.remaining_directions == []:
                        self.cleanDictionary(opponent, other_window)
                        break

                    try:
                        direction = random.choice(self.remaining_directions)
                        self.remaining_directions.remove(direction)
                        next_point = (self.last_point[0] + direction[0], self.last_point[1] + direction[1])
                        if next_point not in opponent.getGuesses():
                            break
                    except:
                        self.cleanDictionary(opponent, other_window)
                        break

                if next_point:
                    if (1 <= next_point[0] <= 10) and (1 <= next_point[1] <= 10):
                        opponent.addGuess(next_point)
                        if next_point in opponent.getOccupiedPoints():
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    square.getMidpoint().changeColor('red', other_window)
                                    opponent.hit(square.getCoords())
                                    self.all_viable_points[self.last_point] = [[-1 * direction[0], -1 * direction[1]]]
                                    self.last_point = square.getCoords()
                                    self.remaining_directions = [direction]
                                    self.found_target = True
                                    self.all_viable_points[self.last_point] = self.remaining_directions
                                    break
                        else:
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    square.getMidpoint().changeColor('white', other_window)
                                    if not self.remaining_directions:
                                        del self.all_viable_points[self.last_point]
                                        if self.all_viable_points:
                                            self.last_point = random.choice(self.all_viable_points.keys())
                                            self.remaining_directions = self.all_viable_points[self.last_point]
                                        else:
                                            self.found_target = False
                                    break
                    else:
                        self.turn(opponent, other_window)

        # guess based on most likely squares, target in one direction
        elif self.difficulty == 4:
            if not self.found_target:
                if opponent.getParitySquares():
                    coords = self.nextPriorityGuess()
                    while coords in opponent.getGuesses():
                        coords = self.nextPriorityGuess()
                    for square in opponent.getAllSquares():
                        if square.getCoords() == coords:
                            opponent.removeSquare(square)
                            opponent.removeParitySquare(square)
                            break
                else:
                    square = random.choice(opponent.getAllSquares())
                    opponent.removeSquare(square)
                opponent_points = opponent.getOccupiedPoints()
                opponent.addGuess(square.getCoords())
                if square.getCoords() in opponent_points:
                    self.hitAction(square, opponent, other_window)
                else:
                    square.getMidpoint().changeColor('white', other_window)
            else:
                next_point = None
                while True:
                    if not self.remaining_directions or self.remaining_directions == []:
                        self.cleanDictionary(opponent, other_window)
                        break

                    try:
                        direction = random.choice(self.remaining_directions)
                        self.remaining_directions.remove(direction)
                        next_point = (
                            self.last_point[0] + direction[0], self.last_point[1] + direction[1])
                        if next_point not in opponent.getGuesses():
                            break
                    except:
                        self.cleanDictionary(opponent, other_window)
                        break

                if next_point:
                    if (1 <= next_point[0] <= 10) and (1 <= next_point[1] <= 10):
                        opponent.addGuess(next_point)
                        if next_point in opponent.getOccupiedPoints():
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    square.getMidpoint().changeColor('red', other_window)
                                    opponent.hit(square.getCoords())
                                    self.all_viable_points[self.last_point] = [[-1 * direction[0], -1 * direction[1]]]
                                    self.last_point = square.getCoords()
                                    self.remaining_directions = [direction]
                                    self.found_target = True
                                    self.all_viable_points[self.last_point] = self.remaining_directions
                                    break
                        else:
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    square.getMidpoint().changeColor('white', other_window)
                                    if not self.remaining_directions:
                                        del self.all_viable_points[
                                            self.last_point]
                                        if self.all_viable_points:
                                            self.last_point = random.choice(self.all_viable_points.keys())
                                            self.remaining_directions = self.all_viable_points[self.last_point]
                                        else:
                                            self.found_target = False
                                    break
                    else:
                        self.turn(opponent, other_window)

        # calculate density matricies based on ships left and points guessed,
        # and guess based on that
        elif self.difficulty == 5:
            if not self.found_target:
                if opponent.getParitySquares() and self.can_theorize:
                    numbers_mtx = getPlacementNumbers(opponent.getGuesses(), opponent.getShipLengthsLeft())
                    if numbers_mtx == None:
                        self.can_theorize = False
                        self.turn(opponent, other_window)
                        return
                    priority_list = getSquareOrdering(numbers_mtx)
                    if not priority_list:
                        self.can_theorize = False
                        self.turn(opponent, other_window)
                        return
                    coords = priority_list.pop(0)
                    while coords in opponent.getGuesses():
                        coords = priority_list.pop(0)
                    for square in opponent.getAllSquares():
                        if square.getCoords() == coords:
                            opponent.removeSquare(square)
                            opponent.removeParitySquare(square)
                            break

                elif opponent.getParitySquares():
                    coords = self.nextPriorityGuess()
                    while coords in opponent.getGuesses():
                        coords = self.nextPriorityGuess()
                    for square in opponent.getAllSquares():
                        if square.getCoords() == coords:
                            opponent.removeSquare(square)
                            opponent.removeParitySquare(square)
                            break
                else:
                    square = random.choice(opponent.getAllSquares())
                    opponent.removeSquare(square)
                opponent_points = opponent.getOccupiedPoints()
                opponent.addGuess(square.getCoords())
                if square.getCoords() in opponent_points:
                    self.hitAction(square, opponent, other_window)
                else:
                    square.getMidpoint().changeColor('white', other_window)
            else:
                next_point = None
                while True:
                    if not self.remaining_directions or self.remaining_directions == []:
                        self.cleanDictionary(opponent, other_window)
                        break

                    try:
                        direction = random.choice(self.remaining_directions)
                        self.remaining_directions.remove(direction)
                        next_point = (self.last_point[0] + direction[0], self.last_point[1] + direction[1])
                        if next_point not in opponent.getGuesses():
                            break
                    except:
                        self.cleanDictionary(opponent, other_window)
                        break

                if next_point:
                    if (1 <= next_point[0] <= 10) and (1 <= next_point[1] <= 10):
                        opponent.addGuess(next_point)
                        if next_point in opponent.getOccupiedPoints():
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    square.getMidpoint().changeColor('red', other_window)
                                    opponent.hit(square.getCoords())
                                    self.all_viable_points[self.last_point] = [[-1 * direction[0], -1 * direction[1]]]
                                    self.last_point = square.getCoords()
                                    self.remaining_directions = [direction]
                                    self.found_target = True
                                    self.all_viable_points[
                                        self.last_point] = self.remaining_directions
                                    for ship in opponent.getShips():
                                        if set(ship.getPoints()).issubset(set(opponent.getGuesses())):
                                            opponent.sinkShip(ship)
                                            opponent.removeShip(
                                                ship.getLength())
                                    break
                        else:
                            for square in opponent.getAllSquares():
                                if square.getCoords() == next_point:
                                    opponent.removeSquare(square)
                                    opponent.removeParitySquare(square)
                                    square.getMidpoint().changeColor('white', other_window)
                                    if not self.remaining_directions:
                                        del self.all_viable_points[
                                            self.last_point]
                                        if self.all_viable_points:
                                            self.last_point = random.choice(self.all_viable_points.keys())
                                            self.remaining_directions = self.all_viable_points[self.last_point]
                                        else:
                                            self.found_target = False
                                    break
                    else:
                        self.turn(opponent, other_window)
