import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# Set page config
st.set_page_config(page_title="Dashboard Overview", layout="wide")

# Function to load data
@st.cache_data
def load_data(sheet_url):
    df = pd.read_csv(sheet_url)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

# URL of the Google Sheet
sheet_url = "https://docs.google.com/spreadsheets/d/1JZ4gNmC9tW7w9xHq-NHYifW4Woq4Wx6B2XH1-W3yRck/export?format=csv"

# Load data
df = load_data(sheet_url)

# Get the latest timestamp
latest_timestamp = df['Timestamp'].max()

# Filter the DataFrame to get the row with the latest timestamp
latest_data = df[df['Timestamp'] == latest_timestamp]

# Create a subplot with 4 rows and 2 columns (4 charts + 4 tables)
fig = make_subplots(
    rows=4, cols=2,
    specs=[[{"type": "bar"}, {"type": "table"}], 
           [{"type": "bar"}, {"type": "table"}], 
           [{"type": "bar"}, {"type": "table"}], 
           [{"type": "bar"}, {"type": "table"}]],
    subplot_titles=("Jumlah Unit, Unit RFU, Unit BD", "Table for JUMLAH UNIT, RFU, and BD",
                    "Driver Status Distribution", "Table for Driver Status",
                    "Hauling Metrics", "Table for Hauling Metrics",
                    "Tonase and Fuel Metrics", "Table for Tonase and Fuel Metrics")
)

# Color scheme
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# Chart 1: Bar chart for JUMLAH UNIT, RFU, and BD
fig.add_trace(go.Bar(x=['Latest'], y=[latest_data['JUMLAH UNIT'].values[0]], name='JUMLAH UNIT', marker_color=colors[0]), row=1, col=1)
fig.add_trace(go.Bar(x=['Latest'], y=[latest_data['RFU'].values[0]], name='RFU', marker_color=colors[1]), row=1, col=1)
fig.add_trace(go.Bar(x=['Latest'], y=[latest_data['BD'].values[0]], name='BD', marker_color=colors[2]), row=1, col=1)


# Table for JUMLAH UNIT, RFU, and BD
table_data_1 = [['JUMLAH UNIT', latest_data['JUMLAH UNIT'].values[0]],
               ['RFU', latest_data['RFU'].values[0]],
               ['BD', latest_data['BD'].values[0]]]
fig.add_trace(go.Table(
    header=dict(
        values=['Metric', 'Value'],
        fill_color='#2c2c2c',  # Dark background for header
        align='left',
        font=dict(color='#e0e0e0', size=14)  # Light text, larger font
    ),
    cells=dict(
        values=list(zip(*table_data_1)),
        fill_color=['#242424', '#2a2a2a'],  # Alternating dark rows
        align='left',
        font=dict(color='#e0e0e0', size=12)  # Light text, slightly larger font
    )),
    row=1, col=2
)

# Chart 2: Bar chart for Driver statuses
driver_statuses = ['Driver Bekerja', 'Driver Sakit', 'Driver Cuti', 'Driver Off', 'Driver Ijin', 'Driver Alpha']
driver_data = latest_data[driver_statuses].sum().reset_index()
driver_data.columns = ['Driver Status', 'Count']
fig.add_trace(go.Bar(x=driver_data['Driver Status'], y=driver_data['Count'], name='Driver Status', marker_color=colors), row=2, col=1)

# Table for Driver Status
table_data_2 = driver_data.values.tolist()
fig.add_trace(go.Table(
    header=dict(
        values=['Driver Status', 'Count'],
        fill_color='#2c2c2c',  # Dark background for header
        align='left',
        font=dict(color='#e0e0e0', size=14)  # Light text, larger font
    ),
    cells=dict(
        values=list(zip(*table_data_2)),
        fill_color=['#242424', '#2a2a2a'],  # Alternating dark rows
        align='left',
        font=dict(color='#e0e0e0', size=12)  # Light text, slightly larger font
    )),
    row=2, col=2
)

# Chart 3: Bar chart for Hauling Metrics
hauling_metrics = ['Hauling Batubara', 'Support Washing Plant', 'Support HRM', 'Parkir']
hauling_values = [latest_data[metric].values[0] for metric in hauling_metrics]
fig.add_trace(go.Bar(x=hauling_metrics, y=hauling_values, name='Hauling Metrics', marker_color=colors[:4]), row=3, col=1)

# Table for Hauling Metrics
table_data_3 = list(zip(hauling_metrics, hauling_values))
fig.add_trace(go.Table(
    header=dict(
        values=['Hauling Metric', 'Value'],
        fill_color='#2c2c2c',  # Dark background for header
        align='left',
        font=dict(color='#e0e0e0', size=14)  # Light text, larger font
    ),
    cells=dict(
        values=list(zip(*table_data_3)),
        fill_color=['#242424', '#2a2a2a'],  # Alternating dark rows
        align='left',
        font=dict(color='#e0e0e0', size=12)  # Light text, slightly larger font
    )),
    row=3, col=2
)

# Chart 4: Bar chart for Tonase and Fuel Metrics
tonase_metrics = ['Tonase Terakhir dari WB', 'Jumlah Unit Hauling Belum Sampai Port', 'FUEL Consumption Terakhir', 'STOCK BB Terakhir di BUA']
tonase_values = [latest_data[metric].values[0] for metric in tonase_metrics]
fig.add_trace(go.Bar(x=tonase_metrics, y=tonase_values, name='Tonase and Fuel Metrics', marker_color=colors[:4]), row=4, col=1)

# Table for Tonase and Fuel Metrics
table_data_4 = list(zip(tonase_metrics, tonase_values))
fig.add_trace(go.Table(
    header=dict(
        values=['Tonase and Fuel Metric', 'Value'],
        fill_color='#2c2c2c',  # Dark background for header
        align='left',
        font=dict(color='#e0e0e0', size=14)  # Light text, larger font
    ),
    cells=dict(
        values=list(zip(*table_data_4)),
        fill_color=['#242424', '#2a2a2a'],  # Alternating dark rows
        align='left',
        font=dict(color='#e0e0e0', size=12)  # Light text, slightly larger font
    )),
    row=4, col=2
)

# Update layout for the entire figure
fig.update_layout(
    title_text='Dashboard Overview - Latest Data',
    title_font=dict(size=24),
    height=1200,
    margin=dict(l=40, r=40, t=100, b=40),
    font=dict(size=12),
    showlegend=False,
    plot_bgcolor='#F9F9F9',
    paper_bgcolor='#F9F9F9'
)

# Streamlit app
st.title('Dashboard Overview')
st.write(f"Latest Data: {latest_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

# Display the plot
st.plotly_chart(fig, use_container_width=True)

# Additional information or interactivity can be added here
st.write("This dashboard shows the latest data.")
