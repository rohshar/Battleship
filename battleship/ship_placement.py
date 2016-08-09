from drawables import GridPoint, GridSquare, Ship
from players_test import ComputerPlacer


def placeShipsTest(guesses, ship_lengths, ship_placement):
    size = 300
    diff = 4 
    diff2 = 3

    placer1 = ComputerPlacer(diff) # probability matrix guessing, one dirction targeting
    placer2 = ComputerPlacer(diff2) # parity guessing, on direction targeting

    window = None
    placer1.drawBoard(window)
    check = placer1.theoreticalShips(window, ship_lengths, guesses)
    p1_points = placer1.getOccupiedPoints()

    window2 = None
    placer2.drawBoard(window2)
    check2 = placer2.theoreticalShips(window2, ship_lengths, guesses)
    p2_points = placer2.getOccupiedPoints()

    if check == False or check2 == False:
        return False
    
    for point in p1_points:
        ship_placement[point[0] - 1][point[1] - 1] += 1
    for point in p2_points:
        ship_placement[point[0] - 1][point[1] - 1] += 1

def getPlacementNumbers(guesses, ship_lengths):
    w, h = 10, 10 
    ship_placement = [[0 for x in range(w)] for y in range(h)]
    for i in range(100):
        check = placeShipsTest(guesses, ship_lengths, ship_placement)
        if check == False:
            return None

    return ship_placement
