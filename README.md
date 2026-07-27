Our project implements and tests quantum strategies for the perfect-matching nonlocal game centered in the paper [*<u>Quantum Perfect Matchings</u>*](https://arxiv.org/pdf/2502.05136).

The main focus is the complete graph $`K_{7}`$ as it has an odd number of vertices, so it has no classical perfect matching. However, the paper proves that it has a perfect quantum strategy. This repository implements the corresponding vector, projector, and quantum circuit construction and examines extensions to larger odd complete graphs

## Overview

In this perfect-matching nonlocal game, a verifier sends one graph vertex (question) to Alice and another to Bob. Each player responds and returns an edge (answer). Their answers are valid when:

1.  The edge that the player returns is incident corresponding to the vertex they received.

2.  The edges that the players return are either identical or disjoint.

A perfect classical strategy exists exactly when the graph has a classical perfect matching possible. The $`K_{7}`$ construction instead uses shared entanglement and quantum measurements to win the game perfectly for odd-number graphs without producing an ordinary classical matching.

## Requirements

- Python 3.10 or later

- Qiskit 2.20

- NumPy 2.3.1

- Matplotlib 3.10.3

- Pytest 8.4.1

Install the required packages with this command:

|                                           |
|:------------------------------------------|
| python -m pip install -r requirements.txt |

Recommendation is to use a virtual environment:

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">python -m venv .venv<br />
source .venv/bin/activate<br />
python -pip install -r requirements.txt</td>
</tr>
</tbody>
</table>

Virtual environment implementation for Windows:

|                        |
|:-----------------------|
| .venv\Scripts\activate |

## Usage

### Run the K_7 Strategy

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">from src.K7.quantumcircuit import game_circuit<br />
from src.K7.verifier import game_result<br />
<br />
alice_vertex = 1<br />
Bob_vertex = 4<br />
<br />
Alice_edge, bob_edge = game_circuit(alice_vertex, bob_vertex)<br />
<br />
print("Alice:", alice_edge)<br />
print("Bob:" bob_edge)<br />
print("winning result:", game_result(alice_edge, bob_edge))</td>
</tr>
</tbody>
</table>

The circuit returns one sampled edge for Alice and one sampled edge for Bob.

### Run the tests

Run this in the repository root:

|           |
|:----------|
| pytest -q |

### Extension experiments execution

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<tbody>
<tr>
<td style="text-align: left;">python K9quantumcircuit.py<br />
python K9_2quantumcircuit.py<br />
python K_nquantumcircuit.py</td>
</tr>
</tbody>
</table>

Each script grades its strategy over the selected Alice and Bob question pairs and prints the total number of accepted outcomes.

## Mathematical Construction

### $`K_{7}`$ Vectors and Bases

The 21 edges of $`K_{7}\`$are displayed by 21 normalized vectors in $`\backslash mathbb\{ C\}\hat{}6`$. For each graph vertex, the six vectors are associated with their incident edges that form an orthonormal basis.

If $`B_{x}`$ is the basis for vertex $`x`$, then

$`B_{x}{B^{\dagger}}_{x}\  = \ I_{6}`$

Definition for a rank-one projector is given by its corresponding normalized vector $`v_{e}`$

$`P_{e}\  = \ |v_{e} > < v_{e}|`$

The projectors for the six edges incident to each vertex satisfy:

sum($`P_{e}`$ for the e incident to x) = $`I_{6}`$

Projections with distinct overlapping edges are orthogonal.

## Qubit Embedding

The mathematical construction uses a six-dimensional Hilbert space. Since a qubit register must have dimension $`2^{n}`$, the implementation turns the six-dimensional vectors into an eight-dimension three-qubit space

$`(a0,\ a1,\ a2,\ a3,\ a4,\ a5) - > (a0,\ a1,\ a2,\ a3,\ a4,\ a5,0,0)`$

Alice and Bob each use three qubits which gives a six-qubit circuit in total.

## Larger Odd complete graphs

For odd $`n \geq 9`$, the strategy splits the graph into:

- A seven-vertex subgraph using the $`K_{7}`$ quantum strategy

- An even number of remaining vertices paired with fixed classical edges

This trails the construction used to extend the $`K_{7}`$ result in larger odd complete graphs.

## Current Limitations

## Testing Improvements

## Reference(s)

> Cui, D., Mančinska, L., Nezhadi, S. S., & Roberson, D. E. (2025). Quantum Perfect Matchings. *Annales Henri Poincaré*. https://doi.org/10.1007/s00023-025-01632-5
