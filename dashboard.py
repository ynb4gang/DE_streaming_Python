import os
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import logging

logging.basicConfig(
    filename="dashboard.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

st.set_page_config(
    page_title="Real Estate Streaming Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🏠 Real Estate Analytics Dashboard")
st.markdown("#### Real-Time Overview of the Real Estate Market")

uploaded_file = "data/aggregated_results.csv"
refresh_rate = 30

if not os.path.exists(uploaded_file):
    st.warning(f"The file `{uploaded_file}` is missing. Waiting for data to appear...")
    logging.warning("Data file not found. Retrying in 30 seconds...")
    time.sleep(refresh_rate)
    st.rerun()

def load_data():
    """
    Load the data from the specified CSV file.
    Returns a pandas DataFrame or an empty DataFrame if loading fails.
    """
    try:
        data = pd.read_csv(uploaded_file)
        data.columns = data.columns.str.strip()
        logging.info("Data loaded successfully.")
        return data
    except Exception as e:
        logging.error(f"Failed to load data: {e}")
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

data = load_data()

if not data.empty:
    st.sidebar.header("Data Filters")

    min_price, max_price = st.sidebar.slider(
        "Price Range (EUR):",
        min_value=0,
        max_value=int(data["Avg_Price"].max() or 1000000),
        value=(0, int(data["Avg_Price"].max() or 1000000))
    )

    min_area, max_area = st.sidebar.slider(
        "Area Range (m²):",
        min_value=0,
        max_value=int(data["Avg_Area"].max() or 1000),
        value=(0, int(data["Avg_Area"].max() or 1000))
    )

    selected_districts = st.sidebar.multiselect(
        "Select Districts:",
        options=data["District"].unique(),
        default=data["District"].unique()
    )

    selected_property_types = st.sidebar.multiselect(
        "Select Property Types:",
        options=data["Property_Type"].unique(),
        default=data["Property_Type"].unique()
    )

    filtered_data = data[
        (data["District"].isin(selected_districts)) &
        (data["Property_Type"].isin(selected_property_types)) &
        (data["Avg_Price"].between(min_price, max_price)) &
        (data["Avg_Area"].between(min_area, max_area))
    ]

    st.subheader("📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Average Price (EUR)", f"{filtered_data['Avg_Price'].mean():,.0f}")
    with col2:
        st.metric("Average Area (m²)", f"{filtered_data['Avg_Area'].mean():,.0f}")
    with col3:
        st.metric("Price per m² (EUR)", f"{filtered_data['Avg_Price_per_Sqm'].mean():,.0f}")
    with col4:
        st.metric("Listings", f"{filtered_data['Count'].sum():,.0f}")

    st.subheader("📈 Charts and Visualizations")

    fig1 = px.bar(
        filtered_data,
        x="District",
        y="Avg_Price",
        color="Property_Type",
        title="Average Price by District",
        color_discrete_sequence=px.colors.qualitative.Set2,
        text=None,
        labels={"Avg Price": "Average Price (EUR)", "District": "Districts"},
        template="plotly_dark",
        height=400
    )
    fig1.update_layout(
        xaxis_title="Districts",
        yaxis_title="Average Price (EUR)",
        title_x=0.5,
        title_font=dict(size=20, color="white"),
        plot_bgcolor="#111111"
    )
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        filtered_data,
        x="Property_Type",
        y="Avg_Price_per_Sqm",
        color="District",
        title="Average Price per m² by Property Type",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        text=None,
        labels={"Avg Price per Sqm": "Price per m² (EUR)", "Property Type": "Property Types"},
        template="plotly_dark",
        height=400
    )
    fig2.update_layout(
        xaxis_title="Property Types",
        yaxis_title="Price per m² (EUR)",
        title_x=0.5,
        title_font=dict(size=20, color="white"),
        plot_bgcolor="#111111"
    )
    st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(
        filtered_data,
        x="Avg_Price",
        nbins=50,
        title="Distribution of Property Prices",
        labels={"Avg Price": "Price (EUR)"},
        color_discrete_sequence=["#636EFA"],
        template="plotly_dark",
        height=400
    )
    fig3.update_layout(
        xaxis_title="Price (EUR)",
        yaxis_title="Frequency",
        title_x=0.5,
        title_font=dict(size=20, color="white"),
        plot_bgcolor="#111111"
    )
    st.plotly_chart(fig3, use_container_width=True)


    fig4 = px.scatter(
        filtered_data,
        x="Avg_Area",
        y="Avg_Price",
        color="Property_Type",
        title="Average Price vs. Area",
        color_discrete_sequence=px.colors.qualitative.Set1,
        labels={"Avg_Area": "Area (m²)", "Avg_Price": "Price (EUR)"},
        template="plotly_dark",
        height=400
    )
    fig4.update_layout(
        xaxis_title="Area (m²)",
        yaxis_title="Price (EUR)",
        title_x=0.5,
        title_font=dict(size=20, color="white"),
        plot_bgcolor="#111111"
    )
    st.plotly_chart(fig4, use_container_width=True)

    fig5 = px.bar(
        filtered_data,
        x="District",
        y="Avg_Price_per_Sqm",
        color="Property_Type",
        title="Price per m² by District",
        color_discrete_sequence=px.colors.qualitative.Set3,
        text=None,
        labels={"Avg_Price_per_Sqm": "Price per m² (EUR)", "District": "Districts"},
        template="plotly_dark",
        height=400
    )
    fig5.update_layout(
        xaxis_title="Districts",
        yaxis_title="Price per m² (EUR)",
        title_x=0.5,
        title_font=dict(size=20, color="white"),
        plot_bgcolor="#111111"
    )
    st.plotly_chart(fig5, use_container_width=True)

    fig6 = px.box(
        filtered_data,
        x="Property_Type",
        y="Avg_Price",
        color="Property_Type",
        title="Price Distribution by Property Type",
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={"Avg_Price": "Price (EUR)", "Property_Type": "Property Type"},
        template="plotly_dark",
        height=400
    )
    fig6.update_layout(
        xaxis_title="Property Types",
        yaxis_title="Price (EUR)",
        title_x=0.5,
        title_font=dict(size=20, color="white"),
        plot_bgcolor="#111111"
    )
    st.plotly_chart(fig6, use_container_width=True)

    import seaborn as sns
    import matplotlib.pyplot as plt

    corr_matrix = filtered_data[["Avg_Price", "Avg_Area", "Avg_Price_per_Sqm", "Count"]].corr()

    fig7, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", ax=ax, fmt=".2f", cbar_kws={'label': 'Correlation coefficient'})
    ax.set_title("Correlation Matrix", fontsize=20, color="white")
    plt.tight_layout()
    st.pyplot(fig7)

    fig8 = px.pie(
        filtered_data,
        names="District",
        values="Count",
        title="Distribution of Listings by District",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_dark",
        height=400
    )
    fig8.update_layout(
        title_x=0.5,
        title_font=dict(size=20, color="white"),
        plot_bgcolor="#111111"
    )
    st.plotly_chart(fig8, use_container_width=True)

    logging.info("Charts rendered successfully.")

    st.info(f"Last data update: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Dashboard updated at {time.strftime('%Y-%m-%d %H:%M:%S')}.")

    time.sleep(refresh_rate)
    st.rerun()
else:
    st.warning("No data available or file is empty. Waiting for new data...")
    logging.warning("No data available. Retrying in 30 seconds...")
    time.sleep(refresh_rate)
    st.rerun()
