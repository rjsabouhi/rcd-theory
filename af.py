
import streamlit as st
import numpy as np
from src.rcd_model import RCDModel
from app.memory_buffer import SymbolMemory

# --- Embedded RCD-Core Kernel ---
from typing import Dict

class RCDSystem:
    def __init__(self):
        self.H = {}
        self.M = []
        self.gamma = 1.0
        self.mu = 1.0
        self.entropy = 1.0
        self.theta = 1.0
        self.tau = 1.0
        self.drift = 0.0
        self.fate = "stabilize"

    def update_state(self, new_symbolic_input: Dict):
        self.H = new_symbolic_input
        self._update_memory()
        self._compute_drift()
        self._compute_time()
        self._determine_fate()

    def _update_memory(self):
        self.M.append(self.H.copy())
        if len(self.M) > 100:
            self.M.pop(0)

    def _compute_drift(self):
        self.gamma = 1 / (1 + self.theta * self.entropy)
        self.drift = self.mu * (1 - self.gamma)

    def _compute_time(self):
        self.tau = self.gamma * (self.mu + self.entropy)

    def _determine_fate(self):
        if self.drift < 0.2:
            self.fate = "recover"
        elif self.drift < 0.6:
            self.fate = "rebase"
        else:
            self.fate = "collapse"

    def get_metrics(self) -> Dict:
        return {
            "gamma": self.gamma,
            "mu": self.mu,
            "entropy": self.entropy,
            "theta": self.theta,
            "tau": self.tau,
            "drift": self.drift,
            "fate": self.fate
        }

# --- Streamlit App Starts Here ---
if "memory" not in st.session_state:
    st.session_state.memory = SymbolMemory()

if "rcd_core" not in st.session_state:
    st.session_state.rcd_core = RCDSystem()

st.title("Attractor Forge - RCD Simulation")

st.sidebar.header("Model Parameters")
symbol = st.sidebar.text_input("Symbolic Concept", value="self-worth")
alpha = st.sidebar.slider("Alpha (Θ - Clinging)", 0.0, 1.0, 0.7)
beta = st.sidebar.slider("Beta (μ - Memory Tension)", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("Delta (∇S - Entropy)", 0.0, 1.0, 0.1)
dimensions = st.sidebar.slider("Dimensions", 1, 20, 3)
noise = st.sidebar.slider("Noise Level", 0.0, 0.5, 0.1)

if st.button("Run Simulation"):
    st.session_state.memory.add(symbol, alpha, beta, delta)

    model = RCDModel()
    model.set_parameters(alpha=alpha, beta=beta, delta=delta,
                         n_dimensions=dimensions, noise_level=noise)

    def symbol_to_vector(symbol, dim):
        np.random.seed(abs(hash(symbol)) % (2**32))
        return np.random.normal(0, 0.1, dim)

    model.inject_H = symbol_to_vector(symbol + "_H", dimensions)
    model.inject_M = symbol_to_vector(symbol + "_M", dimensions)
    model.inject_R = hash(symbol + "_R") % 100 / 100.0

    st.write(f"Running simulation for: **{symbol}**")

    results = model.simulate(n_timesteps=100)

    # Update symbolic core with current state
    symbolic_input = {
        "symbol": symbol,
        "alpha": alpha,
        "beta": beta,
        "delta": delta
    }
    st.session_state.rcd_core.mu = beta
    st.session_state.rcd_core.entropy = delta
    st.session_state.rcd_core.theta = alpha
    st.session_state.rcd_core.update_state(symbolic_input)

    metrics = st.session_state.rcd_core.get_metrics()

    # Display symbolic memory buffer
    st.subheader("Symbolic Memory (recent inputs):")
    st.json(st.session_state.memory.get_recent())

    # Display symbolic system metrics
    st.subheader("RCD-Core Metrics:")
    st.metric("Phase Coherence γ(t)", f"{metrics['gamma']:.4f}")
    st.metric("Symbolic Time Drift τ(t)", f"{metrics['tau']:.4f}")
    st.metric("Identity Drift δ(t)", f"{metrics['drift']:.4f}")
    st.metric("System Fate ψ", metrics['fate'].upper())

    # Plot symbolic state evolution
    H_vals = [h[0] for h in results["H_states"]]
    M_vals = [m[0] for m in results["M_states"]]
    st.line_chart({"H(t)": H_vals, "M(t)": M_vals})

    dist = [np.linalg.norm(np.array(h) - np.array(m)) for h, m in zip(results["H_states"], results["M_states"])]
    st.line_chart({"‖H - M‖(t)": dist})
