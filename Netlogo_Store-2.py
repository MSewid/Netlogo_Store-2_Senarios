import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel

# Set plot style
sns.set(style='whitegrid', palette='muted')

# Function to process and plot each scenario
def analyze_scenario(filename, title):
    st.markdown(f"### Scenario: {title}")
    
    # Load data
    df = pd.read_excel(filename)
    
    # Rename columns
    df.columns = ['x0', 'y0', 'x1', 'y1']
    
    # Plot cumulative sales
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['x0'], df['y0'], label='Store 0 (Boosted)', linewidth=2)
    ax.plot(df['x1'], df['y1'], label='Store 1 (Baseline)', linewidth=2, linestyle='--')
    ax.set_title(f'Cumulative Sales: {title}')
    ax.set_xlabel('Days Passed')
    ax.set_ylabel('Cumulative Sales')
    ax.legend()
    st.pyplot(fig)
    
    # Final cumulative sales
    final_store0 = df['y0'].iloc[-1]
    final_store1 = df['y1'].iloc[-1]
    
    st.write("**Final Cumulative Sales:**")
    st.write(f"- Store 0 (Boosted): {final_store0:.2f}")
    st.write(f"- Store 1 (Baseline): {final_store1:.2f}")
    
    if final_store1 > 0:
        perc_diff = ((final_store0 - final_store1) / final_store1) * 100
        st.success(f"→ Store 0 outperformed Store 1 by **{perc_diff:.2f}%**")
    else:
        st.warning("→ Store 1 has 0 sales — no valid percentage comparison.")
    
    # Paired t-test
    stat, p_value = ttest_rel(df['y0'], df['y1'])
    st.write("**Paired t-test on daily cumulative sales:**")
    st.write(f"- t-statistic = {stat:.4f}")
    st.write(f"- p-value = {p_value:.4f}")
    
    if p_value < 0.05:
        st.success("→ Statistically significant difference (p < 0.05)")
    else:
        st.info("→ No statistically significant difference (p ≥ 0.05)")

# Streamlit App Title
st.title("Retail Store Strategy Simulation Results")

# File Upload
uploaded_files = st.file_uploader("Upload 3 scenario Excel files", accept_multiple_files=True)

scenario_titles = [
    'Marketing-Driven Strategy (New Store)',
    'Service-Oriented Strategy (Luxury/Niche)',
    'Product Variety Focused Strategy (High-Traffic)'
]

# Run analysis if 3 files uploaded
if uploaded_files and len(uploaded_files) == 3:
    for file, title in zip(uploaded_files, scenario_titles):
        analyze_scenario(file, title)
elif uploaded_files:
    st.warning("Please upload all 3 scenario files.")
