import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Set up Streamlit page environment layout
st.set_page_config(page_title="Macro History Dashboard", layout="wide")

st.title("📈 100 Years of Macroeconomics (1925 - 2025)")
st.subheader("Dual-Axis tracking of Market Growth vs. Annual Inflation Rate")

# 1. Generate historical proxy data spanning 1925 to 2025
@st.cache_data
def load_historical_data():
    years = np.arange(1925, 2026)
    market_values = []
    current_val = 100.0
    
    np.random.seed(42)
    for y in years:
        if y >= 1929 and y <= 1932:  # Great Depression crash
            growth = np.random.uniform(-0.25, -0.10)
        elif y in [1937, 1938, 1945]: # Mid-century corrections
            growth = np.random.uniform(-0.15, -0.05)
        elif y in [1981, 1982]:      # Volcker Double-Dip correction
            growth = np.random.uniform(-0.12, -0.02)
        elif y in [2000, 2001, 2008, 2022]:  # Tech, GFC, and 2022 Bear Markets
            growth = np.random.uniform(-0.20, -0.05)
        else:                        # Standard compounding expansion years
            growth = np.random.uniform(0.05, 0.14)
            
        current_val *= (1 + growth)
        market_values.append(current_val)
        
    inflation_rates = []
    for y in years:
        if y >= 1930 and y <= 1933:   # Great Depression deflation
            inf = np.random.uniform(-10.0, -2.0)
        elif y in [1946, 1947]:       # Post-WWII supply shock inflation spike
            inf = np.random.uniform(8.0, 14.0)
        elif y >= 1973 and y <= 1981: # 1970s Great Inflation stagflation
            inf = np.random.uniform(6.0, 13.5)
        elif y in [2021, 2022]:       # Post-pandemic supply shock spikes
            inf = np.random.uniform(4.5, 8.0)
        else:                         # Standard targeted baseline stability
            inf = np.random.uniform(1.5, 3.5)
        inflation_rates.append(inf)

    df = pd.DataFrame({
        "Year": years,
        "Market_Value": market_values,
        "Inflation_Rate": inflation_rates
    })
    return df

raw_df = load_historical_data()

# --- 2. NEW: INTERACTIVE SIDEBAR TIMELINE CONTROL CONTROLLER ---
st.sidebar.header("🔍 Timeline Navigation Panel")
st.sidebar.markdown("Use the slider controls below to isolate specific historical eras and economic cycles.")

# Dual-thumb range slider to isolate years dynamically
start_year, end_year = st.sidebar.slider(
    label="Select Timeline Window Range",
    min_value=1925,
    max_value=2025,
    value=(1925, 2025), # Default state encapsulates full data scope
    step=1
)

# Apply runtime query filters to slice the primary dataframe index matrix
df = raw_df[(raw_df["Year"] >= start_year) & (raw_df["Year"] <= end_year)].copy()

# --- 3. SUMMARY METRICS LAYER ANALYSIS (Dynamically Sliced) ---
starting_val = df["Market_Value"].iloc[0]
ending_val = df["Market_Value"].iloc[-1]
growth_multiplier = ending_val / starting_val

peak_inflation_row = df.loc[df["Inflation_Rate"].idxmax()]
max_inflation_rate = peak_inflation_row["Inflation_Rate"]
max_inflation_year = peak_inflation_row["Year"]

max_deflation_row = df.loc[df["Inflation_Rate"].idxmin()]
max_deflation_rate = max_deflation_row["Inflation_Rate"]
max_deflation_year = max_deflation_row["Year"]

# Render dynamic metadata metric summaries
m_col1, m_col2, m_col3 = st.columns(3)
with m_col1:
    st.metric(
        label=f"Market Growth Multiplier ({start_year}-{end_year})", 
        value=f"{growth_multiplier:,.1f}x", 
        delta="Compounding Return"
    )
