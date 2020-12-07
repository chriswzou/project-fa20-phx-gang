import networkx as nx
from parse import read_input_file, write_output_file
from utils import *
import sys
import random
from collections import defaultdict
import re

# This function outlines the recurrence relation if you want to place n students in k breakout
# rooms such that every breakout room has at least 1 student
def sol_breakout(n, k):
	if k == 1 or k == n or n == 1:
		return 1

	return k * sol_breakout(n-1, k) + sol_breakout(n-1, k-1)

# This function calculates the number of possible solutions for a given number of students
# Essentially, n students can be placed into anywhere from 1 to n breakout rooms
def num_sols(n):
	res = 0
	for k in range(1, n+1):
		res += sol_breakout(n, k)

	return res

# This function constructs solutions given a list of students and a number of possible rooms
# Logic here is strongly based on the original recurrence relation. The function will return
# a list of dictionaries, where each dictionary is a valid solution using exactly ROOMS number
# of rooms.
def construct_sol(students, rooms):
	if rooms == 1 or len(students) == 1:
		return [{s:0 for s in students}]
	if rooms == len(students):
		return [{s:s for s in students}]
	
	result = []
	student = students[-1]
	copy = students[:]
	copy.remove(student)

	existing_room_sols = construct_sol(copy, rooms)
	for er_sol in existing_room_sols:
		possible_rooms = set(er_sol.values())
		for room in possible_rooms:
			toAdd = dict(er_sol)
			toAdd[student] = room
			result.append(toAdd)

	new_room_sols = construct_sol(copy, rooms-1)
	for nr_sol in new_room_sols:
		toAdd = dict(nr_sol)
		toAdd[student] = rooms-1
		result.append(toAdd)

	return result

# Finally, our brute force solver. Iterate through the number of possible rooms, and for
# each number construct all solutions that use exactly this number of rooms. Check each
# of these solutions to see what happens.

# Logic:
# Instead of constructing all solutions based on the full set of people, construct
# all solutions based off of groups of 10 at a time.


def merge(d1, d2):
    n_rooms_d1 = len(set(d1.values()))
    n_rooms_d2 = len(set(d2.values()))
    return_dict = {}
    for item in d1:
        return_dict[item] = d1[item]
    for item in d2:
        return_dict[item] = d2[item] + n_rooms_d1
    return return_dict

def solve(G, s):
    # given a subgraph of 10 students, solve by brute force, returning a
    # student_to_room mapping and the number of rooms
    max_happiness = 0.0
    best_sol = {}
    num_students = len(list(G.nodes))
    list_student_nums = [i for i in range(num_students)]
    random.shuffle(list_student_nums)
    solns = defaultdict(list)
    
    # construct all of the ways to place 10 students at a time into rooms.
    counter = 0
    while len(list_student_nums) != 0:
        curr_student_list = []
        subset_sols = [] # list of dicts to put these 10 students into <= 10 rooms.
        for i in range(10):
            curr_student_list.append(list_student_nums.pop())
        for num_rooms in range(1, 11):
            subset_sols.append(construct_sol(curr_student_list, num_rooms))
        solns[counter] = subset_sols
        counter += 1
    # We now have a dictionary of the following form:
    # {
    #   0: ways to put first 10 in rooms 0 - 9
    #   1: ways to put second 10 in rooms 0 - 9
    #   etc...
    # }
    # We need to retrieve all pairwise combinations between the two lists
    # For each pairwise combination, merge the dictionaries, test the resulting soln,
    # And commit that soln to be the best soln if it's better than the existing one.
    for i in solns:
        for j in solns[0]:
            for k in solns[1]:
                soln = merge(solns[0][j], solns[1][k])
                n_rooms = len(set(soln.values()))
                if is_valid_solution(soln, G, s, n_rooms):
                    happy = calculate_happiness(soln, G)
                    if happy > max_happiness:
                        max_happiness = happy
                        best_sol = soln
    return best_sol, len(set(best_sol.values()))

# Here's an example of how to run your solver.

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