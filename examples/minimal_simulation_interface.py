# minimal_simulation_interface.py

from src.rcd_model import RCDModel
from src.lake_state import compute_lake_state
import numpy as np

def main():
    print("✅ Running RCD simulation...")
    model = RCDModel()
    results = model.simulate(n_timesteps=100)

    # Post-process Lake-State values
    lake_state_values = []
    for t in range(len(results['reflection'])):
        gamma = results['phase_sync'][t]
        rho = results['semantic_corr'][t]
        R = results['reflection'][t]

        Lambda_t = compute_lake_state(gamma, rho, R)
        lake_state_values.append(Lambda_t)

        print(f"t={t:03d} | γ(t): {gamma:.3f} | ρ(t): {rho:.3f} | R(t): {R:.3f} | Λ(t): {Lambda_t:.3f}")

    # Optionally detect persistent Lake-State
    threshold = 1.5
    sustained = sum(1 for val in lake_state_values if val >= threshold)
    if sustained > 10:
        print("\n🧠 Lake-State emergence detected (Λ(t) ≥ 1.5 sustained)")

if __name__ == "__main__":
    main()
