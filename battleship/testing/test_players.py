import sys
sys.path.append("..")
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

    def drawBoard(self, window):

        for i in range(10):
            for j in range(10):
                gp = GridPoint(i, j)
                gs = GridSquare(i, j)
                gs.setMidpoint(gp)
                self.all_squares.append(gs)
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self.parity_squares.append(gs)


    def removeShip(self, length):
        self.ships_left.remove(length)

    def getShipLengthsLeft(self):
        return self.ships_left

class ComputerPlayer(Player):
    def __init__(self, difficulty):
        self.all_computer_ships = []
        self.all_occupied_points = []
        self.hit_points = []
        self.difficulty = difficulty
        self.all_opponent_guesses = []

        self.found_target = False
        self.last_point = None
        self.remaining_directions = None
        self.all_viable_points = {}

        self.naive_ordering = getSpotOrdering()
        self.can_theorize = True

        Player.__init__(self)

    def placeShips(self, window):
        comp5 = self.placeShip(5, None)
        #comp5.draw(window)

        comp4 = self.placeShip(4, [comp5])
        #comp4.draw(window)

        comp3_1 = self.placeShip(3, [comp5, comp4])
        #comp3_1.draw(window)

        comp3_2 = self.placeShip(3, [comp5, comp4, comp3_1])
        #comp3_2.draw(window)

        comp2 = self.placeShip(2, [comp5, comp4, comp3_1, comp3_2])
        #comp2.draw(window)

        for ship in self.all_computer_ships:
            self.all_occupied_points += ship.getPoints()

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

    def getShips(self):
        return self.all_computer_ships

    def sinkShip(self, ship):
        self.all_computer_ships.remove(ship)

    def getParitySquares(self):
        return self.parity_squares

    def removeParitySquare(self, square):
        if square in self.parity_squares:
            self.parity_squares.remove(square)

    def getGuesses(self):
        return self.all_opponent_guesses

    def addGuess(self, guess):
        self.all_opponent_guesses.append(guess)

    def nextPriorityGuess(self):
        return self.naive_ordering.pop(0)

    def hitAction(self, square, opponent, other_window):
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

        #random guessing
        if self.difficulty == 1:
            square = random.choice(opponent.getAllSquares())
            opponent.removeSquare(square)
            opponent_points = opponent.getOccupiedPoints()
            if square.getCoords() in opponent_points:
                opponent.hit(square.getCoords())

        #random guessing until a hit, then targets points blindly around it
        elif self.difficulty == 2:
            if not self.found_target:
                square = random.choice(opponent.getAllSquares())
                opponent.removeSquare(square)
                opponent_points = opponent.getOccupiedPoints()
                opponent.addGuess(square.getCoords())
                if square.getCoords() in opponent_points:
                    self.hitAction(square, opponent, other_window)
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

        #parity guessing, then targets points around it
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

        #parity guessing, then targets points around it, when it gets a second hit, goes in that direction
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

        #guess based on most likely squares, target in one direction
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


        #calculate density matricies based on ships left and points guessed, and guess based on that
        elif self.difficulty == 5:
            if not self.found_target:
                if opponent.getParitySquares() and self.can_theorize:
                    numbers_mtx = getPlacementNumbers(opponent.getGuesses(), opponent.getShipLengthsLeft())
                    if numbers_mtx == None:
                        self.can_theorize = False
                        self.turn(opponent, other_window)
                        return
                    priority_list = getSquareOrdering(numbers_mtx)
                    #for n in numbers_mtx:
                    #    print(n)
                    #print(priority_list)
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
                                    opponent.hit(square.getCoords())
                                    self.all_viable_points[self.last_point] = [[-1 * direction[0], -1 * direction[1]]]
                                    self.last_point = square.getCoords()
                                    self.remaining_directions = [direction]
                                    self.found_target = True
                                    self.all_viable_points[self.last_point] = self.remaining_directions
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
        