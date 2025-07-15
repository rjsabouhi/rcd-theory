
print("✅ rcd_model.py loaded")

import numpy as np
from scipy.spatial import procrustes
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

class RCDModel:
    """
    Recursive Cognitive Dynamics Model Implementation

    This class implements the mathematical model for RCD including:
    - Recursive update equations for H(t) and M(t)
    - Phase synchronization computation
    - Semantic correlation analysis
    - Procrustes distance calculation
    - Recursive reflection loop dynamics
    """

    def __init__(self):
        self.alpha = 0.7  # Reflection persistence
        self.beta = 0.2   # Phase synchronization weight
        self.delta = 0.1  # Semantic correlation weight
        self.n_dimensions = 3
        self.noise_level = 0.1

        # Initialize states
        self.H = None  # User cognitive state
        self.M = None  # AI generative state
        self.R = 0.0   # Recursive reflection value

    def set_parameters(self, alpha, beta, delta, n_dimensions, noise_level):
        self.alpha = alpha
        self.beta = beta
        self.delta = delta
        self.n_dimensions = n_dimensions
        self.noise_level = noise_level

    def initialize_manifolds(self):
        self.H = np.random.randn(self.n_dimensions, self.n_dimensions)
        self.M = np.random.randn(self.n_dimensions, self.n_dimensions)
        self.R = np.random.uniform(0, 1)

    def compute_phase_synchronization(self, H, M):
        try:
            H_eigenvals = np.linalg.eigvals(H @ H.T)
            M_eigenvals = np.linalg.eigvals(M @ M.T)
            H_phases = np.angle(H_eigenvals)
            M_phases = np.angle(M_eigenvals)
            phase_diff = H_phases - M_phases
            gamma = np.abs(np.mean(np.exp(1j * phase_diff)))
            return gamma
        except:
            H_flat = H.flatten()
            M_flat = M.flatten()
            correlation = np.corrcoef(H_flat, M_flat)[0, 1]
            return max(0, correlation)

    def compute_semantic_correlation(self, H, M):
        H_flat = H.flatten()
        M_flat = M.flatten()
        try:
            correlation, _ = pearsonr(H_flat, M_flat)
            return correlation if not np.isnan(correlation) else 0.0
        except:
            return 0.0

    def compute_procrustes_distance(self, H, M):
        try:
            _, _, disparity = procrustes(H, M)
            return disparity
        except:
            return np.linalg.norm(H - M) / (np.linalg.norm(H) + np.linalg.norm(M) + 1e-8)

    def update_manifold_H(self, H, M, R):
        coupling = 0.3 * M @ M.T @ H
        reflection_term = R * np.eye(self.n_dimensions) @ H
        damping = 0.95 * H
        noise = self.noise_level * np.random.randn(*H.shape)
        H_new = damping + 0.1 * coupling + 0.05 * reflection_term + noise
        return H_new

    def update_manifold_M(self, M, H, R):
        coupling = 0.3 * H @ H.T @ M
        reflection_term = R * np.eye(self.n_dimensions) @ M
        damping = 0.95 * M
        noise = self.noise_level * np.random.randn(*M.shape)
        M_new = damping + 0.1 * coupling + 0.05 * reflection_term + noise
        return M_new

    def update_reflection(self, R_prev, gamma, rho):
        R_new = self.alpha * R_prev + self.beta * gamma + self.delta * rho
        R_new = np.clip(R_new, 0, 2)
        return R_new

    def simulate(self, n_timesteps):
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
            results['H_states'].append(self.H.copy())
            results['M_states'].append(self.M.copy())
            gamma = self.compute_phase_synchronization(self.H, self.M)
            rho = self.compute_semantic_correlation(self.H, self.M)
            d = self.compute_procrustes_distance(self.H, self.M)
            results['phase_sync'].append(gamma)
            results['semantic_corr'].append(rho)
            results['procrustes_dist'].append(d)
            results['reflection'].append(self.R)
            self.H = self.update_manifold_H(self.H, self.M, self.R)
            self.M = self.update_manifold_M(self.M, self.H, self.R)
            self.R = self.update_reflection(self.R, gamma, rho)

        return results

    def detect_coherence(self, results, threshold=0.95):
        phase_sync = np.array(results['phase_sync'])
        procrustes_dist = np.array(results['procrustes_dist'])
        coherent_mask = (phase_sync > threshold) & (procrustes_dist < (1 - threshold))
        return coherent_mask, np.where(coherent_mask)[0]
