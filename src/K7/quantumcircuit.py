import numpy as np
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit.providers.basic_provider import BasicSimulator

from bases import bases
from verifier import vertex_edges, game_result


#create the 7 8x8 matrices
def matrix(m):
  eight_m = np.identity(8, dtype=complex)
  eight_m[:6, :6] = m
  return eight_m

bases_eight = [matrix(m) for m in bases]


def alicestrategy(vertice):
  matrix = bases_eight[vertice-1]
  gate = UnitaryGate(matrix)
  return gate

def bobstrategy(vertice):
  matrix = bases_eight[vertice-1]
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


#testing the algorithm

for alice_vertex in range(1, 8):
  for bob_vertex in range(1, 8):   
    print("Alice's vertex:", alice_vertex)
    print("Bob's vertex:", bob_vertex)
    alice_edge, bob_edge = game_circuit(alice_vertex, bob_vertex)
    print("Alice's edge:", alice_edge)
    print("Bob's edge:", bob_edge)
    print("Game result:", game_result(alice_edge, bob_edge))