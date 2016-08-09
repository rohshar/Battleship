import sys
sys.path.append("..")
from drawables import GridPoint, GridSquare, Ship
from test_players import ComputerPlayer


player1_wins = 0
player2_wins = 0
w, h = 10, 10 
ship_placement = [[0 for x in range(w)] for y in range(h)] 
def main():
    global player1_wins
    global player2_wins

    size = 300
    option = 3
    diff = 5 
    diff2 = 4

    player1 = ComputerPlayer(diff) 
    player2 = ComputerPlayer(diff2) 

    window = None
    player1.drawBoard(window)
    player1.placeShips(window)
    p1_points = player1.getOccupiedPoints()

    window2 = None
    player2.drawBoard(window2)
    player2.placeShips(window2)
    p2_points = player2.getOccupiedPoints()

    
    while not player1.hasLost() and not player2.hasLost():
        player1.turn(player2, window2)
        player2.turn(player1, window)

    if player1.hasLost():
        player2_wins += 1
    else:
        player1_wins += 1

if __name__ == '__main__':
    for i in range(5):
        print(i)
        main()
    print('')

    print(str(player1_wins) + ": player1")    
    print(str(player2_wins) + ": player2")
    with open("statistics.txt", "a") as myfile:
        myfile.write(str(player1_wins) + ": probability matrix guessing, directional surrounding hunt mode\n")
        myfile.write(str(player2_wins) + ": parity guessing, directional surrounding hunt mode\n\n")

