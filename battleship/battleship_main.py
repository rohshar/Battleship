from drawables import GridPoint, GridSquare, Ship
from players import HumanPlayer, ComputerPlayer
from intro_gui_utils import start, instruct, SampleApp
from graphics import *

def main():
    """
    Contains the logic that gets user input and executes the actual BattleShip game.
    """
    while True:
        choice = input('Text input interface (1) or GUI input interface (2)? ')
        if (choice == 1) or (choice == 2):
            break
        else:
            print('You much choose 1 or 2! Please try again.\n')


    if (choice == 1):
        while True:
            size = input('How large do you want the BattleShip window to be? (from 150-550 px) ')
            if (150 <= size <= 550):
                break
            else:
                print('Your size must be between 150 and 550! Please try again.\n')

        while True:
            option = input('Do you wanna play: player vs. player (1), player vs. CPU (2), CPU vs. CPU (3) ')
            if (option == 1) or (option == 2) or (option == 3):
                break
            else:
                print('You must choose an appropriate option!\n')

        while True:
            if option == 2:
                diff = input('What CPU level do you want? (1: very easy, 2: easy, 3: medium, 4: hard, 5: very hard) ')
                if (1 <= diff <= 5):
                    break
                else:
                    print('You must choose an appropriate difficulty!\n')
            if option == 3:
                diff = input('What CPU level do you want for the first CPU? (1: very easy, 2: easy, 3: medium, 4: hard, 5: very hard) ')
                diff2 = input('What CPU level do you want for the second CPU? (1: very easy, 2: easy, 3: medium, 4: hard, 5: very hard) ')
                if (1 <= diff <= 5) and (1 <= diff2 <= 5):
                    break
                else:
                    print('You must choose appropriate difficulties!\n')
            break
    else:
        check = start()
        if check:
            app = SampleApp()
            app.mainloop()
            size = app.size
            option = app.option
            diff = app.diff
            diff2 = 5
        else:
            instruct()
            main()

    if option == 1:
        player1 = HumanPlayer()
        player2 = HumanPlayer()
    if option == 2:
        player1 = HumanPlayer()
        player2 = ComputerPlayer(diff)
    if option == 3:
        player1 = ComputerPlayer(diff)
        player2 = ComputerPlayer(diff2)

    window = GraphWin("Player 1 BattleShip", size * 141 / 100.0, size * 131 / 100.0)
    window.setCoords(0, 0, 28, 28)
    player1.drawBoard(window)
    player1.placeShips(window)

    window2 = GraphWin("Player 2 BattleShip", size * 121 / 100.0, size * 111 / 100.0)
    window2.setCoords(0, 0, 23, 23)
    player2.drawBoard(window2)
    player2.placeShips(window2)

    while not player1.hasLost() and not player2.hasLost():
        player1.turn(player2, window2)
        if (option == 3):
            time.sleep(.2)
        player2.turn(player1, window)
        if (option == 3):
            time.sleep(.2)

    print('\nGame is finished!')
    if player1.hasLost():
        print('Player 2 won!\n\n')
    else:
        print('Player 1 won!\n\n')

    if window.getMouse() or window2.getMouse():
        window.close()
        window2.close()

if __name__ == '__main__':
    main()