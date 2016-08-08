from graphics import *
from drawables import GridPoint, GridSquare, Ship
from parse_matrix import getSpotOrdering
from matrix_parser import getSquareOrdering
import ship_placement
import random


class ShipPlacer:
    def __init__(self):
        self.all_squares = []

    def drawBoard(self, window):
        for i in range(10):
            for j in range(10):
                gp = GridPoint(i, j)
                gs = GridSquare(i, j)
                gs.setMidpoint(gp)
                self.all_squares.append(gs)


class ComputerPlacer(ShipPlacer):
    def __init__(self, difficulty):
        self.all_computer_ships = []
        self.all_occupied_points = []

        ShipPlacer.__init__(self)

    def getOccupiedPoints(self):
        return self.all_occupied_points

    def theoreticalShips(self, window, ship_lengths, occupied_points):
        other_ships = []
        for length in ship_lengths:
            ship = self.placeShip(length, other_ships, occupied_points)
            if ship == None:
                return False
            other_ships.append(ship)

        for ship in self.all_computer_ships:
            self.all_occupied_points += ship.getPoints()

        return True

    def placeShip(self, length, other_ships, occupied_points):
        counter = 0
        while True:
            counter += 1
            overlapping = False
            valid = True
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
            if occupied_points is not None:
                for point in occupied_points:
                    if point in ship.getPoints():
                        valid = False
            if overlapping == False and valid == True:
                self.all_computer_ships.append(ship)
                return ship
            if counter == 100:
                return None


