from random import randint
from graphics import *

class GridPoint:
	def __init__(self, x, y, size):
		self.x = x
		self.y = y
		self.size = size

	def draw(self, graphics_window):
		p = Point(self.x * self.size / 10.0 + self.size * 11 / 200.0, self.y * self.size / 10.0 + self.size * 73 / 200.0)
		p.draw(graphics_window)


class GridSquare:
	def __init__(self, top_x, top_y, size):
		self.top_x = top_x
		self.top_y = top_y
		self.size = size

	def draw(self, graphics_window):
		p1 = Point(self.top_x * self.size / 10.0 + self.size / 100.0, self.top_y * self.size / 10.0 + self.size * 31 / 100.0)
		p2 = Point(self.top_x * self.size / 10.0 + self.size * 11 / 100.0, self.top_y * self.size / 10.0 + self.size * 41 / 100.0)
		r = Rectangle(p1, p2)
		r.draw(graphics_window)


def main():
	while True:
		size = input('How large do you want the BattleShip window to be? (from 250-550 px) ')
		if (250 <= size <= 550):
				break
		else:
			print('Your size must be between 250 and 550! Please try again.\n')

	window = GraphWin("BattleShip", size * 141 / 100.0, size * 131 / 100.0)
	for i in range(10):
		for j in range(10):
			gp = GridPoint(i, j, size)
			gp.draw(window)

	for i in range(10):
		for j in range(10):
			gs = GridSquare(i, j, size)
			gs.draw(window)


	window.getMouse()
	window.close()


if __name__ == '__main__':
    main()