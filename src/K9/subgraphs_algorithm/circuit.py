import numpy as np
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit.providers.basic_provider import BasicSimulator

from src.K9.subgraphs_algorithm.projector_search import projectors
from src.K9.subgraphs_algorithm.graphs import subgraph
from src.K9.subgraphs_algorithm.rank_search import find_rank_pattern, remove_equivlant_patterns
from src.K7.verifier import game_result

#create the 7 8x8 matrices
edges = []

for i in range(1,10):
  for j in range(i+1, 10):
    edges.append((i,j))
vertex_edges = {}
for i in range(1,10):
  vertex_edges[i] = []

  for edge in edges:
    if i in edge:
      vertex_edges[i].append(edge)


graph_edges = subgraph([(0,1)])

    
patterns = find_rank_pattern(graph_edges, dimension=8, max=10)

unique_patterns = remove_equivlant_patterns(patterns, graph_edges)


best_index = 0
best_loss = 100.0
best_result = []
for i in range(0, len(unique_patterns)):
  pattern = unique_patterns[i]

  result = projectors(dimension=8, pattern=pattern, graph_edges=graph_edges, attempts=1, max_iterations=50)
  print("Attempt", i+1, " loss is:", result["loss"])
  
  if result["loss"] < best_loss:
    best_loss = result["loss"]
    best_index = i
    best_result = result["bases"]

bases_eight = best_result



def alicestrategy(vertice):
  matrix = np.asarray(bases_eight[vertice-1])
  gate = UnitaryGate(matrix)
  return gate

def bobstrategy(vertice):
  matrix = np.asarray(bases_eight[vertice-1])
  gate = UnitaryGate(np.conjugate(matrix))
  return gate

#the actual circuit based on two inputs
def game_circuit(a, b):
  #create the entangled state: Alice 3 qubits, Bob 3 qubits.
  #We don't use |7> or |8>. we first initialize the first three qubits
  circuit = QuantumCircuit(6)
  circuit.initialize([1,1,1,1,1,1,0,0], [0,1,2], normalize = True)

  #bob's state should mirror alice's state
  circuit.cx(0,3)
  circuit.cx(1,4)
  circuit.cx(2,5)

  #000,000+001,001+010,010+011,011+100,100+101,101

  #find the gates we use
  agate = alicestrategy(a)
  bgate = bobstrategy(b)

  #apply the gates
  circuit.append(agate, [0,1,2])

  circuit.append(bgate, [3,4,5])

  circuit.measure_all()

#actually measure it
  backend = BasicSimulator()
  circuit = transpile(circuit, backend)
  result = backend.run(circuit, shots=1).result()
#get the measurements as a string
  string = list(result.get_counts())[0]
#separate the first three and last three elements in the string above
  bobstring = string[:3]
  alicestring = string[3:]
#convert the string from base 2 to base 10 
  aliceindex = int(alicestring[0])*4+int(alicestring[1])*2+int(alicestring[2])
  bobindex = int(bobstring[0])*4+int(bobstring[1])*2 + int(bobstring[2])
#find the related edge based on the index 
  aliceedge = vertex_edges[a][aliceindex]
  bobedge = vertex_edges[b][bobindex]
#return the edges that alice and bob input into the game verifier
  return aliceedge, bobedge



total = 0
for alice_vertex in range(1, 10):
    for bob_vertex in range(1, 10):   
      alice_edge, bob_edge = game_circuit(alice_vertex, bob_vertex)

      total = total + game_result(alice_edge, bob_edge) 

print(total) 
