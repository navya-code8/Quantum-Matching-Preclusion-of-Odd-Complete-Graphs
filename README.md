
# Quantum Matching Preclusion of Odd Complete Graphs

This repository implements and tests quantum strategies for the
perfect-matching nonlocal game on:

- the complete graph $K_7$; and
- $K_n-e$ for odd $n\geq 9$, where one edge has been deleted.

The project accompanies our work on **quantum matching preclusion**, which
studies how many edge failures a quantum perfect-matching strategy can
tolerate. The implementation is based on the projector construction in
[Quantum Perfect Matchings](https://doi.org/10.1007/s00023-025-01632-5).

## The perfect-matching nonlocal game

A verifier sends Alice a vertex $a$ and Bob a vertex $b$ from the same graph.
Each player must return an edge incident with the vertex they received. They
win when:

1. Alice's edge is incident with $a$ and Bob's edge is incident with $b$; and
2. their returned edges are either identical or vertex-disjoint.

A perfect classical strategy exists exactly when the graph has an ordinary
perfect matching. Since $K_7$ has an odd number of vertices, it has no
classical perfect matching. Nevertheless, shared entanglement allows Alice and
Bob to win the game perfectly.

## Implemented strategies

### The $K_7$ quantum strategy

The 21 edges of $K_7$ are represented by 21 vectors in $\mathbb C^6$. For
each vertex, the six vectors corresponding to its incident edges form an
orthonormal basis. If $v_e$ is the normalized vector assigned to edge $e$,
then its rank-one projector is

$$
P_e=\lvert v_e\rangle\langle v_e\rvert.
$$

At every vertex $x$, the incident projectors satisfy

$$
\sum_{e\ni x}P_e=I_6.
$$

Projectors corresponding to distinct intersecting edges are orthogonal. These
relations are exactly the conditions needed for a perfect quantum strategy.

#### Six-qubit circuit

Alice and Bob each use three qubits, for a total of six qubits. The circuit
prepares the maximally entangled state

$$
\lvert\Phi_6\rangle
=\frac{1}{\sqrt6}\sum_{j=0}^{5}
\lvert j\rangle_A\lvert j\rangle_B.
$$

In the computational basis, this is

$$
\frac{1}{\sqrt6}\big(
\lvert000000\rangle+\lvert001001\rangle+
\lvert010010\rangle+\lvert011011\rangle+
\lvert100100\rangle+\lvert101101\rangle
\big).
$$

The mathematical measurement bases are $6\times6$ matrices. Because three
qubits span an eight-dimensional space, each matrix is embedded into an
$8\times8$ unitary by adding an identity block on the two unused dimensions:

$$
\widetilde U_x=U_x\oplus I_2.
$$

After receiving their vertices, Alice and Bob apply the appropriate
vertex-dependent basis gates. Bob uses the conjugate basis required by the
maximally entangled strategy. They then measure their three-qubit registers.
Outcomes $0,\ldots,5$ are mapped to the six edges incident with the
corresponding input vertex.

The unused outcomes $6$ and $7$ have zero probability in the ideal
construction.

### The $K_n-e$ strategy

For every odd $n\geq9$, the repository implements a perfect quantum strategy
for $K_n-e$, where $e=xy$ is the deleted edge.

The strategy divides the graph into two components:

1. a seven-vertex quantum core using the $K_7$ strategy; and
2. deterministic matched pairs on the remaining $n-7$ vertices.

The algorithm selects seven vertices containing exactly one endpoint of the
deleted edge. Therefore, the missing edge does not occur inside the $K_7$
core. Since $n-7$ is even, all remaining vertices can be paired.

If a player receives a vertex in the quantum core, the program runs the
corresponding $K_7$ measurement. If the received vertex is outside the core,
the player returns its predetermined pairing edge. An edge returned from the
quantum core is disjoint from every deterministic pairing edge, so the
combined strategy wins perfectly.

The quantum component always uses the same six-qubit circuit, independently of
$n$. Increasing $n$ requires only classical vertex selection, relabeling, and
pairing.

## Repository structure

```text
.
├── src/
│   ├── K7/
│   │   ├── __init__.py
│   │   ├── bases.py
│   │   ├── quantumcircuit.py
│   │   └── verifier.py
│   └── Kn/
│       └── Knquantumcircuit.py
├── tests/
│   ├── test_K7.py
│   └── test_Kn_minus_e.py
├── requirements.txt
└── README.md
```

The main files are:

- **`src/K7/bases.py`**: the seven measurement bases for the $K_7$
  construction;
- **`src/K7/quantumcircuit.py`**: preparation, measurement, simulation, and
  decoding for the six-qubit circuit;
- **`src/K7/verifier.py`**: graph edges, incident-edge lists, and the game
  verifier;
- **`src/Kn/Knquantumcircuit.py`**: the general $K_n-e$ core-and-pairs
  strategy;
- **`tests/test_K7.py`**: tests of all ordered $K_7$ verifier inputs; and
- **`tests/test_Kn_minus_e.py`**: tests of the $K_n-e$ construction.

## Installation

Python 3.10 or later is recommended.

Clone the repository:

```bash
git clone https://github.com/navya-code8/Quantum-Matching-Preclusion-of-Odd-Complete-Graphs.git
cd Quantum-Matching-Preclusion-of-Odd-Complete-Graphs
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The main dependencies are Qiskit, NumPy, and Pytest.

## Usage

### Run the $K_7$ strategy

```python
from src.K7.quantumcircuit import game_circuit
from src.K7.verifier import game_result

alice_vertex = 1
bob_vertex = 4

alice_edge, bob_edge = game_circuit(alice_vertex, bob_vertex)

print("Alice:", alice_edge)
print("Bob:", bob_edge)
print("Win:", bool(game_result(alice_edge, bob_edge)))
```

The circuit returns one sampled edge for Alice and one sampled edge for Bob.

### Run the $K_n-e$ strategy

```python
from src.Kn.Knquantumcircuit import strategy
from src.K7.verifier import game_result

n = 11
deleted_edge = (1, 2)
alice_vertex = 3
bob_vertex = 8

alice_edge, bob_edge = strategy(
    alice_vertex,
    bob_vertex,
    deleted_edge[0],
    deleted_edge[1],
    n,
)

print("Alice:", alice_edge)
print("Bob:", bob_edge)
print("Win:", bool(game_result(alice_edge, bob_edge)))
```

The arguments of `strategy(a, b, x, y, n)` are:

- `a`: Alice's input vertex;
- `b`: Bob's input vertex;
- `x, y`: the endpoints of the deleted edge; and
- `n`: an odd integer at least 9.

## Running the tests

Run all tests from the repository root:

```bash
python -m pytest -q
```

The tests iterate over every ordered pair of verifier questions for:

- the $K_7$ circuit; and
- representative $K_n-e$ instances with $n=9,11,13$.

The current circuit uses one simulator shot for each input pair. These tests
therefore confirm that the sampled outputs satisfy the verifier, but they do
not compute the complete output distribution. The exact correctness of the
strategy follows from the vector and projector identities.

## Current limitations

- The circuits run on Qiskit's ideal `BasicSimulator` rather than quantum
  hardware.
- Each test uses one sampled outcome per verifier input.
- The current $K_n-e$ test uses a representative deleted edge instead of
  iterating over all possible deleted edges.
- The implementation covers the $K_7$ and single-edge $K_n-e$ constructions,
  not every failure pattern studied in the accompanying paper.
- Circuit-depth and gate-count estimates are not yet included.

## Possible improvements

- Verify complete statevector output distributions instead of one-shot
  samples.
- Test every deleted edge in $K_n-e$.
- Add fixed simulator seeds for fully reproducible test runs.
- Record transpiled circuit depth and two-qubit gate counts.
- Add noisy-simulator or quantum-hardware experiments.

## References

1. D. Cui, L. Mančinska, S. S. Nezhadi, and D. E. Roberson,
   “Quantum Perfect Matchings,” *Annales Henri Poincaré*, 2025.
   [doi:10.1007/s00023-025-01632-5](https://doi.org/10.1007/s00023-025-01632-5)
2. J. Furches, S. Chehade, K. Hamilton, N. Wiebe, and C. Ortiz Marrero,
   “Application-Level Benchmarking of Quantum Computers Using Nonlocal Game Strategies,” 2023.
   [arXiv:2311.01363](https://doi.org/10.48550/arXiv.2311.01363)
4. P. Lisoněk, P. Badziąg, J. R. Portillo, and A. Cabello,
   “Kochen-Specker Set with Seven Contexts,” *Physical Review A*, vol. 89,
   no. 4, 042101, 2014.
   [doi:10.1103/PhysRevA.89.042101](https://doi.org/10.1103/PhysRevA.89.042101)

## Paper

The accompanying manuscript is titled **â€œQuantum Matching Preclusion of Odd
Complete Graphs.â€** Citation information and a public paper link will be added
when available.
