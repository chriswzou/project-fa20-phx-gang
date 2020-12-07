import networkx as nx
from parse import read_input_file, write_output_file
from utils import *
import sys
import random
import re
from collections import defaultdict
import pprint

# Basic idea: 1. generate a random number of rooms
#             2. randomly place students into said number of rooms
#             3. check the solution, if valid --> proceed, if not, repea

pp = pprint.PrettyPrinter(indent=4)

def generate_solution(n_students):
    # generate a random number of rooms
    if n_students == 50:
        n_rooms = random.randint(4, 30)
    elif n_students == 20:
        n_rooms = random.randint(4, 15)
    else:
        n_rooms = random.randint(1, n_students)

    # randomly place students into the rooms
    room_to_students = defaultdict(list)

    for student in range(n_students):
        rand_room = random.randint(0, n_rooms - 1)
        room_to_students[rand_room].append(student)

    curr_room = 0
    revised_dict = defaultdict(list)
    for key in room_to_students:
        if len(room_to_students[key]) == 0:
            continue
        revised_dict[curr_room] = room_to_students[key]
        curr_room += 1
    n_rooms_filled = len(revised_dict)

    # return our student_to_room dictionary
    students_to_rooms = convert_dictionary(revised_dict)
    return students_to_rooms, n_rooms_filled, revised_dict

def update_solution(solution, n_rooms, s, G, room_to_students):
    # assess the current state
    curr_happiness = calculate_happiness(solution, G)
    best_soln = [solution, n_rooms]

    # optimization strategy 1: move students into largest room
    largest_room = max(room_to_students, key=lambda k: len(room_to_students[k]))
    for student in solution:
        if solution[student] != largest_room:
            new_soln = solution.copy()
            new_soln[student] = largest_room
            if is_valid_solution(new_soln, G, s, n_rooms): # number of rooms may change!!
                new_happiness = calculate_happiness(new_soln, G)
                if new_happiness > curr_happiness:
                    curr_happiness = new_happiness
                    best_soln[0] = new_soln # number of rooms may change!!

    return best_soln[0], best_soln[1]

def solve(G, s):
    num_students = len(list(G.nodes))
    list_solutions = []
    n_iterations = 0
    while (len(list_solutions) < 1000 and n_iterations < 10000) or len(list_solutions) == 0:
        soln, k, room_to_students = generate_solution(num_students)
        if is_valid_solution(soln, G, s, k):
            list_solutions.append([soln, k, room_to_students])
        n_iterations += 1        
    best_solution = max(list_solutions, key=lambda s: calculate_happiness(s[0], G))
    updated_soln, k = update_solution(best_solution[0], best_solution[1], s, G, best_solution[2])
    return updated_soln, k

# Usage: python3 solver.py test.in location.out

if __name__ == '__main__':
    assert len(sys.argv) == 3
    path = sys.argv[1]
    out = sys.argv[2]
    print(path, out)
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    write_output_file(D, out)


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
