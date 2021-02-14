import numpy as np
#----------------------------------------------------------------------------------------#

def CircleCenter3D(A, B, C):
    a = np.linalg.norm(C - B)
    b = np.linalg.norm(C - A)
    c = np.linalg.norm(B - A)
    s = (a + b + c) / 2
    radius = a*b*c / 4 / np.sqrt(s * (s - a) * (s - b) * (s - c))
    b1 = a**2 * (b**2 + c**2 - a**2)
    b2 = b**2 * (a**2 + c**2 - b**2)
    b3 = c**2 * (a**2 + b**2 - c**2)
    center = np.column_stack((A, B, C)).dot(np.hstack((b1, b2, b3)))
    center /= b1 + b2 + b3
    return [center, radius]

def GramSchmidt(vectors):
    basis = []
    for v in vectors:
        w = v - sum(np.dot(v,b)*b for b in basis)
        if (w > 1e-10).any(): basis.append(w/np.linalg.norm(w))
    return np.array(basis)

def GenerateCircle3D(A, B, C, sampling=100):
    try: a, b = GramSchmidt([A-C, A-B])
    except: pass
    try: a, b = GramSchmidt([C-B, C-A])
    except: pass
    try: a, b = GramSchmidt([B-C, B-A])
    except: pass
    center, radius = CircleCenter3D(A, B, C)
    xp, yp, zp = list(), list(), list()
    for i in np.linspace(0, 2*np.pi, sampling):
        xp.append(center[0] + radius*np.cos(i)*a[0] + radius*np.sin(i)*b[0])
        yp.append(center[1] + radius*np.cos(i)*a[1] + radius*np.sin(i)*b[1])
        zp.append(center[2] + radius*np.cos(i)*a[2] + radius*np.sin(i)*b[2])
    return center, np.array([xp, yp, zp])
