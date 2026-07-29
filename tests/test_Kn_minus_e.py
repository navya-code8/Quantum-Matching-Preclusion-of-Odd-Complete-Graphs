from src.Kn.Knquantumcircuit import strategy
from src.K7.verifier import game_result

def test_Kn_minus_e():
    for i in range(4,7):
        for alice_vertex in range(1, 2*i+2):
            for bob_vertex in range(1, 2*i+2):   
                    alice_edge, bob_edge = strategy(alice_vertex, bob_vertex, 1, 2, 2*i+1)
        
                    assert game_result(alice_edge, bob_edge) is 1

