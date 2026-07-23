import numpy as np
import qiskit
from qiskit import QuantumCircuit
from qiskit import UnitaryGate
#not needed in vs code but needed here
from src.bases import bases
from src.verifier import vertex_edges


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
  gate = UnitaryGate(matrix)
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
  import numpy as np
import qiskit
from qiskit import QuantumCircuit
from qiskit import UnitaryGate
from qiskit import BasicSimulator

#not needed in vs code but needed here
v1 = norm(np.array([1,0,0,0,0,0]))
v2 = norm(np.array([0,1,0,0,0,0]))
v3 = norm(np.array([0,0,1,0,0,0]))
v4 = norm(np.array([0,0,0,1,0,0]))
v5 = norm(np.array([0,0,0,0,1,0]))
v6 = norm(np.array([0,0,0,0,0,1]))
v7 = norm(np.array([0,0,1,1,1,1]))
v8 = norm(np.array([0,1,0,1,w,w**2],dtype=complex))
v9 = norm(np.array([0,1,1,0,w**2,w],dtype=complex))
v10 = norm(np.array([0,1,w,w**2,0,1],dtype=complex))
v11 = norm(np.array([0, 1, w**2, w, 1, 0],dtype=complex))
v12 = norm(np.array([1, 0, 0, 1, w**2, w],dtype=complex))
v13 = norm(np.array([1, 0, 1, 0, w, w**2],dtype=complex))
v14 = norm(np.array([1, 0, w**2, w, 0, 1],dtype=complex))
v15 = norm(np.array([1, 0, w, w**2, 1, 0],dtype=complex))
v16 = norm(np.array([1, 1, 0, 0, 1, 1]))
v17 = norm(np.array([w, w**2, 0, 1, 0, 1],dtype=complex))
v18 = norm(np.array([w**2, w, 0, 1, 1, 0],dtype=complex))
v19 = norm(np.array([w**2, w, 1, 0, 0, 1],dtype=complex))
v20 = norm(np.array([w, w**2, 1, 0, 1, 0],dtype=complex))
v21 = norm(np.array([1, 1, 1, 1, 0, 0]))

#bases
B1 = np.array([v1,v2,v3,v4,v5,v6])
B2 = np.array([v1,v7,v8,v9,v10,v11])
B3 = np.array([v2,v7,v12,v13,v14,v15])
B4 = np.array([v3,v8,v12,v16,v17,v18])
B5 = np.array([v4, v9, v13, v16, v19, v20])
B6 = np.array([v5, v10, v14, v17, v19, v21])
B7 = np.array([v6, v11, v15, v18, v20, v21])

bases = [B1, B2, B3, B4, B5, B6, B7]

#all 21 edges
edges = []

for i in range(1,8):
  for j in range(i+1, 8):
    edges.append((i,j))

#given a vertex i, gives all edges connected to that vertex i
vertex_edges = []
for i in range(1,8):
  vertex_edges[i] = []

  for edge in edges:
    if i in edge:
      vertex_edges[i].append[edge]

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
  gate = UnitaryGate(matrix)
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
  result = backend.run(circuit, shots=1).result()
#get the measurements as a string
  string = list(result.getcounts())[0]
#separate the first three and last three elements in the string above
  alicestring = string[:3]
  bobstring = string[3:]
#convert the string from base 2 to base 10 
  aliceindex = alicestring[0]*4+alicestring[1]*2+alicestring[2]
  bobindex = bobstring[3]*4+bobstring[4]*2 + bobstring[5]
#find the related edge based on the index 
  aliceedge = vertex_edges[a][aliceindex]
  bobedge = vertex_edges[b][bobindex]
#return the edges that alice and bob input into the game verifier
  return aliceedge, bobedge






