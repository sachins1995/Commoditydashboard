import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.colors
from homepage import LATEST_MODEL_RUN
from plotly.io import to_image

# Load data with caching for performance
@st.cache_data
def load_data():
    df = pd.read_excel('price_data.xlsx', sheet_name='shrimp')
    months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']
    df_melted = df.melt(
        id_vars=['Graph Type', 'Financial Year', 'Model', 'Count'],
        value_vars=months,
        var_name='Month',
        value_name='Value'
    )
    return df_melted

df = load_data()

# Default filters
default_graph_type = ['Price']
default_fy = ["2025-26","2024-25"]
default_models = ["Actual", LATEST_MODEL_RUN ]
default_count = ["60C"]


# Filter data based on default
filtered_df = df[
    (df['Graph Type'].isin(default_graph_type)) &
    (df['Financial Year'].isin(default_fy)) &
    (df['Model'].isin(default_models)) &
    (df['Count'].isin(default_count))
]

# Convert 'Value' column to numeric, coercing errors to NaN
filtered_df['Value'] = pd.to_numeric(filtered_df['Value'], errors='coerce')

def shrimp_graph(filtered_df, showlegend=True):
    fig = go.Figure()
    months_order = ['Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']
    color_list = plotly.colors.qualitative.Plotly
 # --- Price lines: dashed (model ≠ "Actual") go first (bottom), solid ("Actual") go after (top) ---
    price_entries = filtered_df[filtered_df['Graph Type'] == 'Price']
    # Dashed, not-Actual
    dashed_idxs = []
    solid_idxs = []
    for idx, (key, _) in enumerate(price_entries.groupby(['Financial Year', 'Model', 'Count'])):
        if key[1] != "Actual":
            dashed_idxs.append(idx)
        else:
            solid_idxs.append(idx)

    # Dashed lines (back/bottom, first)
    for plot_idx, idx in enumerate(dashed_idxs):
        key, group = list(price_entries.groupby(['Financial Year', 'Model', 'Count']))[idx]
        group = group.sort_values('Month', key=lambda x: [months_order.index(m) for m in x])
        label = f"Price - {key[0]} - {key[1]} - {key[2]}"
        color = color_list[idx % len(color_list)]
        fig.add_trace(go.Scatter(
            x=group['Month'],
            y=group['Value'],
            name=label,
            mode='lines+markers+text',
            marker=dict(color=color),
            line=dict(color=color, dash='dash'),
            yaxis='y1',
            text=group['Value'],
            textposition='top center',
            texttemplate='%{text:.0f}'
        ))

    # Solid lines ("Actual", always on top)
    for plot_idx, idx in enumerate(solid_idxs):
        key, group = list(price_entries.groupby(['Financial Year', 'Model', 'Count']))[idx]
        group = group.sort_values('Month', key=lambda x: [months_order.index(m) for m in x])
        label = f"Price - {key[0]} - {key[1]} - {key[2]}"
        color = color_list[idx % len(color_list)]
        fig.add_trace(go.Scatter(
            x=group['Month'],
            y=group['Value'],
            name=label,
            mode='lines+markers+text',
            marker=dict(color=color),
            line=dict(color=color, dash='solid'),
            yaxis='y1',
            text=group['Value'],
            textposition='top center',
            texttemplate='%{text:.0f}'
        ))

    # Layout
    fig.update_layout(
        xaxis=dict(title='Month', categoryorder='array', categoryarray=months_order),
        yaxis=dict(title='Price', side='left'),
        legend=dict(x=0.01, y=0.99),
        showlegend=showlegend,
        title='Monthly Shrimp Price Trend'
    )

    return fig

def shrimp_image():
    return to_image(shrimp_graph(filtered_df=filtered_df, showlegend=False))

if __name__ == "__main__":
    # Sidebar filters
    st.sidebar.header("Filter Options")
    # Only 'Price' will be available, but keep filter for consistency
    graph_types = st.sidebar.multiselect(
        "Graph Type", options=df['Graph Type'].unique(), default=default_graph_type
    )
    financial_years = st.sidebar.multiselect(
        "Financial Year", options=df['Financial Year'].unique(), default=default_fy
    )
    models = st.sidebar.multiselect(
        "Model", options=df['Model'].unique(), default=default_models
    )
    counts = st.sidebar.multiselect(
        "Count", options=df['Count'].unique(), default=default_count
    )

    # Filter data based on selections
    filtered_df = df[
        (df['Graph Type'].isin(graph_types)) &
        (df['Financial Year'].isin(financial_years)) &
        (df['Model'].isin(models)) &
        (df['Count'].isin(counts))
    ]

    # Convert 'Value' column to numeric, coercing errors to NaN
    filtered_df['Value'] = pd.to_numeric(filtered_df['Value'], errors='coerce')

    # Warn if any values could not be converted
    if filtered_df['Value'].isnull().any():
        st.warning("Some values in the 'Value' column could not be converted to numbers and are set as NaN.")

    # Title
    st.title("Shrimp Price Trend")

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        

        st.plotly_chart(shrimp_graph(filtered_df=filtered_df), use_container_width=True)

        # --- Placeholder Data Point Section ---
    st.markdown("## Model Accuracy Metrics")
    st.markdown("""
    | Metric                          | Value      |
    |----------------------------------|:----------:|
    | Next Month Model Accuracy        | -- %       |
    | 3rd Month Model Accuracy         | -- %       |
    | 6th Month Model Accuracy         | -- %       |
    | Seasonal Model Accuracy          | -- %       |
    | 3 Month Average Accuracy         | -- %       |
    | 6 Month Average Accuracy         | -- %       |
    | Next Month Directional Accuracy  | -- %       |
    """)