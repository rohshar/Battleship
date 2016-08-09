from graphics import *
from drawables import GridPoint, GridSquare, Ship
from parse_matrix import getSpotOrdering
from matrix_parser import getSquareOrdering
from ship_placement import getPlacementNumbers
import random


class Player:
    """
    Represents the parent Player class.
    """
    def __init__(self):
        self.all_squares = []
        self.parity_squares = []
        self.ships_left = [5, 4, 3, 3, 2]
        self.all_opponent_guesses = []
        self.all_occupied_points = []
        self.hit_points = []
        self.all_ship_objects = []

    def drawBoard(self, window):
        """
        Draws the board for the player, and initializes all of the GridSquares
        :param window: The graphics window to draw the board on
        :return:
        """
        rect = Rectangle(Point(2, 1), Point(22, 21))
        rect.setFill("deep sky blue")
        rect.draw(window)

        for i in range(10):
            for j in range(10):
                gp = GridPoint(i, j)
                gp.draw(window)
                gs = GridSquare(i, j)
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
        """
        Remove the ship length from the ships left
        :param length: The length of the ship to be removed
        :return:
        """
        self.ships_left.remove(length)

    def getShipLengthsLeft(self):
        """
        Get the lengths of the ships not sunk
        :return:
        """
        return self.ships_left

    def getParitySquares(self):
        """
        Get every other GridSquare in the player's grid
        :return: All of the parity squares not yet guessed
        """
        return self.parity_squares

    def removeParitySquare(self, square):
        """
        Remove the parity square from the list if it has been guessed
        :param square: The square to be removed
        """
        if square in self.parity_squares:
            self.parity_squares.remove(square)

    def getGuesses(self):
        """
        :return: All of the guesses that haves been made
        """
        return self.all_opponent_guesses

    def addGuess(self, guess):
        """
        :param guess: The guess to be added to the list of guesses
        """
        self.all_opponent_guesses.append(guess)

    def getAllSquares(self):
        """
        Get all of the GridSquares not yet guessed
        :return: All of the squares not yet guessed
        """
        return self.all_squares

    def removeSquare(self, square):
        """
        Remove the  square from the list if it has been guessed
        :param square: The square to be removed
        """
        self.all_squares.remove(square)

    def getOccupiedPoints(self):
        """
        :return: All of the points where there is a ship
        """
        return self.all_occupied_points

    def hit(self, location):
        """
        Add the coordinates to a list of other hits
        :param location: The coordinates of the place where the player hit a ship
        """
        self.hit_points.append(location)

    def getShips(self):
        """
        :return: All remaining ship object
        """
        return self.all_ship_objects

    def sinkShip(self, ship):
        """
        :param ship: The ship that was just fully sunk
        """
        self.all_ship_objects.remove(ship)

    def hasLost(self):
        """
        Checks if all of the player's ships have been sunk
        """
        if set(self.all_occupied_points) == set(self.hit_points):
            return True
        return False


class HumanPlayer(Player):
    """
    Represents the human player class.
    """
    def __init__(self):

        Player.__init__(self)

    def placeShips(self, window):
        """
        Allows the user to place their own ships sequentially
        :param window: The graphics window to draw the board on
        :return:
        """
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
        """
        Places each individual ships based on length and obstacles
        :param window: The graphics window to draw the board on
        :param length: The length of the ship
        :param other_ships: The ships that cannot be overlapped
        :return: The valid ship object
        """
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
        """
        Allows the user to click and take their turn
        :param opponent: The person or computer the user is playing against
        :param other_window: The user's opponent's graphics window
        """
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
    """
    Represents the computer player class.
    """
    def __init__(self, difficulty):
        """
        :param difficulty: The difficulty of play of the CPU
        :return:
        """
        self.difficulty = difficulty
        self.found_target = False
        self.last_point = None
        self.remaining_directions = None
        self.all_viable_points = {}
        self.naive_ordering = getSpotOrdering()
        self.can_theorize = True

        Player.__init__(self)

    def placeShips(self, window):
        """
        Places all of the computer ships without drawing them
        :param window: The graphics window to draw the board on
        :return:
        """
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
        """
        Places each individual ships based on length and obstacles
        :param length: The length of the ship
        :param other_ships: The ships that cannot be overlapped
        :return: The valid ship object
        """
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
        """
        Gets the next most likely guess based on an initial probability matrix (for difficulty 4)
        :return: The coordinates of the next guess
        """
        return self.naive_ordering.pop(0)

    def hitAction(self, square, opponent, other_window):
        """
        Used in turn for non-discriminatory hunt mode, where the computer checks all around a hit
        :param square: The square that was hit
        :param opponent: The player being played against
        :param other_window: The window with the other player's ships
        """
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
        """
        Used when the stack of all points that need to be checked around has a key with an empty
        value and needs to be removed
        :param opponent: The player being played against
        :param other_window: The window with the other player's ships
        """
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

    def nextValidPoint(self, opponent, other_window):
        """
        Finds the next point that has not been guessed around a hit
        :param opponent: The player being played against
        :param other_window: The window with the other player's ships
        """
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
                    return next_point, direction
            except:
                self.cleanDictionary(opponent, other_window)
                return None, None

        return None, None

    def turn(self, opponent, other_window):
        """
        The method where the computer player picks the best next move based on the difficulty it is
        being played at. There are 6 difficulties, one of which is obscured from the user, and they are
        all explained before the logic of each.
        :param opponent: The person or computer the user is playing against
        :param other_window: The user's opponent's graphics window
        """
        #Entirely random guessing with no intelligent logic
        if self.difficulty == 1:
            square = random.choice(opponent.getAllSquares())
            opponent.removeSquare(square)
            opponent_points = opponent.getOccupiedPoints()
            if square.getCoords() in opponent_points:
                square.getMidpoint().changeColor('red', other_window)
                opponent.hit(square.getCoords())
            else:
                square.getMidpoint().changeColor('white', other_window)
     
        #Random guessing until the CPU gets a hit, then it switches to hunt mode, where it targets
        #all points around the hit point
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
                next_point, direction = self.nextValidPoint(opponent, other_window)
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
                                        del self.all_viable_points[self.last_point]
                                        if self.all_viable_points:
                                            self.last_point = random.choice(self.all_viable_points.keys())
                                            self.remaining_directions = self.all_viable_points[self.last_point]
                                        else:
                                            self.found_target = False
                                    break
                    else:
                        self.turn(opponent, other_window)

        #Parity guessing (every other GridSquare) until the CPU gets a hit, then it switches to hunt
        #mode, where it targets all points around the hit point
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
                next_point, direction = self.nextValidPoint(opponent, other_window)
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
                                            self.remaining_directions = self.all_viable_points[self.last_point]
                                        else:
                                            self.found_target = False
                                    break
                    else:
                        self.turn(opponent, other_window)

        
        #Parity guessing (every other GridSquare) until the CPU gets a hit, then it switches to hunt
        #mode, where it targets points around the hit. When it gets a second hit in any direction, the
        #computer then targets points along that line
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
                next_point, direction = self.nextValidPoint(opponent, other_window)
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

        #Guessing based on most likely squares as determined by an initial probability matrix. After a hit
        #it targets points around the hit and when it gets a second hit in any direction, the computer then
        #targets points along that line
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
                next_point, direction = self.nextValidPoint(opponent, other_window)
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

        #Guessing based on probability density matrices that are calculated each turn based on available space.
        #After a hit it targets points around the hit and when it gets a second hit in any direction, the
        #computer then targets points along that line
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
                next_point, direction = self.nextValidPoint(opponent, other_window)
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
                                            opponent.removeShip(ship.getLength())
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
