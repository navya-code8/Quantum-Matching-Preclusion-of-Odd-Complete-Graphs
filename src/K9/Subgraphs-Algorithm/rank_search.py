#we want to find many solutions (integers) for a lot of rank equations. we use the CP-SAT solver from google
from ortools.sat.python import cp_model
from graphs import vertices, edge, incident_edges

#finds a rank pattern based on the graph after deletion and the quantum dimension
def find_rank_pattern(graph_edges, dimension):

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

    #call the solver
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    if status not in [cp_model.FEASIBLE, cp_model.OPTIMAL]:
        return None

    rank_pattern = {}

    #we want the actual values of each edge
    for current_edge, i in rank_variables.items():
        rank_pattern[current_edge] = solver.value(i)

    return rank_pattern

if __name__ == "__main__":
    from graphs import subgraph

    graph_edges = subgraph([(0,1)])

    pattern = find_rank_pattern(graph_edges, dimension=6)

    if pattern is None:
        print("None")
    else:
        for current_edge, rank in pattern.items():
            if rank >0:
                print(current_edge, "rank", rank)




        

