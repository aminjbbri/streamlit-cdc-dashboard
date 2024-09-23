import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Function to fetch data from CDC WONDER
def fetch_data(year, cause_of_death):
    # Example URL - Replace with the actual CDC WONDER API endpoint if available
    url = "https://data.cdc.gov/api/views/bi63-dtpu/rows.csv?accessType=DOWNLOAD"
    response = requests.get(url)
    if response.status_code == 200:
        data = StringIO(response.text)
        df = pd.read_csv(data)
        # Filter data based on year and cause_of_death
        filtered_df = df[(df['Year'] == year) & (df['Cause of Death'] == cause_of_death)]
        return filtered_df
    else:
        st.error("Failed to fetch data.")
        return pd.DataFrame()

# Title of the dashboard
st.title("US Causes of Death Dashboard")

# Sidebar for user inputs
st.sidebar.header("Filter Options")

# Example filters - adjust based on available data fields
year = st.sidebar.selectbox("Select Year", options=range(2000, 2024))
cause_of_death = st.sidebar.selectbox(
    "Select Cause of Death",
    options=["Heart Disease", "Cancer", "Accidents", "Stroke", "Chronic Lower Respiratory Diseases"]
)

# Fetch data based on user input
data = fetch_data(year, cause_of_death)

if not data.empty:
    st.subheader(f"Causes of Death in {year}: {cause_of_death}")
    st.dataframe(data)
    
    # Additional features: Sorting and Visualization
    sort_column = st.selectbox("Sort By", options=data.columns.tolist())
    sort_ascending = st.radio("Sort Order", options=["Ascending", "Descending"]) == "Ascending"
    sorted_data = data.sort_values(by=sort_column, ascending=sort_ascending)
    st.dataframe(sorted_data)
    
    # Example visualization
    st.bar_chart(sorted_data.set_index(sort_column)['Number of Deaths'])
else:
    st.write("No data available for the selected filters.")
