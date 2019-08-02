import copy
from operator import attrgetter


class State(object):
    map = []
    h = 0


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_valid(index, row_size, column_size):
    return (index[0] >= 0 and index[1] >= 0) and (index[0] < row_size and index[1] < column_size)


def up_is_valid(map, boundary, row_size, column_size):
    starting_point = boundary[0]
    up_is_v = is_valid([starting_point[0]-1, starting_point[1]], row_size, column_size)
    up_is_zero = True
    width = boundary[1][1] - boundary[0][1] + 1
    if up_is_v:
        for i in range(width):
            if map[boundary[0][0]-1][boundary[0][1]+i] != 0:
                up_is_zero = False
    return up_is_zero and up_is_v


def right_is_valid(map, boundary, row_size, column_size):
    finishing_point = boundary[1]
    right_is_v = is_valid([finishing_point[0], finishing_point[1]+1], row_size, column_size)
    right_is_zero = True
    height = boundary[0][0] - boundary[1][0] + 1
    if right_is_v:
        for i in range(height):
            if map[boundary[1][0]-i][boundary[1][1]+1] != 0:
                right_is_zero = False
    return right_is_zero and right_is_v


def down_is_valid(map, boundary, row_size, column_size):
    finishing_point = boundary[1]
    down_is_v = is_valid([finishing_point[0]+1, finishing_point[1]], row_size, column_size)
    down_is_zero = True
    width = boundary[1][1] - boundary[0][1] + 1
    if down_is_v:
        for i in range(width):
            if map[boundary[1][0]+1][boundary[1][1]-i] != 0:
                down_is_zero = False
    return down_is_zero and down_is_v


def left_is_valid(map, boundary, row_size, column_size):
    starting_point = boundary[0]
    left_is_v = is_valid([starting_point[0], starting_point[1]-1], row_size, column_size)
    left_is_zero = True
    height = boundary[0][0] - boundary[1][0] + 1
    if left_is_v:
        for i in range(height):
            if map[boundary[0][0]+i][boundary[0][1]-1] != 0:
                left_is_zero = False
    return left_is_zero and left_is_v


def swap_up(start_map, boundary, row_size, column_size):
    starting_point = boundary[0]
    finishing_point = boundary[1]
    map = copy.deepcopy(start_map)
    value = map[starting_point[0]][starting_point[1]]
    for row in range(row_size):
        for column in range(column_size):
            if row == finishing_point[0] and starting_point[1] <= column <= finishing_point[1]:
                map[row][column] = 0
            if row == starting_point[0]-1 and starting_point[1] <= column <= finishing_point[1]:
                map[row][column] = value
    return map


def swap_right(start_map, boundary, row_size, column_size):
    starting_point = boundary[0]
    finishing_point = boundary[1]
    map = copy.deepcopy(start_map)
    value = map[starting_point[0]][starting_point[1]]
    for row in range(row_size):
        for column in range(column_size):
            if column == starting_point[1] and starting_point[0] <= row <= finishing_point[0]:
                map[row][column] = 0
            if column == finishing_point[1]+1 and starting_point[0] <= row <= finishing_point[0]:
                map[row][column] = value
    return map


def swap_down(start_map, boundary, row_size, column_size):
    starting_point = boundary[0]
    finishing_point = boundary[1]
    map = copy.deepcopy(start_map)
    value = map[starting_point[0]][starting_point[1]]
    for row in range(row_size):
        for column in range(column_size):
            if row == starting_point[0] and starting_point[1] <= column <= finishing_point[1]:
                map[row][column] = 0
            if row == finishing_point[0]+1 and starting_point[1] <= column <= finishing_point[1]:
                map[row][column] = value
    return map


def swap_left(start_map, boundary, row_size, column_size):
    starting_point = boundary[0]
    finishing_point = boundary[1]
    map = copy.deepcopy(start_map)
    value = map[starting_point[0]][starting_point[1]]
    for row in range(row_size):
        for column in range(column_size):
            if column == finishing_point[1] and starting_point[0] <= row <= finishing_point[0]:
                map[row][column] = 0
            if column == starting_point[1]-1 and starting_point[0] <= row <= finishing_point[0]:
                map[row][column] = value
    return map


def find_position(start, final, row_size, column_size, pieces):
    position_dict = {}
    pieces_list = list(range(1, pieces+1))
    for row in range(row_size):
        for column in range(column_size):
            if start[row][column] in pieces_list:
                starting_point = [row, column]
                r = row
                c = column
                while is_valid([r, c], row_size, column_size) and start[r][c] == start[row][column]:
                    r += 1
                r -= 1
                while is_valid([r, c], row_size, column_size) and start[r][c] == start[row][column]:
                    c += 1
                c -= 1
                finishing_point = [r, c]
                position_dict[final[row][column]] = [starting_point, finishing_point]
                pieces_list.remove(start[row][column])
    return position_dict


def solve(start_map, final, row_size, column_size, pieces):
    start_position_dict = find_position(start_map, start_map, row_size, column_size, pieces)
    final_position_dict = find_position(start_map, final, row_size, column_size, pieces)
    start = start_map
    while start != final:
        next_states = []
        closed_list = []
        for row in range(row_size):
            for column in range(column_size):
                if start[row][column] != 0:
                    if start[row][column] not in closed_list:
                        closed_list.append(start[row][column])
                        if up_is_valid(start, start_position_dict[start[row][column]], row_size, column_size):  # up
                            if final_position_dict[start[row][column]][0] == [row, column]:
                                continue
                            state = State()
                            state.map = swap_up(start, start_position_dict[start[row][column]], row_size, column_size)
                            state.h = manhattan_distance([row-1, column], final_position_dict[start[row][column]][0])
                            next_states.append(state)
                        if right_is_valid(start, start_position_dict[start[row][column]], row_size, column_size):  # right
                            if final_position_dict[start[row][column]][0] == [row, column]:
                                continue
                            state = State()
                            state.map = swap_right(start, start_position_dict[start[row][column]], row_size, column_size)
                            state.h = manhattan_distance([row, column+1], final_position_dict[start[row][column]][0])
                            next_states.append(state)
                        if down_is_valid(start, start_position_dict[start[row][column]], row_size, column_size):  # down
                            if final_position_dict[start[row][column]][0] == [row, column]:
                                continue
                            state = State()
                            state.map = swap_down(start, start_position_dict[start[row][column]], row_size, column_size)
                            state.h = manhattan_distance([row+1, column], final_position_dict[start[row][column]][0])
                            next_states.append(state)
                        if left_is_valid(start, start_position_dict[start[row][column]], row_size, column_size):  # left
                            if final_position_dict[start[row][column]][0] == [row, column]:
                                continue
                            state = State()
                            state.map = swap_left(start, start_position_dict[start[row][column]], row_size, column_size)
                            state.h = manhattan_distance([row, column-1], final_position_dict[start[row][column]][0])
                            next_states.append(state)
        next_states.sort(key=attrgetter('h'))
        start = next_states[0].map
        print(start)


start = [[0, 1, 1, 0, 0, 2, 2, 0], [0, 1, 1, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 0, 0, 4, 4, 0], [0, 3, 3, 0, 0, 4, 4, 0]]
final = [[0, 2, 2, 0, 0, 4, 4, 0], [0, 2, 2, 0, 0, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 0, 0, 3, 3, 0], [0, 1, 1, 0, 0, 3, 3, 0]]
row = 6
column = 8
pieces = 4
solve(start, final, row, column, pieces)

