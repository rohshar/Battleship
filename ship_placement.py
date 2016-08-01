from drawables import GridPoint, GridSquare, Ship
from players_test import ComputerPlayer


w, h = 10, 10 
ship_placement = [[0 for x in range(w)] for y in range(h)] 
def place_ships(guesses, ship_lengths):
    global ship_placement

    size = 300

    diff = 4 
    diff2 = 3

    player1 = ComputerPlayer(diff) # probability matrix guessing, one dirction targeting
    player2 = ComputerPlayer(diff2) # parity guessing, on direction targeting

    window = None

    player1.drawBoard(size, window)
    player1.theoreticalShips(window, ship_lengths, guesses)
    p1_points = player1.getOccupiedPoints()

    window2 = None
    player2.drawBoard(size, window2)
    player2.theoreticalShips(window2, ship_lengths, guesses)
    p2_points = player2.getOccupiedPoints()
    
    
    for point in p1_points:
        ship_placement[point[0] - 1][point[1] - 1] += 1
    for point in p2_points:
        ship_placement[point[0] - 1][point[1] - 1] += 1




def get_placement_numbers(guesses, ship_lengths):
    for i in range(100):
        place_ships(guesses, ship_lengths)
    return ship_placement

    #print(str(player1_wins) + ": player1")    
    #print(str(player2_wins) + ": player2")
    #with open("statistics.txt", "a") as myfile:
    #    myfile.write(str(player1_wins) + ": probability matrix guessing, directional surrounding hunt mode\n")
    #    myfile.write(str(player2_wins) + ": parity guessing, directional surrounding hunt mode\n\n")

