# reactivation_trigger.py

import random

def should_reactivate(timestep, rate=0.1):
    """
    Determines whether a stochastic novelty jolt should occur at this timestep.

    Parameters:
    - timestep: Current timestep in the simulation
    - rate: Probability of reactivation per timestep

    Returns:
    - Boolean indicating whether to trigger reactivation
    """
    return random.random() < rate
