"""
Metric definitions for measuring recursive cognitive alignment.

Includes:
- Phase alignment (γ)
- Semantic correlation (ρ)
- Structural distance (d)
- Overall alignment (α)
- Meta-cognition (μ)
- Transformational gain (τ)
- Drift (δ)
"""

def gamma_t(H_t, M_t):
    """Phase alignment: rhythmic synchrony of reasoning."""
    return compute_phase_alignment(H_t, M_t)

def rho_t(H_t, M_t):
    """Semantic similarity at time t."""
    return compute_semantic_correlation(H_t, M_t)

def d_t(H_t, M_t):
    """Procrustes distance: structural shape difference."""
    return compute_procrustes_distance(H_t, M_t)

def alpha_t(gamma, rho, d):
    """Aggregate alignment metric."""
    return (gamma + rho) / (1 + d)

def mu_t(H_meta, M_meta):
    """Meta-cognitive depth estimation."""
    return measure_metacognitive_nesting(H_meta, M_meta)

def tau_t(prev_state, new_state):
    """Transformational gain across cycle."""
    return measure_state_difference(prev_state, new_state)

def delta_t(prev_alpha, curr_alpha):
    """Cognitive drift over time."""
    return abs(curr_alpha - prev_alpha)
