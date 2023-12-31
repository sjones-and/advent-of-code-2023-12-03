#!/usr/bin/env python3

import os
from time import perf_counter_ns

data = []
max_x = 0
max_y = 0

adjacencies = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

def get_symbol_locations(y):
    locations = []
    for x in range(max_x):
        if not (data[y][x] == '.' or data[y][x].isnumeric()):
            locations.append(x)
    return locations

def get_adjacent_locations(location):
    adjacent_locations = [(location[0]+offset[0], location[1]+offset[1]) for offset in adjacencies]
    return [adj for adj in adjacent_locations if adj[0] >= 0 and adj[1] >= 0 and adj[0] < max_x and adj[1] < max_y]

def get_number_coords_at(location):
    start_x = location[0]
    end_x = location[0]
    for x in range(start_x, -1, -1):
        if data[location[1]][x].isnumeric():
            start_x = x
        else:
            break
    for x in range(end_x, max_x, 1):
        if data[location[1]][x].isnumeric():
            end_x = x
        else:
            break
    return ((start_x, end_x),location[1])

def get_adjacent_numbers(location):
    numbers = set()
    for adj in get_adjacent_locations(location):
        if data[adj[1]][adj[0]].isnumeric():
            numbers.add(get_number_coords_at(adj))
    return numbers

def get_number_value_at(location):
    return int(data[location[1]][location[0][0]:(location[0][1]+1)])

def answer(input_file):
    start = perf_counter_ns()
    global max_x, max_y, data
    with open(input_file, "r") as input:
        data = input.read().split('\n')

    symbol_locations = set()
    max_x = len(data[0])
    max_y = len(data)

    for y in range(max_y):
        symbol_locations.update(set([(x,y) for x in get_symbol_locations(y)]))

    number_locations = set()
    for symbol in symbol_locations:
        adjacent_numbers = get_adjacent_numbers(symbol)
        number_locations.update(adjacent_numbers)

    answer = sum([get_number_value_at(location) for location in number_locations])
    end = perf_counter_ns()

    print(f'The answer is: {answer}')
    print(f'{((end-start)/1000000):.2f} milliseconds')

input_file = os.path.join(os.path.dirname(__file__), "input")
answer(input_file)
