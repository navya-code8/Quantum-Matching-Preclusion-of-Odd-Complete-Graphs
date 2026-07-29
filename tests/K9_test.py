from src.K9.K9quantumcircuit import strategy 
from src.K7.verifier import game_result

def test_quantum_strategy():
  for alice_vertex in range(1, 10):
    for bob_vertex in range(1, 10):   
      alice_edge, bob_edge = strategy(alice_vertex, bob_vertex)

      assert game_result(alice_edge, bob_edge) is 1