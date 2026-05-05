import streamlit as st
import pandas as pd
import json
import requests

# Backend API URL
BACKEND_API = "https://hcl-final-hackathon-backend.onrender.com"

# Page configuration
st.set_page_config(
    page_title="Retail Sales Data ETL & Analytics Platform",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS for centering
st.markdown("""
    <style>
    .center-title {
        text-align: center;
    }
    .center-header {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Main title (centered)
st.markdown('<h1 class="center-title">Retail Sales Data ETL & Analytics Platform</h1>', unsafe_allow_html=True)

# Section 1: EXTRACTION (centered)
st.markdown('<h2 class="center-header">Phase 1: EXTRACTION</h2>', unsafe_allow_html=True)

# Dropdown menu for feature selection
feature_option = st.selectbox(
    "Select Data Source",
    ["Upload CSV File", "Fetch from External API"],
    help="Choose how you want to load data into the system"
)

# Conditional display based on selection
if feature_option == "Upload CSV File":
    # File upload section
    st.subheader("Upload CSV file")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=['csv'],
        help="Upload your retail sales data in CSV format"
    )

    # Upload button
    if uploaded_file is not None:
        if st.button("Upload file"):
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{BACKEND_API}/upload", files=files)
                if response.status_code == 200:
                    st.success("File uploaded successfully to backend!")
                    st.session_state['data_source'] = 'CSV Upload'
                else:
                    st.error(f"Upload failed: {response.status_code}")
            except Exception as e:
                st.error(f"Error uploading file: {str(e)}")

elif feature_option == "Fetch from External API":
    # Fetch data from external API section
    st.subheader("Fetch Data from External API")

    api_url = st.text_input(
        "Enter API URL",
        placeholder="https://jsonplaceholder.typicode.com/users",
        help="Enter the URL of the external API to fetch data from"
    )

    st.info("Allowed domains: jsonplaceholder.typicode.com, hcl-hacthon-store-one-details-1.onrender.com")

    if st.button("Fetch from External API"):
        if api_url:
            try:
                payload = {"url": api_url}
                response = requests.post(f"{BACKEND_API}/fetch-external", json=payload)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Successfully fetched {result.get('count', 0)} records from external API")
                    if 'data' in result and result['data']:
                        df = pd.DataFrame(result['data'])
                        st.session_state['df'] = df
                        st.session_state['data_source'] = 'External API'
                else:
                    error_detail = response.json().get('detail', 'Unknown error') if response.headers.get('content-type', '').startswith('application/json') else response.text
                    st.error(f"Failed to fetch data: {error_detail}")
            except Exception as e:
                st.error(f"Error fetching from external API: {str(e)}")
        else:
            st.warning("Please enter an API URL")

# Divider
st.markdown("---")

# Fetch data from backend
st.subheader("Fetch Data")

col1, col2 = st.columns(2)
with col1:
    if st.button("Get All Data"):
        try:
            response = requests.get(f"{BACKEND_API}/data")
            if response.status_code == 200:
                data = response.json()
                if data:
                    df = pd.DataFrame(data)
                    st.session_state['df'] = df
                    st.session_state['data_source'] = 'Backend Cache'
                    st.success(f"Successfully fetched {len(df)} records")
                else:
                    st.warning("No data available on backend")
            else:
                st.error(f"Failed to fetch data: {response.status_code}")
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")

with col2:
    if st.button("Clear Backend Data"):
        try:
            response = requests.delete(f"{BACKEND_API}/clear")
            if response.status_code == 200:
                st.success("Backend data cleared successfully")
                if 'df' in st.session_state:
                    del st.session_state['df']
            else:
                st.error(f"Failed to clear data: {response.status_code}")
        except Exception as e:
            st.error(f"Error clearing data: {str(e)}")

# Display data if available
if 'df' in st.session_state:
    st.subheader("Raw Data Preview")
    df = st.session_state['df']
    
    # Display file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Rows", len(df))
    with col2:
        st.metric("Total Columns", len(df.columns))
    with col3:
        data_source = st.session_state.get('data_source', 'Backend Cache')
        st.metric("Data Source", data_source)
    
    # Display the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        height=400
    )
    
    # Display column information
    st.subheader("Column Information")
    col_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes.values,
        'Non-Null Count': df.count().values,
        'Null Count': df.isnull().sum().values
    })
    st.dataframe(col_info, use_container_width=True)
else:
    st.info("👆 Upload a CSV file to fetch data to view the raw data")
