import numpy as np  # type: ignore[import]
#define omega
w = np.exp(2*np.pi*1j/3)

#normalization
def norm(v):
  norm = np.linalg.norm(v)
  return v/norm

#21 edges
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

vectors = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21]




#bases
B1 = np.array([v1,v2,v3,v4,v5,v6])
B2 = np.array([v1,v7,v8,v9,v10,v11])
B3 = np.array([v2,v7,v12,v13,v14,v15])
B4 = np.array([v3,v8,v12,v16,v17,v18])
B5 = np.array([v4, v9, v13, v16, v19, v20])
B6 = np.array([v5, v10, v14, v17, v19, v21])
B7 = np.array([v6, v11, v15, v18, v20, v21])

bases = [B1, B2, B3, B4, B5, B6, B7];

#projectors
def p(v):
  return np.outer(v, np.conjugate(v))
P1 = p(v1)
P2 = p(v2)
P3 = p(v3)
P4 = p(v4)
P5 = p(v5)
P6=p(v6)
P7 = p(v7)
P8 = p(v8)
P9 = p(v9)
P10 = p(v10)
P11 = p(v11)
P12 = p(v12)
P13 = p(v13)
P14 = p(v14)
P15 = p(v15)
P16 = p(v16)
P17 = p(v17)
P18 = p(v18)
P19 = p(v19)
P20 = p(v20)
P21 = p(v21)

projectors = [P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21]

#checks
#all normalized

"""
for i in range(21):
  print(np.isclose(np.linalg.norm(vectors[i]), 1))
"""
#check orthonomal bases
"""
for k in range(7):

  basis = bases[k]
  for i in range(6):
    for j in range(6):
        if i == j:
          print(np.isclose(np.vdot(basis[i], basis[j]), 1))
        else:
          print(np.isclose(np.vdot(basis[i], basis[j]), 0))
"""

#projectors should satisfy P^2=P
"""
for i in range(21):
  print(np.isclose(projectors[i] @ projectors[i], projectors[i]))
"""

#projects should be hermitian
"""
for i in range(21):
  print(np.isclose(projectors[i].conj().T, projectors[i]))
"""

#projectors should be rank=1
"""
for i in range(21):
  print(np.linalg.matrix_rank(projectors[i]))
"""

#for each vertex the projectors connected to it should add to the identity
"""
print(np.isclose(P1+P2+P3+P4+P5+P6, np.identity(6)))
print(np.isclose(P1+P7+P8+P9+P10+P11, np.identity(6)))
print(np.isclose(P2+P7+P12+P13+P14+P15, np.identity(6)))
print(np.isclose(P3+P8+P12+P16+P17+P18, np.identity(6)))
print(np.isclose(P4+P9+P13+P16+P19+P20, np.identity(6)))
print(np.isclose(P5+P10+P14+P17+P19+P21, np.identity(6)))
print(np.isclose(P6+P11+P15+P18+P20+P21, np.identity(6)))
"""