with m_col2:
    st.metric(
        label=f"Era Peak Inflation ({int(max_inflation_year)})", 
        value=f"{max_inflation_rate:.2f}%", 
        delta="Inflation Top", 
        delta_color="inverse"
    )
with m_col3:
    st.metric(
        label=f"Era Deepest Deflation ({int(max_deflation_year)})", 
        value=f"{max_deflation_rate:.2f}%", 
        delta="Deflation Floor"
    )

st.markdown("---")

# --- 4. COMPREHENSIVE HISTORICAL EVENTS REGISTRY (Updated) ---
events = [
    {
        "start": 1929, "end": 1933, "color": "rgba(255, 0, 0, 0.05)", 
        "label": "Great Depression", "hover": "Great Depression: Stock crash & asset over-supply cuts markets by 80%+"
    },
    {
        "start": 1937, "end": 1938, "color": "rgba(142, 68, 173, 0.06)", 
        "label": "1937 Roosevelt Recession", "hover": "Recession of 1937: Premature fiscal tightening and monetary contracting forces a severe economic relapse"
    },
    {
        "start": 1945, "end": 1946, "color": "rgba(22, 160, 133, 0.06)", 
        "label": "Post-WWII Shock", "hover": "Post-War Demobilization: War spending stops causing a short structural drop, followed by a massive lifting of price controls"
    },
    {
        "start": 1951, "end": 1952, "color": "rgba(52, 152, 219, 0.07)", 
        "label": "1951 Fed-Treasury Accord", "hover": "Fed Autonomy Regained (1951): Historic Accord separates the Fed from Treasury control, allowing independent rate hikes to crush post-war inflation"
    },
    {
        "start": 1959, "end": 1960, "color": "rgba(39, 174, 96, 0.07)", 
        "label": "1959 Vault Cash Act", "hover": "Vault Cash Expansion (1959): Fed allows banks to count on-hand cash as legal reserves, instantly unlocking billions for suburban home loans"
    },
    {
        "start": 1971, "end": 1972, "color": "rgba(241, 196, 15, 0.07)", 
        "label": "Nixon Shock", "hover": "Nixon Shock (1971): US abandons the gold standard, destroying the Bretton Woods system & sparking fiat asset devaluation"
    },
    {
        "start": 1973, "end": 1981, "color": "rgba(255, 165, 0, 0.05)", 
        "label": "Great Inflation", "hover": "Stagflation Crisis: Oil supply shocks trigger runaway interest rates & market friction"
    },
    {
        "start": 1979, "end": 1980, "color": "rgba(0, 200, 200, 0.08)", 
        "label": "Silver Run & Crash", "hover": "Silver Corner Crash: Hunt brothers corner 1/3 of global silver, sparking a huge commodity spike & immediate collapse"
    },
    {
        "start": 1981, "end": 1985, "color": "rgba(41, 128, 185, 0.06)", 
        "label": "Volcker Rate Hikes", "hover": "Reagan-Volcker Solution: Fed raises interest rates to a record 20% to crush hyper-inflation, triggering a deliberate double-dip recession"
    },
    {
        "start": 1995, "end": 2001, "color": "rgba(46, 204, 113, 0.06)", 
        "label": "Dot-com Bubble", "hover": "Dot-com Crash: Extreme speculation in internet startups peaks in 2000, wiping out trillions in tech valuations"
    },
    {
        "start": 2007, "end": 2008, "color": "rgba(128, 0, 128, 0.05)", 
        "label": "Housing Crash", "hover": "Great Recession: Subprime mortgage defaults trigger a 20%+ banking market decline"
    },
    {
        "start": 2011, "end": 2012, "color": "rgba(0, 128, 0, 0.06)", 
        "label": "Euro Sovereign Debt", "hover": "Eurozone Crisis: High government debt in Greece/Italy triggers banking sector panic & bailouts"
    },
    {
        "start": 2013, "end": 2013, "color": "rgba(241, 196, 15, 0.07)", 
        "label": "Taper Tantrum", "hover": "Emerging Market Turmoil: Fed hints at scaling back QE, causing mass capital flight from developing markets"
    },
    {
        "start": 2014, "end": 2015, "color": "rgba(70, 130, 180, 0.06)", 
        "label": "Oil Price Collapse", "hover": "Crude Oil Crash: Massive oversupply from US shale and OPEC policy shift crashes oil prices by 50%+"
    },
    {
        "start": 2015, "end": 2016, "color": "rgba(220, 20, 60, 0.06)", 
        "label": "Puerto Rico Debt", "hover": "Puerto Rican Debt Crisis: Government defaults on $70B+ debt, prompting US federal restructuring intervention"
    },
    {
        "start": 2018, "end": 2019, "color": "rgba(255, 20, 147, 0.06)", 
        "label": "Crypto Winter", "hover": "Crypto Crash: Initial Coin Offering (ICO) bubble bursts, wiping out over 80% of total crypto market valuation"
    },
    {
        "start": 2020, "end": 2021, "color": "rgba(255, 0, 0, 0.06)", 
        "label": "COVID-19 Financial Shock", "hover": "COVID Financial Crisis: Global pandemic lockdowns spark sudden recession, saved by historic central bank stimulus"
    },
    {
        "start": 2022, "end": 2023, "color": "rgba(231, 76, 60, 0.06)", 
        "label": "2022 Fed Tightening", "hover": "Modern Rate Shock: Fed aggressively hikes interest rates from 0% to 5.25%+ to stomp out post-pandemic inflation, sparking a 19% bear market correction"
    }
]

