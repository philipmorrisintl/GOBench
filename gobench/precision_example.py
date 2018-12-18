import numpy as np
from scipy.optimize import dual_annealing

# Zerosum function (credits: SciPy testing function benchmark)
def func(x):
    if np.abs(np.sum(x)) < 3e-16:
        return 0.0
    return 1.0 + (10000.0 * np.abs(np.sum(x))) ** 0.5

dimension = 2
lower = np.array([-10.0] * dimension)
upper = np.array([10.0] * dimension)


# A custom 3-points gradient computation
def gradient(x):
    g = np.zeros(len(x), np.float64)
    reps = 1.e-6
    for i in range(len(x)):
        x1 = np.array(x)
        x2 = np.array(x)
        respl = reps
        respr = reps
        x1[i] = x[i] + reps
        if x1[i] > upper[i]:
            x1[i] = upper[i]
            repsr = x1[i] - x[i]
        x2[i] = x[i] - reps
        if x2[i] < lower[i]:
            x2[i] = lower[i]
            respl = x[i] - x2[i]
        f1 = func(x1)
        f2 = func(x2)
        g[i] = ((f1 - f2)) / (respl + respr)
    return g

res = dual_annealing(func, bounds=list(zip(lower, upper)),
        local_search_options={'method': 'BFGS', 'jac': gradient}
        )
print(res)
