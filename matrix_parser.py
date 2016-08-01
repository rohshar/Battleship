from numpy import unravel_index, array, count_nonzero, copy


priority = array([[74196, 109035, 137024, 150981, 157879, 157764, 150919, 137176, 109538, 74055],
[108858, 140443, 165679, 179001, 184821, 184658, 178049, 166097, 141075, 108815],
[137268, 166265, 189731, 200986, 205842, 206370, 200037, 189694, 166912, 136826],
[150263, 177824, 200373, 211421, 217097, 217136, 210763, 200318, 178564, 150356],
[157580, 184450, 206297, 216509, 222062, 221901, 216176, 205896, 184874, 157448],
[157600, 184688, 206384, 216286, 221785, 222131, 216755, 206393, 184981, 158028],
[150967, 177706, 200102, 210474, 216198, 216569, 210750, 200289, 178045, 151015],
[137030, 166304, 189097, 200880, 205992, 206365, 200397, 188747, 165632, 137736],
[108732, 140316, 165339, 178677, 184015, 184461, 178537, 165708, 140464, 109730],
[74171, 109521, 137236, 150839, 157256, 156760, 150067, 136453, 108910, 74180]])

def getSquareOrdering(d_list):
    double_list = array(d_list)
    priority_queue = []
    for i in range(10):
        for j in range(10):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                double_list[i][j] = 0

    while (count_nonzero(double_list) != 0):
        high_val = unravel_index(double_list.argmax(), double_list.shape)
        double_list[high_val[0]][high_val[1]] = 0
        priority_queue.append((high_val[0] + 1, high_val[1] + 1))

    return priority_queue


if __name__ == '__main__':
    getSpotOrdering()