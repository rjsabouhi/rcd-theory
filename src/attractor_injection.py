# attractor_injection.py

import numpy as np

def inject_attractor(H, M, R, injection_timestep, current_timestep):
    """
    Inject controlled symbolic modulation at a defined timestep.

    Parameters:
    - H, M, R: Current manifold states and reflection value
    - injection_timestep: When to apply injection
    - current_timestep: Simulation's current timestep

    Returns:
    - Modified H, M, R
    """
    if current_timestep == injection_timestep:
        delta_H = np.random.normal(loc=0.1, scale=0.05, size=H.shape)
        delta_M = np.random.normal(loc=-0.1, scale=0.05, size=M.shape)
        H += delta_H
        M += delta_M
        R += 0.2  # symbolic boost to reflection
    return H, M, R
