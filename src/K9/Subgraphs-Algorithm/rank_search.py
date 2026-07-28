#we want to find many solutions (integers) for a lot of rank equations. we use the CP-SAT solver from google
from ortools.sat.python import cp_model
from graphs import vertices, edge, incident_edges, K9_edges
#import permutations to eliminate the equivalant rank patterns
from itertools import permutations, combinations

#finds a rank pattern based on the graph after deletion and the quantum dimension
def find_rank_pattern(graph_edges, dimension, max):

    #declare the CP-SAT model
    model = cp_model.CpModel()

    #dictionary for the value of the rank for each edge
    rank_variables = {}

    for current_edge in graph_edges:

        #make sure the edge is in the correct order
        u,v = current_edge

        #creates the variables for the problem
        rank_variables[current_edge] = model.new_int_var(0, dimension, f"r_{u}_{v}")

    for vertex in vertices:
        edges = incident_edges(vertex, graph_edges)

        #we want the ranks at those edges
        ranks = []
        for i in edges:
            ranks.append(rank_variables[i])

        #create the constraints
        model.add(sum(ranks) == dimension)
    for a, b, c in combinations(vertices, 3):

        edge_ab = edge(a, b)
        edge_ac = edge(a, c)
        edge_bc = edge(b, c)

        # Only add the constraint if all three triangle edges
        # are present in the current subgraph.
        if (
            edge_ab in rank_variables
            and edge_ac in rank_variables
            and edge_bc in rank_variables
        ):
            model.add(
                rank_variables[edge_ab]
                + rank_variables[edge_ac]
                + rank_variables[edge_bc]
                <= dimension
            )
    #edges, variables, in matching order
    edges = list(rank_variables.keys())
    variables = list(rank_variables.values())

    patterns = []


    #we want to run this as much as posisble
    while len(patterns) < max:

        #solver
        solver = cp_model.CpSolver()
        status = solver.solve(model)

        #we need a solution
        if status not in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
            break

        #we want the ranks chosen by the solver
        values = []

        for i in variables:
            values.append(solver.value(i))

        #match each edge with its rank in a dictionary
        pattern = {}

        for i in range(len(edges)):
            pattern[edges[i]] = values[i]

        patterns.append(pattern)

        model.add_forbidden_assignments(variables, [values])

    return patterns

#now, we have rank patterns. however, a lot of them are the same with different permutes. 

#we first fine symmetries in graphs (based on removed edges)
def find_symmetries(graph_edges):
    graph_edges = set(graph_edges)

    #calculate the deleted edges
    deleted_edges = []
    for i in K9_edges:
        if i not in graph_edges:
            deleted_edges.append(i)

    deleted_edges = set(deleted_edges)
 
    symmetries = []

    #9! total permutations
    for i in permutations(vertices):
        #stores where deleted edges get mapped to under permutations
        moved_deleted = set()

        for u,v in deleted_edges:
            moved = edge(i[u], i[v])

            moved_deleted.add(moved)

        #if this is yes, then this is a valid permutation
        if moved_deleted == deleted_edges:
            symmetries.append(i)
    return symmetries

#renames the pattern using every graph symmetry
def recognition(pattern, graph_edges, symmetries):
    ordered_edges = sorted(graph_edges)
    smallest_signature = None

    for i in symmetries:

        moved_pattern = {}

        #go through each surviving edge
        for current_edge in graph_edges:
            u,v = current_edge

            #edge under permutation
            moved_edge = edge(i[u], i[v])

            #move the rank with the edge
            moved_pattern[moved_edge] = pattern[current_edge]

        recognitions = []

        for current_edge in ordered_edges:
            recognitions.append(moved_pattern[current_edge])

        recognition1 = tuple(recognitions)


        #we want the smallest possible one


        if smallest_signature is None:
            smallest_signature = recognition1

        elif recognition1 < smallest_signature:
            smallest_signature = recognition1
    return smallest_signature
        

def remove_equivlant_patterns(patterns,graph_edges):
    #we want to keep only one pattern from each equivalance class.


    #find graph symmetriees
    symmetries = find_symmetries(graph_edges)

    #this is what we want
    unique = []

    #this stores the equivalance classes that we have already seen
    seen = set()

    #enumerate through all the patterns 
    for pattern in patterns:
        signature = recognition(pattern, graph_edges, symmetries)

        #if this hasn't appeared before then this pattern is new
        if signature not in seen:
            seen.add(signature)
            unique.append(pattern)
    print("Graph symmetries: ", len(symmetries))
    print("rank patterns before equivalance:", len(patterns))
    print("distinct rank patterns:", len(unique))

    return unique







if __name__ == "__main__":
    from graphs import subgraph

    graph_edges = subgraph([(0,1)])

    
    patterns = find_rank_pattern(graph_edges, dimension=6, max=100)

    unique_patterns = remove_equivlant_patterns(patterns, graph_edges)

    for pattern_number in range(len(unique_patterns)):
        print("\nPattern", pattern_number+1)

        pattern = unique_patterns[pattern_number]

        for current_edge, rank in pattern.items():
            if rank >0:
                print(current_edge, "rank", rank)

        




        

