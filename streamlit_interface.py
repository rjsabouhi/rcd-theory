import streamlit as st
import numpy as np
from rcd_model import RCDModel

st.title("Attractor Forge - RCD Simulation")

# Sidebar parameters
st.sidebar.header("Model Parameters")
alpha = st.sidebar.slider("Alpha", 0.0, 1.0, 0.7)
beta = st.sidebar.slider("Beta", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("Delta", 0.0, 1.0, 0.1)
dimensions = st.sidebar.slider("Dimensions", 1, 20, 3)
noise = st.sidebar.slider("Noise Level", 0.0, 0.5, 0.1)

# Create and configure model
model = RCDModel()
model.set_parameters(alpha=alpha, beta=beta, delta=delta, n_dimensions=dimensions, noise_level=noise)

# Inject attractors
model.inject_H = np.random.randn(10) * 0.1
model.inject_M = np.random.randn(10) * 0.1
model.inject_R = 0.2

# Run simulation
results = model.simulate(n_timesteps=100)

# Preview parsed results (optional debug)
st.write("Example of raw output (first 5 steps):")
st.json({k: v[:5] for k, v in results.items()})

#Parse and plot
import numpy as np

# Extract and parse the first dimension of each H/M/R vector
H_vals = [h[0] for h in results["H_states"]]
M_vals = [m[0] for m in results["M_states"]]

# Plot them
st.line_chart({
    "H(t)": H_vals,
    "M(t)": M_vals,
})

st.write("Example of raw output (first 5 steps):")
st.json({k: v[:5] for k, v in results.items()})

# Display results
y_vals = [r[0] for r in results]
A_vals = [r[1] for r in results]

st.line_chart({"y(t)": y_vals, "A(t)": A_vals})
