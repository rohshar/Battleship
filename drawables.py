from graphics import *


class GridPoint:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.p = None

    def draw(self, graphics_window):
        self.p = Circle(Point(3 + 2 * self.x, 2 + 2 * self.y), .2)
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