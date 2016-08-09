from graphics import *


class GridPoint:
    """
    Represents the center of each GridSquare and is used to display a hit or miss.
    """
    def __init__(self, x, y):
        """
        :param x: The x coordinate of the point
        :param y: The y coordinate of the point
        :return:
        """
        self.x = x
        self.y = y
        self.p = None

    def draw(self, graphics_window):
        """
        :param graphics_window: The window to be drawn in
        :return:
        """
        self.p = Circle(Point(3 + 2 * self.x, 2 + 2 * self.y), .2)
        self.p.draw(graphics_window)

    def changeColor(self, color, graphics_window):
        """
        :param color: The color that the point needs to change to
        :param graphics_window: The window to be drawn in
        :return:
        """
        self.p.setFill(color)
        self.p.undraw()
        self.p.draw(graphics_window)


class GridSquare:
    """
    Represents each location that a ship can be placed on the grid.
    """
    def __init__(self, top_x, top_y):
        """
        :param top_x: The upper x coordinate of the square
        :param top_y: The upper y coordinate of the square
        :return:
        """
        self.top_x = top_x
        self.top_y = top_y
        self.r = None
        self.coords = (top_x + 1, 10 - top_y)
        self.midpoint = None

    def draw(self, graphics_window):
        """
        :param graphics_window: The window to be drawn in
        :return:
        """
        p1 = Point(2 * (self.top_x + 1), 2 * (self.top_y) + 1)
        p2 = Point(2 * (self.top_x + 2), 2 * (self.top_y) + 3)
        self.r = Rectangle(p1, p2)
        self.r.draw(graphics_window)

    def within(self, point):
        """
        Checks if the user has clicked within the GridSquare
        :param point: The user's click
        :return:
        """
        p_x = point.getX()
        p_y = point.getY()
        if (2 * (self.top_x + 1)) <= p_x <= (2 * (self.top_x + 2)):
            if (2 * (self.top_y) + 1) <= p_y <= (2 * (self.top_y) + 3):
                return True

    def getRectangle(self):
        """
        :return: The rectange graphics object
        """
        return self.r

    def getCoords(self):
        """
        :return: The coordinates of the square
        """
        return self.coords

    def setMidpoint(self, point):
        """
        :param point: The GridPoint corresponding to the GridSquare
        :return:
        """
        self.midpoint = point

    def getMidpoint(self):
        """
        :return: The GridPoint corresponding to the GridSquare
        """
        return self.midpoint


class Ship:
    """
    Represents each ship that is placed in the game.
    """
    def __init__(self, length, coord1, coord2, increment):
        """
        :param length: The length of the ship
        :param coord1: The coordinate of the beginning of the ship
        :param coord2: The coordinate of the end of the ship
        :param increment: The direction in which the ship is to be created
        :return:
        """
        self.length = length
        self.coord1 = coord1
        self.coord2 = coord2
        self.increment = increment
        self.all_points = []
        for i in range(length):
            self.all_points.append((self.coord1[0] + increment[0] * i, self.coord1[1] + increment[1] * i))

    def getPoints(self):
        """
        :return: All of the points that the ship is on top of
        """
        return self.all_points

    def getLength(self):
        """
        :return: The length of the ship
        """
        return self.length

    def checkOverlap(self, other_ship):
        """
        Checks if the ship overlaps with another ship
        :param other_ship: The ship to be checked against
        """
        other_points = other_ship.getPoints()
        for point in self.getPoints():
            if point in other_points:
                return True
        return False

    def draw(self, graphics_window):
        """
        :param graphics_window: The window the ship will be drawn on
        """
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