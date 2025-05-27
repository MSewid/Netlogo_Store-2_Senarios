import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_rel

# Set plot style
sns.set(style='whitegrid', palette='muted')

# Function to process and plot each scenario
def analyze_scenario(filename, title):
    print(f"\n{'='*30}\nScenario: {title}\n{'='*30}")
    
    # Load data
    df = pd.read_excel(filename)
    
    # Rename columns if needed
    df.columns = ['x0', 'y0', 'x1', 'y1']
    
    # Plot cumulative sales
    plt.figure(figsize=(10, 5))
    plt.plot(df['x0'], df['y0'], label='Store 0 (Boosted)', linewidth=2)
    plt.plot(df['x1'], df['y1'], label='Store 1 (Baseline)', linewidth=2, linestyle='--')
    plt.title(f'Cumulative Sales: {title}')
    plt.xlabel('Days Passed')
    plt.ylabel('Cumulative Sales')
    plt.legend()
    plt.tight_layout()
    plt.show()
    
    # Final cumulative sales
    final_store0 = df['y0'].iloc[-1]
    final_store1 = df['y1'].iloc[-1]
    print(f"Final Cumulative Sales:")
    print(f"Store 0 (Boosted): {final_store0:.2f}")
    print(f"Store 1 (Baseline): {final_store1:.2f}")
    
    # % Difference
    if final_store1 > 0:
        perc_diff = ((final_store0 - final_store1) / final_store1) * 100
        print(f"→ Store 0 outperformed Store 1 by {perc_diff:.2f}%\n")
    else:
        print("→ Store 1 has 0 sales — no valid percentage comparison.\n")

    # Optional: Paired t-test on day-by-day cumulative sales
    stat, p_value = ttest_rel(df['y0'], df['y1'])
    print("Paired t-test on daily cumulative sales:")
    print(f"t-statistic = {stat:.4f}, p-value = {p_value:.4f}")
    if p_value < 0.05:
        print("→ Statistically significant difference between stores (p < 0.05)\n")
    else:
        print("→ No statistically significant difference (p ≥ 0.05)\n")

# Run the function for all 3 scenarios
analyze_scenario('NewStore_store-2plot.xlsx', 'Marketing-Driven Strategy (New Store)')
analyze_scenario('LuxStore_store-2plot.xlsx', 'Service-Oriented Strategy (Luxury/Niche)')
analyze_scenario('GroceryStore_store-2plot.xlsx', 'Product Variety Focused Strategy (High-Traffic)')