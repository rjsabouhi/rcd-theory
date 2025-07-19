# simulation_runner.py

import numpy as np
from src.rcd_model import RCDModel
from src.reactivation_trigger import should_reactivate
from src.memory_buffer import RollingMemoryBuffer
from src.attractor_injection import inject_attractors

class SimulationRunner:
    """
    Orchestrates full-cycle RCD simulation with:
    - stochastic reactivation triggers (γ/ρ spikes)
    - rolling memory buffers (γ̄/ρ̄ smoothing)
    - attractor injection (symbolic modulation of H, M, R)
    """

    def __init__(self, timesteps=100, buffer_size=5, inject_schedule=None, reactivation_rate=0.1):
        self.timesteps = timesteps
        self.buffer_size = buffer_size
        self.inject_schedule = inject_schedule or {}  # e.g. {10: {"R": 0.5}, 50: {"H": [0.2]*10}}
        self.reactivation_rate = reactivation_rate

        self.model = RCDModel()
        self.model.initialize_manifolds()

        self.gamma_buffer = RollingMemoryBuffer(buffer_size)
        self.rho_buffer = RollingMemoryBuffer(buffer_size)

        self.results = {
            'H_states': [],
            'M_states': [],
            'phase_sync': [],
            'semantic_corr': [],
            'procrustes_dist': [],
            'reflection': []
        }

    def run(self):
        for t in range(self.timesteps):
            # Store states
            self.results['H_states'].append(self.model.H.copy())
            self.results['M_states'].append(self.model.M.copy())

            # Core metrics
            gamma = self.model.compute_phase_synchronization(self.model.H, self.model.M)
            rho = self.model.compute_semantic_correlation(self.model.H, self.model.M)
            d = self.model.compute_procrustes_distance(self.model.H, self.model.M)

            # Smooth with rolling memory
            gamma_smoothed = self.gamma_buffer.update(gamma)
            rho_smoothed = self.rho_buffer.update(rho)

            # Potentially reactivate
            if should_reactivate(t, self.reactivation_rate):
                gamma_smoothed += np.random.uniform(0.3, 0.7)
                rho_smoothed += np.random.uniform(0.3, 0.7)
                gamma_smoothed = min(gamma_smoothed, 1.0)
                rho_smoothed = min(rho_smoothed, 1.0)

            # Log metrics
            self.results['phase_sync'].append(gamma_smoothed)
            self.results['semantic_corr'].append(rho_smoothed)
            self.results['procrustes_dist'].append(d)
            self.results['reflection'].append(self.model.R)

            # Attractor injection (controlled symbolic modulation)
            if t in self.inject_schedule:
                inject_attractors(self.model, self.inject_schedule[t])

            # Update state
            self.model.H = self.model.update_manifold_H(self.model.H, self.model.M, self.model.R)
            self.model.M = self.model.update_manifold_M(self.model.M, self.model.H, self.model.R)
            self.model.R = self.model.update_reflection(self.model.R, gamma_smoothed, rho_smoothed)

            # Optional: print status
            print(f"t={t:03} | γ(t): {gamma_smoothed:.3f} | ρ(t): {rho_smoothed:.3f} | R(t): {self.model.R:.3f} | Λ(t): {1-d:.3f}")

        return self.results
