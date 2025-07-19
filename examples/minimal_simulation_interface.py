
print("✅ rcd_model.py loaded")
print("✅ Running RCD simulation...")

from src.rcd_model import RCDModel
from novelty_trigger import check_novelty_trigger
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Instantiate and configure model
model = RCDModel()
model.set_parameters(alpha=0.7, beta=0.2, delta=0.1, n_dimensions=3, noise_level=0.1)

# Inject attractors mid-simulation
model.inject_H = np.random.randn(10) * 0.1  # symbolic perturbation
model.inject_M = np.random.randn(10) * 0.1
model.inject_R = 0.2  # boost reflection

# Run simulation
results = model.simulate(n_timesteps=100)

# Print results
for t in range(len(results['reflection'])):
    # Check for stochastic novelty trigger
    if check_novelty_trigger():
        print(f"Novelty trigger activated at t={t}!")
        model.state['gamma'] = min(1.0, model.state['gamma'] + 0.2)
        model.state['rho'] = min(1.0, model.state['rho'] + 0.1)

    g = results['phase_sync'][t]
    r = results['semantic_corr'][t]
    R_val = results['reflection'][t]
    Lambda = results['procrustes_dist'][t]
    print(f"t={t:03d} | γ(t): {g:.3f} | ρ(t): {r:.3f} | R(t): {R_val:.3f} | Λ(t): {Lambda:.3f}")
