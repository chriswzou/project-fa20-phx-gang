import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys

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
def solve(G, s):
	
	max_happiness = 0.0
	best_sol = {}

	num_students = len(list(G.nodes))
	for num_rooms in range(1, num_students+1):
		all_sols = construct_sol(list(range(num_students)), num_rooms)

		for sol in all_sols:
			k = len(set(sol.values()))
			
			if is_valid_solution(sol, G, s, k):
				happy = calculate_happiness(sol, G)
				if happy > max_happiness:
					max_happiness = happy
					best_sol = sol
					print(max_happiness)
	return best_sol, len(set(best_sol.values()))

# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G, s = read_input_file(path)
    D, k = solve(G, s)
    assert is_valid_solution(D, G, s, k)
    print("Total Happiness: {}".format(calculate_happiness(D, G)))
    # write_output_file(D, 'out/test.out')


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