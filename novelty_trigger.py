import numpy as np

def check_novelty_trigger(probability=0.05):
    """
    Returns True with a small probability, simulating stochastic novelty events.

    Parameters:
        probability (float): Likelihood of triggering novelty event at a timestep.

    Returns:
        bool: True if novelty is triggered this timestep.
    """
    return np.random.rand() < probability
