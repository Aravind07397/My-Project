import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pymysql

# Establish connection
myconnection = pymysql.connect(host='127.0.0.1', user='root', passwd='Bala@9944', database="myproject")
cursor = myconnection.cursor()

# Load datasets
agg_transaction_df = pd.read_sql_query("SELECT * FROM agg_transaction", myconnection)
agg_user_df = pd.read_sql_query("SELECT * FROM agg_user", myconnection)
map_transcation_df = pd.read_sql_query("SELECT * FROM map_transcation", myconnection)
map_user_df = pd.read_sql_query("SELECT * FROM map_user", myconnection)
top_transcation_df = pd.read_sql_query("SELECT * FROM top_transcation", myconnection)
top_user_df = pd.read_sql_query("SELECT * FROM top_user", myconnection)

# Function to visualize data
def visualize_data(data_df, x_col, y_col, chart_type, title):
    if chart_type == "Bar Chart":
        fig = px.bar(data_df, x=x_col, y=y_col, title=title)
    elif chart_type == "Pie Chart":
        fig = px.pie(data_df, names=x_col, values=y_col, title=title)
    elif chart_type == "India Map":
        fig = px.choropleth_mapbox(
            data_df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            locations=x_col,
            color=y_col,
            color_continuous_scale="Viridis",
            range_color=(0, data_df[y_col].max()),
            mapbox_style="carto-positron",
            zoom=3,
            center={"lat": 20.5937, "lon": 78.9629},
            opacity=0.5,
            labels={y_col: y_col}
        )
        fig.update_geos(
            visible=False,
            lonaxis=dict(
                showgrid=True,
                gridwidth=0.5,
                range=[65, 100],
                dtick=5
            ),
            lataxis=dict(
                showgrid=True,
                gridwidth=0.5,
                range=[5, 40],
                dtick=5
            )
        )
    st.plotly_chart(fig)

# Sidebar options
datasets = {
    "Aggregate Transaction": agg_transaction_df,
    "Aggregate User": agg_user_df,
    "Mapped Transcation": map_transcation_df,
    "Mapped User": map_user_df,
    "Top Transcation": top_transcation_df,
    "Top User": top_user_df
}
selected_dataset = st.sidebar.selectbox("Select Dataset", list(datasets.keys()))

visualization_options = ["Bar Chart", "Pie Chart", "India Map"]  # Removed "Line Chart" option
selected_chart_type = st.sidebar.selectbox("Select Chart Type", visualization_options)

quarter_options = ["Quater 1", "Quater 2", "Quater 3", "Quater 4"]
selected_quarter = st.sidebar.selectbox("Select Quarter", quarter_options)

# Main content
st.title("PhonePe Pulse Data Visualization")

# Apply violet background color
st.markdown(
    """
    <style>
    .stApp {
        background-color: #8A2BE2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Change font styles for options
st.markdown(
    """
    <style>
    .sidebar .sidebar-content .row-widget .stMultiSelect .multiselect .multiselect-container .select-wrapper .dropdown-menu .dropdown-item .option:hover, .sidebar .sidebar-content .row-widget .stMultiSelect .multiselect .multiselect-container .select-wrapper .dropdown-menu .dropdown-item .option {
        font-family: 'Arial';
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display visualization
if selected_dataset.startswith("Top"):
    x_col = "Pincodes"
else:
    x_col = "state"  # Assuming state as x-axis for non-top datasets

y_col = "Transaction_count"  # Assuming transaction count as y-axis for all datasets
title = f"{selected_dataset} - {selected_chart_type} - {selected_quarter}"

# Filter data based on selected quarter
if selected_quarter == "Quater 1":
    filtered_data = datasets[selected_dataset][datasets[selected_dataset]["Quater"] == 1]
elif selected_quarter == "Quater 2":
    filtered_data = datasets[selected_dataset][datasets[selected_dataset]["Quater"] == 2]
elif selected_quarter == "Quater 3":
    filtered_data = datasets[selected_dataset][datasets[selected_dataset]["Quater"] == 3]
else:
    filtered_data = datasets[selected_dataset][datasets[selected_dataset]["Quater"] == 4]

visualize_data(filtered_data, x_col, y_col, selected_chart_type, title)
