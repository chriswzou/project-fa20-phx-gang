import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys


def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """
    if G.size(weight='stress') <= s:
        return {t:0 for t in list(G.nodes)}, 1

    max_happiness = 0.0
    best_d = {}
    for node in list(G.nodes):
        best_d[node] = node

    # Write out every single solution. Check each solution's validity. If valid, compute happiness.
    n = len(list(G.nodes))
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    for e in range(n):
                        for f in range(n):
                            for g in range(n):
                                for h in range(n):
                                    for i in range(n):
                                        for j in range(n):

                                            sol = {
                                            0: a,
                                            1: b,
                                            2: c,
                                            3: d,
                                            4: e,
                                            5: f,
                                            6: g,
                                            7: h,
                                            8: i,
                                            9: j
                                            }

                                            k = len(set(sol.values()))

                                            if is_valid_solution(sol, G, s, k):
                                                happy = calculate_happiness(sol, G)
                                                if happy > max_happiness:
                                                    max_happiness = happy
                                                    best_d = sol
                                                    print(max_happiness)

    return best_d, len(set(best_d.values()))

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
