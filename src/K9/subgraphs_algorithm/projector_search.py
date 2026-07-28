import numpy as np
from src.K9.subgraphs_algorithm.graphs import incident_edges, subgraph
from src.K9.subgraphs_algorithm.rank_search import find_rank_pattern, remove_equivlant_patterns
#this is for the optimization
from scipy.optimize import minimize
#from a 



#input is:
#for every edge we have a rank.
#decide what columns correspond to what ranks COMPLETED
#we create rotation matrix based on arbitrary values COMPLETED
#build a basis by starting with the identity and then multiplying all rotations COMPLETED
#for each column in a basis, builds a projector (for all edges) COMPLETED
#calculate error
#optimize 
#record best case

#creates a rotation matrix based on the dimension, angle, and indice that needs to be rotated
def rotation_matrix(dimension, i, j, angle):
    #we have the identity
    #if the rotation matrix is R, we only change:
    #R_{ii}, R_{jj}, R_{ij}, R_{ji}

    #identity
    matrix = np.identity(dimension)

    #rotation matrix
    cos = np.cos(angle)
    sin = np.sin(angle)

    #modify the matrix
    matrix[i, i] = cos
    matrix[j, j] = cos
    matrix[i, j] = -sin
    matrix[j,i] = sin

    return matrix

#angles is a 28 item list, and dimension
def basis(dimension, angles):

    #this is the start for every single basis
    basis = np.identity(dimension)

    #angles[0] to angles[27] should be multiplied by basis

    index = 0
    for i in range(dimension):

        for j in range(i+1, dimension):

            #for i =0:
            #(0,1) (0,2) (0,3) ... (0,7) for dimension = 8
            #we take the index of the angle 
            angle = angles[index]

            #uses the rotation_matrix function to convert the rotation about the angle to an dimensionxdimension matrix
            matrix = rotation_matrix(dimension, i, j, angle)

            #we multiply basis times all of the matrices 
            basis = basis @ matrix

            #
            index +=1

    return basis


#build 9 bases for 9 vertices 
#224 item list
#dimension
def build_basis(dimension, allangles):
    #basis 0 is allangles[0] to allangles[27] for dimesion = 8 dimension * dimesion-1)/2


    angles_per_basis = dimension * (dimension-1) //2
    total_angles = 8 * angles_per_basis
    #stores the set of 9 bases
    bases = {}

    #fix the first one to be identity
    bases[0] = np.identity(dimension)

    for i in range(1,9):

        #we want 28 angles per basis
        startindex = angles_per_basis*(i-1)

        endindex = startindex + angles_per_basis

        #for example, basis 1 should be allangles[0] to allangles[27]
        indexes = allangles[startindex:endindex]

        #build the basis
        bases[i] = basis(dimension, indexes)

    return bases

#we don't need dimension for this as the ranks already add up to the dimension
#decides what columns go to what edges for every basis vector for every vertex
def decidecolumns(pattern, graph_edges):

    #define the dictionary which gives us the columns that we want
    routing = {}

    #define the index of the column. goes from 0 to dimension
    for i in range(0,9):
        routing[i] = {}
        index = 0 


        for edge in incident_edges(i, graph_edges):

            #find out what rank is assigned to each edge that is connected to the current vertex
            rank = pattern[edge]


            #find out what columns should be assigned to that specific edge 
            columns = range(index, index+rank)

            #if ranks were (0,2) rank 2, (0,4) rank 1, (0,7) rank 3:
            #routing[0] = (0,2) : [0,1]
            #routing[1] = (0,4) : [2]
            #routing[2] = (0,7) : [3,4,5]
            routing[i][edge] = columns

            #move the index up
            index += rank
    return routing


#create projectors based on basis and columns
def buildprojectors(basis, columns):

    #these are the indices of the columns that we multiply for each basis
    columns = basis[:, columns]


    #creates the projector 
    projector = columns @ columns.conj().T

    #returns the projector 
    return projector


#we want to make all the projectors
def makeprojectors(bases, routing, graph_edges):

    #dictionary of all projectors
    projectors = {}

    #same logic as thedecide columns we enumerate through each vertex and all edges connected to that vertex
    for i in range(0,9):

        projectors[i] = {}


        for edge in incident_edges(i, graph_edges):

            #the indices of columns that we want
            columns = routing[i][edge]

            #builds the projector
            projector = buildprojectors(bases[i], columns)

            #puts it into the dictionary
            projectors[i][edge] = projector

    return projectors


#calculate error
def calculate_error(allangles, routing, graph_edges, dimension):

    bases = build_basis(dimension, allangles)

    projectors = makeprojectors(bases, routing, graph_edges)

    error = 0.0

    for edge in graph_edges:

        u, v = edge

        uprojector = projectors[u][edge]

        vprojector = projectors[v][edge]

        difference = uprojector - vprojector

        edgeloss = np.sum(np.abs(difference)**2)

        error +=edgeloss

    return (error/len(graph_edges))

#optimizer 
def projectors(dimension, pattern, graph_edges, attempts=5, max_iterations=500):
    routing = decidecolumns(pattern, graph_edges)

    best_result = None

    for attempt in range(attempts):

        #randomize the angles
        starting_angles = np.random.uniform(-np.pi, np.pi, 8*dimension*(dimension-1)//2)


        #use scipy for this
        result = minimize(
            calculate_error,
            starting_angles,
            args = (
                routing, 
                graph_edges,
                dimension
            ), 
            method = "L-BFGS-B",
            options = {
                "maxiter": max_iterations
            }
        )

        #bookkeeping
        print(
            f"Attempt {attempt+1}/{attempts}: "
            f"loss = {result.fun}"
        )


        #we want the best result
        if best_result is None or result.fun < best_result.fun:
            best_result = result

    best_angles = best_result.x

    best_bases = build_basis(dimension, best_angles)

    best_projectors = makeprojectors(best_bases, routing, graph_edges)


    #return all bases/projectors/angles associated with the best result
    return {
        "loss": float(best_result.fun),
        "angles": best_angles,
        "bases": best_bases,
        "projectors": best_projectors,
        "routing": routing

    }

#graph_edges 

if __name__ == "__main__":

    graph_edges = subgraph([(0,1), (0,2), (0,3), (1,3), (2,3), (3,4)])

    
    patterns = find_rank_pattern(graph_edges, dimension=6, max=100)

    unique_patterns = remove_equivlant_patterns(patterns, graph_edges)

    pattern = unique_patterns[0]

    result = projectors(dimension=6, pattern=pattern, graph_edges=graph_edges, attempts=1, max_iterations=50)

    print("Loss is:", result["bases"])

    