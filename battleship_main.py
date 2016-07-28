from drawables import GridPoint, GridSquare, Ship
from players import HumanPlayer, ComputerPlayer
from graphics import *


def main():
    while True:
        size = input('How large do you want the BattleShip window to be? (from 150-550 px) ')
        if (150 <= size <= 550):
            break
        else:
            print('Your size must be between 150 and 550! Please try again.\n')

    while True:
        diff = input('What CPU level do you want? (1: easy, 2: medium, 3: hard) ')
        if (diff == 1) or (diff == 2) or (diff == 3):
            break
        else:
            print('You must choose an appropriate difficulty!\n')

    user = HumanPlayer()
    computer = ComputerPlayer(diff)

    window = GraphWin("User BattleShip", size * 141 / 100.0, size * 131 / 100.0)
    window.setCoords(0, 0, 28, 28)
    user.drawBoard(size, window)
    user.placeShips(window)

    window2 = GraphWin("Computer BattleShip", size * 121 / 100.0, size * 111 / 100.0)
    window2.setCoords(0, 0, 23, 23)
    computer.drawBoard(size, window2)
    computer.placeShips(window2)

    while not user.hasLost() and not computer.hasLost():
        user.turn(computer, window2)
        computer.turn(user, window)

    print('Game is finished!\n\n')
    if window.getMouse() or window2.getMouse():
        window.close()
        window2.close()

if __name__ == '__main__':
    main()