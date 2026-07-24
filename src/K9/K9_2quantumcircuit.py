import numpy as np
import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import UnitaryGate
from qiskit.providers.basic_provider import BasicSimulator

from src.K7.bases import bases
from src.K7.verifier import vertex_edges, game_result
from src.K7.quantumcircuit import game_circuit



#a, b are the two vertexes that alice and bob are given.
#(w,x) and (y,z) are the two edges which are removed.
def strategy(a,b,w,x,y,z):

  #define the dictionary so that the function works
  local_to_actual = {}

  #game_circuit returns a pair and we want a integer
  def e(e):
    return (local_to_actual[e[0]], local_to_actual[e[1]])
  #define the two edges
  edge1 = {w,x}
  edge2 = {y,z}

  #figure out the nonshared edge if possible
  if w == y:
    nonshared = {x,z}
  elif w == z:
    nonshared = {y,x}
  elif x == y:
    nonshared = {w,z}
  elif x == z:
    nonshared = {w,y}


  k7 = []

  #first case is if there is a shared vertex
  if w == y or w == z or x == y or x == z:

    #we already know fixed_edge based on above
    fixed_edge = tuple(sorted(nonshared))

    #generate k7 based on the 7 other vertices not in fixed_edge
    for i in range(1,10):
      if i not in fixed_edge:
        k7.append(i)

    #define the dictionaries to be able to map the 1-9 vertices in this game to the 1-7 in the original K7 
    actual_to_local = {k7[0]:1, k7[1]:2, k7[2]:3, k7[3]:4, k7[4]:5, k7[5]:6, k7[6]:7}
    local_to_actual = {1:k7[0], 2:k7[1], 3:k7[2], 4:k7[3], 5:k7[4], 6:k7[5], 7:k7[6]}


    #same logic as K9quantumcircuit.py
    if a in k7 and b in k7:
        local_a, local_b = game_circuit(actual_to_local[a],actual_to_local[b])
        return e(local_a), e(local_b)
      
    elif a in k7:
        local_a, local_b = game_circuit(actual_to_local[a],1)
        return e(local_a), fixed_edge
      
    elif b in k7:
        local_a, local_b = game_circuit(1,actual_to_local[b])
        return fixed_edge, e(local_b)
    else:
        return fixed_edge, fixed_edge


  #second case is where the two edges are disjoint.
  else:

    #again, defined fixed_edge, k7, and the dictionaries similarly.
    fixed_edge = (w,z)
    for i in range(1,10):
      if i not in fixed_edge:
        k7.append(i)
    actual_to_local = {k7[0]:1, k7[1]:2, k7[2]:3, k7[3]:4, k7[4]:5, k7[5]:6, k7[6]:7}
    local_to_actual = {1:k7[0], 2:k7[1], 3:k7[2], 4:k7[3], 5:k7[4], 6:k7[5], 7:k7[6]}
    
    if a in k7 and b in k7:
        local_a, local_b = game_circuit(actual_to_local[a],actual_to_local[b])
        return e(local_a), e(local_b)
          
    elif a in k7:
        local_a, local_b = game_circuit(actual_to_local[a],1)
        return e(local_a), fixed_edge
          
    elif b in k7:
        local_a, local_b = game_circuit(1,actual_to_local[b])
        return fixed_edge, e(local_b)
    else:
        return fixed_edge, fixed_edge




      
    
          


total = 0
for alice_vertex in range(1, 10):
    for bob_vertex in range(1, 10):   
      alice_edge, bob_edge = strategy(alice_vertex, bob_vertex, 2,3,4,1)
      total = total + game_result(alice_edge, bob_edge)

print(total)