# Runtime filter: Only track events that cross inside the user's selected slider scope
filtered_events = [
    e for e in all_events if e["start"] <= end_year and e["end"] >= start_year
]

df["Historical_Event"] = "Stable Market Cycle"
for e in filtered_events:
    df.loc[(df["Year"] >= e["start"]) & (df["Year"] <= e["end"]), "Historical_Event"] = e["hover"]

# 5. Build interactive Plotly Object
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Year"], y=df["Market_Value"],
    name="Market Index Value", mode="lines",
    line=dict(color="#1f77b4", width=3)
))

fig.add_trace(go.Scatter(
    x=df["Year"], y=df["Inflation_Rate"],
    name="Inflation Rate %", mode="lines",
    line=dict(color="#ff7f0e", width=2, dash="dash"),
    yaxis="y2"
))

fig.add_trace(go.Scatter(
    x=df["Year"], y=[0] * len(df),
    name="Macro Event Note", mode="markers",
    marker=dict(opacity=0),
    text=df["Historical_Event"],
    hovertemplate="%{text}<extra></extra>",
    hoverinfo="text"
))

for e in filtered_events:
    # Constrain background drawing boxes strictly inside the chart's visible range limits
    box_start = max(e["start"], start_year)
    box_end = min(e["end"], end_year)
    fig.add_vrect(
        x0=box_start, x1=box_end,
        fillcolor=e["color"], opacity=1,
        layer="below", line_width=0
    )

fig.update_layout(
    xaxis_title="Timeline (Years)",
    yaxis_title="Total Market Index Base Value",
    xaxis=dict(range=[start_year, end_year]), # Explicitly clamps axis bounds
    yaxis=dict(
        title_font=dict(color="#1f77b4"),
        tickfont=dict(color="#1f77b4"),
        type="log"
    ),
    yaxis2=dict(
        title=dict(text="Annual Inflation Rate (%)", font=dict(color="#ff7f0e")),
        tickfont=dict(color="#ff7f0e"),
        anchor="x", overlaying="y", side="right", showgrid=False
    ),
    legend=dict(x=0.01, y=0.99, borderwidth=1),
    hovermode="x unified",
    height=650
)

st.plotly_chart(fig, use_container_width=True)

