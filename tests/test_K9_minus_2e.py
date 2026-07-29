from src.K7.verifier import game_result
from src.K9.K9_2quantumcircuit import strategy

def test_K9_minus_2e_disjoint():
    for alice_vertex in range(1, 10):
        for bob_vertex in range(1, 10):   
              alice_edge, bob_edge = strategy(alice_vertex, bob_vertex, 2,3,4,1)
              assert game_result(alice_edge, bob_edge) is 1


def test_K9_minus_2e_notdisjoint():
    for alice_vertex in range(1, 10):
        for bob_vertex in range(1, 10):   
              alice_edge, bob_edge = strategy(alice_vertex, bob_vertex, 2,3,2,4)
              assert game_result(alice_edge, bob_edge) is 1
