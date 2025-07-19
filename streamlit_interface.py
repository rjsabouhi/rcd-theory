import streamlit as st
import numpy as np
from src.rcd_model import RCDModel
from app.memory_buffer import SymbolMemory

# Initialize in Streamlit session state
if "memory" not in st.session_state:
    st.session_state.memory = SymbolMemory()

st.title("Attractor Forge - RCD Simulation")

# Sidebar parameters
st.sidebar.header("Model Parameters")
symbol = st.sidebar.text_input("Symbolic Concept", value="self-worth")
alpha = st.sidebar.slider("Alpha", 0.0, 1.0, 0.7)
beta = st.sidebar.slider("Beta", 0.0, 1.0, 0.2)
delta = st.sidebar.slider("Delta", 0.0, 1.0, 0.1)
dimensions = st.sidebar.slider("Dimensions", 1, 20, 3)
noise = st.sidebar.slider("Noise Level", 0.0, 0.5, 0.1)

# Add current symbolic input to memory
# st.session_state.memory.add(symbol, alpha, beta, delta)
if st.button("Run Simulation"):

    # Add current symbolic input to memory
    st.session_state.memory.add(symbol, alpha, beta, delta)

    # Create and configure model
    model = RCDModel()
    model.set_parameters(alpha=alpha, beta=beta, delta=delta,
                         n_dimensions=dimensions, noise_level=noise)

    # Inject attractors
    def symbol_to_vector(symbol, dim):
        np.random.seed(abs(hash(symbol)) % (2**32))
        return np.random.normal(0, 0.1, dim)

    model.inject_H = symbol_to_vector(symbol + "_H", dimensions)
    model.inject_M = symbol_to_vector(symbol + "_M", dimensions)
    model.inject_R = hash(symbol + "_R") % 100 / 100.0

    st.write(f"Running simulation for: **{symbol}**")

    # Run simulation
    results = model.simulate(n_timesteps=100)

    # Display symbolic memory buffer
    st.subheader("Symbolic Memory (recent inputs):")
    st.json(st.session_state.memory.get_recent())

    # Extract H and M values
    H_vals = [h[0] for h in results["H_states"]]
    M_vals = [m[0] for m in results["M_states"]]

    # Plot H and M
    st.line_chart({"H(t)": H_vals, "M(t)": M_vals})

    # Compute and plot symbolic divergence
    import numpy as np
    dist = [np.linalg.norm(np.array(h) - np.array(m)) for h, m in zip(results["H_states"], results["M_states"])]
    st.line_chart({"‖H - M‖(t)": dist})

    # Optional debug: show result keys
    # st.write("Available result keys:", list(results.keys()))
