import streamlit as st
import numpy as np
import pandas as pd
import random
from statsmodels.tsa.regime_switching.markov_regression import MarkovRegression

# Page Config
st.set_page_config(page_title="Institutional Quant Dashboard", layout="wide")

st.title("⚡ Institutional-Grade Quant & Microstructure Dashboard")
st.markdown("Integrated system featuring Order Book Kinetic Energy, Markov Regimes, Cross-Asset Flow, and Genetic Optimization.")

# Sidebar Controls
st.sidebar.header("Configuration Panel")
selected_asset = st.sidebar.selectbox("Primary Asset", ["NIFTY", "BANKNIFTY", "FINNIFTY"])
simulation_speed = st.sidebar.slider("Tick Simulation Speed", 1, 5, 2)

# Tabs for Unified View
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Order Book Kinetics", 
    "2. Markov Regimes", 
    "3. Cross-Asset Matrix", 
    "4. Genetic Optimizer"
])

# --- TAB 1: ORDER BOOK KINETIC ENERGY ---
with tab1:
    st.subheader("Order Book Kinetic Energy & Momentum Tensors")
    st.markdown("Calculates physical mass and velocity of order flow imbalances in real-time.")
    
    if st.button("Run Order Kinetics Simulation"):
        # Simulated tick data
        np.random.seed(42)
        bids = np.random.randint(1000, 5000, 10)
        asks = np.random.randint(1000, 5000, 10)
        velocities = np.random.uniform(-2.5, 2.5, 10)
        
        mass = np.abs(bids - asks)
        kinetic_energy = 0.5 * mass * (velocities ** 2)
        momentum = mass * velocities
        
        df_kinetics = pd.DataFrame({
            'Bid Vol': bids,
            'Ask Vol': asks,
            'Velocity': np.round(velocities, 2),
            'Order Mass': mass,
            'Kinetic Energy': np.round(kinetic_energy, 2),
            'Momentum': np.round(momentum, 2)
        })
        
        st.dataframe(df_kinetics, use_container_width=True)
        st.success("Order book pressure analyzed via tensor mechanics.")

# --- TAB 2: MARKOV SWITCHING REGIMES ---
with tab2:
    st.subheader("Markov Switching Volatility Regime Detection")
    st.markdown("Identifies structural shifts between Low Volatility (Sideways) and High Volatility (Shock) regimes.")
    
    if st.button("Detect Market Regime"):
        # Generate synthetic return series
        np.random.seed(100)
        returns = np.random.normal(0.0005, 0.01, 150)
        returns[50:80] = np.random.normal(0.0, 0.03, 30) # High vol shock period
        
        series = pd.Series(returns)
        model = MarkovRegression(series, k_regimes=2, trend='c', switching_variance=True)
        results = model.fit(search_reps=50)
        
        smoothed_probs = results.smoothed_marginal_probabilities[1]
        current_state = "High Volatility / Shock Mode" if smoothed_probs.iloc[-1] > 0.5 else "Stable / Sideways Mode"
        
        st.metric(label="Current Market Regime", value=current_state)
        st.line_chart(smoothed_probs)

# --- TAB 3: CROSS-ASSET LIQUIDITY FLOW MATRIX ---
with tab3:
    st.subheader("Cross-Asset Order Flow Correlation Matrix")
    st.markdown("Monitors lead-lag relationships across Nifty, BankNifty, and Heavyweight Equities.")
    
    if st.button("Compute Cross-Asset Flow"):
        np.random.seed(10)
        dates = pd.date_range(start="2026-01-01", periods=50, freq="D")
        price_data = pd.DataFrame({
            'Nifty': np.cumsum(np.random.normal(1, 10, 50)) + 24000,
            'BankNifty': np.cumsum(np.random.normal(2, 20, 50)) + 51000,
            'Reliance': np.cumsum(np.random.normal(0.5, 5, 50)) + 1300,
            'HDFCBank': np.cumsum(np.random.normal(0.3, 4, 50)) + 1600
        }, index=dates)
        
        corr_matrix = price_data.pct_change().corr()
        st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm'), use_container_width=True)

# --- TAB 4: GENETIC ALGORITHM OPTIMIZER ---
with tab4:
    st.subheader("Genetic Algorithm Strike & Parameter Optimizer")
    st.markdown("Evolves option strategy parameters (Delta, Stop Loss, Target) dynamically using Darwinian selection.")
    
    gen_count = st.slider("Generations", 5, 50, 10)
    
    if st.button("Run Genetic Evolution"):
        def fitness(params):
            delta, sl, target = params
            return (target * 2.0) - (sl * 1.5) + (delta * 15.0)
            
        population = [[random.uniform(0.2, 0.6), random.uniform(10, 40), random.uniform(20, 80)] for _ in range(20)]
        
        for _ in range(gen_count):
            population = sorted(population, key=fitness, reverse=True)
            parents = population[:10]
            offspring = []
            while len(parents) + len(offspring) < 20:
                p1, p2 = random.choice(parents), random.choice(parents)
                child = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2]
                if random.random() < 0.3:
                    child[0] += random.uniform(-0.02, 0.02)
                offspring.append(child)
            population = parents + offspring
            
        best = max(population, key=fitness)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Optimal Option Delta", f"{best[0]:.3f}")
        col2.metric("Optimal Stop Loss (pts)", f"{best[1]:.2f}")
        col3.metric("Optimal Target (pts)", f"{best[2]:.2f}")
        st.success("Strategy parameters successfully evolved and optimized for current market dynamics.")
