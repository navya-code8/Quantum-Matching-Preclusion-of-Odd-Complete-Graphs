from src.K7.quantumcircuit import game_circuit
from src.K7.verifier import game_result


def test_quantum_strategy():
  for alice_vertex in range(1, 8):
    for bob_vertex in range(1, 8):   
      alice_edge, bob_edge = game_circuit(alice_vertex, bob_vertex)

      assert game_result(alice_edge, bob_edge) is 1

    