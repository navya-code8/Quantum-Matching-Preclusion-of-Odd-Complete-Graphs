import numpy as np
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit.providers.basic_provider import BasicSimulator
import random

from src.K7.bases import bases
from src.K7.verifier import vertex_edges, game_result
from src.K7.quantumcircuit import game_circuit


#random edge chosen
removed_edge = random.sample(range(1,10), 2)

partner = random.choice([i for i in range(1,10) if i != removed_edge[0] and i != removed_edge[1]])

#predetermined strategy
fixed = [removed_edge[0], partner]
fixed_edge = (removed_edge[0], partner)

#this is the K7 graph
k7 = [i for i in range(1,10) if i != removed_edge[0] and i != partner]

#maps the vertices from the K9 graph to the K7 graph
actual_to_local = {}
local_to_actual = {}

for i in range(7):
    actual_to_local[k7[i]] = i + 1
    local_to_actual[i + 1] = k7[i]



#game_circuit returns a pair and we want a integer
def e(e):
  return (local_to_actual[e[0]], local_to_actual[e[1]])

#strategy for K9-e breaking it down into K7 plus a paired edge
def strategy(a,b):

  #if both a,b are in the K7 subgraph we can just run the circuit normally
  if a in k7 and b in k7:
    local_a, local_b = game_circuit(actual_to_local[a],actual_to_local[b])
    return e(local_a), e(local_b)
  
  #if only a is in the subgraph, b automatically returns (2,9) so we don't care about local_b
  elif a in k7:
    local_a, local_b = game_circuit(actual_to_local[a],1)
    return e(local_a), fixed_edge
  
  #if only b is in the subgraph, a automatically returns (2,9) so we don't care about local_a
  elif b in k7:
    local_a, local_b = game_circuit(1,actual_to_local[b])
    return fixed_edge, e(local_b)
  #otherwise both a,b are (2,9) so we return (2,9)
  else:
    return fixed_edge, fixed_edge


total = 0
for alice_vertex in range(1, 10):
    for bob_vertex in range(1, 10):   
      alice_edge, bob_edge = strategy(alice_vertex, bob_vertex)
      total = total + game_result(alice_edge, bob_edge)

print(total)

