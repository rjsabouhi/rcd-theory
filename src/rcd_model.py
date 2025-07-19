
import numpy as np
import random

class RCDModel:
    def __init__(self, dim=10, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        self.dim = dim
        self.initialize_manifolds()
        self.state = {
            'gamma': 0.7,  # Phase synchronization
            'rho': 0.5,    # Semantic correlation
        }
        self.gamma_buffer = []
        self.rho_buffer = []
        self.attractor_injections = []

    def initialize_manifolds(self):
        self.H = np.random.randn(self.dim)
        self.M = np.random.randn(self.dim)
        self.R = 0.1  # Initial reflection value

    def set_parameters(self, alpha=0.5, beta=0.1, delta=0.05, n_dimensions=10, noise_level=0.01):
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.dim = n_dimensions
        self.noise_level = noise_level
        self.initialize_manifolds()
        self.gamma_buffer = []
        self.rho_buffer = []
        self.attractor_injections = []

    def compute_phase_synchronization(self, H, M):
        return 1 - np.abs(np.dot(H, M) / (np.linalg.norm(H) * np.linalg.norm(M)))

    def compute_semantic_correlation(self, H, M):
        return np.corrcoef(H, M)[0, 1] if np.std(H) > 0 and np.std(M) > 0 else 0.0

    def compute_procrustes_distance(self, H, M):
        return np.linalg.norm(H - M)

    def update_reflection(self, R, gamma, rho, alpha=0.1):
        return R + alpha * (gamma + rho - R)

    def update_manifold_H(self, H, M, R):
        return H + 0.05 * (M - H) + R * np.random.randn(self.dim) * 0.01

    def update_manifold_M(self, M, H, R):
        return M + 0.05 * (H - M) + R * np.random.randn(self.dim) * 0.01

    def apply_memory_buffer(self, gamma, rho, window=5):
        self.gamma_buffer.append(gamma)
        self.rho_buffer.append(rho)
        if len(self.gamma_buffer) > window:
            self.gamma_buffer.pop(0)
            self.rho_buffer.pop(0)
        return np.mean(self.gamma_buffer), np.mean(self.rho_buffer)

    def maybe_stochastic_reactivation(self, gamma, rho, t, prob=0.05):
        if random.random() < prob:
            spike = random.choice(["gamma", "rho"])
            boost = random.uniform(0.5, 1.0)
            if spike == "gamma":
                gamma += boost
            else:
                rho += boost
        return gamma, rho

    def maybe_inject_attractor(self, t):
        for injection in self.attractor_injections:
            if injection["t"] == t:
                if injection["target"] == "H":
                    self.H += injection["vector"]
                elif injection["target"] == "M":
                    self.M += injection["vector"]
                elif injection["target"] == "R":
                    self.R += injection["value"]

    def simulate(self, n_timesteps=100):
        self.initialize_manifolds()
        results = {
            'H_states': [],
            'M_states': [],
            'phase_sync': [],
            'semantic_corr': [],
            'procrustes_dist': [],
            'reflection': []
        }

        for t in range(n_timesteps):
            self.maybe_inject_attractor(t)
            gamma = self.compute_phase_synchronization(self.H, self.M)
            rho = self.compute_semantic_correlation(self.H, self.M)
            gamma, rho = self.maybe_stochastic_reactivation(gamma, rho, t)
            gamma, rho = self.apply_memory_buffer(gamma, rho)

            results['H_states'].append(self.H.copy())
            results['M_states'].append(self.M.copy())
            results['phase_sync'].append(gamma)
            results['semantic_corr'].append(rho)
            results['procrustes_dist'].append(self.compute_procrustes_distance(self.H, self.M))
            results['reflection'].append(self.R)

            self.H = self.update_manifold_H(self.H, self.M, self.R)
            self.M = self.update_manifold_M(self.M, self.H, self.R)
            self.R = self.update_reflection(self.R, gamma, rho)

        return results

    def add_attractor_injection(self, t, target, vector=None, value=None):
        self.attractor_injections.append({
            "t": t,
            "target": target,
            "vector": vector,
            "value": value
        })
