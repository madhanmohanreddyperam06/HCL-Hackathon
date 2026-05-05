import streamlit as st
import pandas as pd
import json
import requests

# Backend API URLs
BACKEND_API = "https://hcl-final-hackathon-backend.onrender.com"
TRANSFORM_API = "https://hcl-final-hackathon-backend-2.onrender.com"

# Page configuration
st.set_page_config(
    page_title="Retail Sales Data ETL & Analytics Platform",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .center-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        padding: 1.5rem 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    .title-bar {
        width: 200px;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        margin: 0 auto 2rem auto;
        border-radius: 2px;
    }
    .center-header {
        text-align: center;
        font-size: 2rem;
        font-weight: 600;
        color: #667eea;
        padding: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Main title (centered)
st.markdown('<h1 class="center-title">Retail Sales Data ETL & Analytics Platform</h1>', unsafe_allow_html=True)
st.markdown('<div class="title-bar"></div>', unsafe_allow_html=True)

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
        key="csv_uploader",
        help="Upload your retail sales data in CSV format"
    )

    # Upload button
    if uploaded_file is not None:
        if st.button("Upload File"):
            try:
                files = {"file": uploaded_file}
                response = requests.post(f"{BACKEND_API}/upload", files=files)
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"File uploaded successfully! {result.get('rows', 0)} rows loaded.")
                    st.session_state['data_source'] = 'CSV Upload'
                    # Clear previous data
                    if 'df' in st.session_state:
                        del st.session_state['df']
                else:
                    st.error(f"Upload failed: {response.status_code}")
            except Exception as e:
                st.error(f"Error uploading file: {str(e)}")

    # Get Data button
    if st.button("Get Data"):
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
    
    # Get Data button
    if st.button("Get Data"):
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

# Divider
st.markdown("---")

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
    
    # Transform button
    st.markdown("---")
    if st.button("Transform"):
        st.session_state['show_transformation'] = True
        # Call transformation API
        try:
            response = requests.post(f"{TRANSFORM_API}/transform")
            if response.status_code == 200:
                result = response.json()
                st.session_state['transform_result'] = result
                st.success("Transformation completed successfully!")
            else:
                st.error(f"Transformation failed: {response.status_code}")
        except Exception as e:
            st.error(f"Error during transformation: {str(e)}")

# Phase 2: Transformation (hidden until Transform button is clicked)
if st.session_state.get('show_transformation', False):
    st.markdown("---")
    st.markdown('<h2 class="center-header">Phase 2: TRANSFORMATION</h2>', unsafe_allow_html=True)
    
    # Transformation options
    st.subheader("Data Transformation Options")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Run Transformation"):
            try:
                response = requests.post(f"{TRANSFORM_API}/transform")
                if response.status_code == 200:
                    result = response.json()
                    st.session_state['transform_result'] = result
                    st.success("Transformation completed successfully!")
                    st.rerun()
                else:
                    st.error(f"Transformation failed: {response.status_code}")
            except Exception as e:
                st.error(f"Error during transformation: {str(e)}")
    
    with col2:
        if st.button("Get Transform Report"):
            try:
                response = requests.get(f"{TRANSFORM_API}/transform/report")
                if response.status_code == 200:
                    report = response.json()
                    st.session_state['transform_report'] = report
                    st.success("Report fetched successfully!")
                else:
                    st.error(f"Failed to fetch report: {response.status_code}")
            except Exception as e:
                st.error(f"Error fetching report: {str(e)}")
    
    # Display transformation result if available
    if 'transform_result' in st.session_state:
        result = st.session_state['transform_result']
        
        st.subheader("Transformation Summary")
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Original Rows", result.get('total_rows', 0))
        with col2:
            st.metric("Total Columns", result.get('total_columns', 0))
        with col3:
            report = result.get('report', {})
            st.metric("Rows After Transform", report.get('rows_after_transform', 0))
        with col4:
            st.metric("Issues Fixed", len(report.get('issues_fixed', [])))
        
        # Display report details
        if 'report' in result:
            report = result['report']
            
            if report.get('issues_fixed'):
                st.subheader("Issues Fixed")
                for issue in report['issues_fixed']:
                    st.success(f"✓ {issue}")
            
            if report.get('features_added'):
                st.subheader("Features Added")
                for feature in report['features_added']:
                    st.info(f"+ {feature}")
            
            if report.get('validation_warnings'):
                st.subheader("Validation Warnings")
                for warning in report['validation_warnings']:
                    st.warning(f"⚠ {warning}")
            
            if report.get('final_columns'):
                st.subheader("Final Columns")
                st.write(", ".join(report['final_columns']))
        
        # Display aggregation summary
        if 'aggregation_summary' in result:
            st.subheader("Aggregation Summary")
            agg_summary = result['aggregation_summary']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if agg_summary.get('total_revenue'):
                    st.metric("Total Revenue", f"${agg_summary['total_revenue']:,.2f}")
                if agg_summary.get('total_orders'):
                    st.metric("Total Orders", f"{agg_summary['total_orders']:,}")
            with col2:
                if agg_summary.get('avg_order_value'):
                    st.metric("Avg Order Value", f"${agg_summary['avg_order_value']:,.2f}")
                if agg_summary.get('total_units_sold'):
                    st.metric("Total Units Sold", f"{agg_summary['total_units_sold']:,}")
            with col3:
                if agg_summary.get('unique_stores'):
                    st.metric("Unique Stores", agg_summary['unique_stores'])
                if agg_summary.get('unique_categories'):
                    st.metric("Unique Categories", agg_summary['unique_categories'])
        
        # View transformed data option
        st.markdown("---")
        if st.button("View Transformed Data"):
            try:
                response = requests.get(f"{TRANSFORM_API}/transformed")
                if response.status_code == 200:
                    data = response.json()
                    if data:
                        df = pd.DataFrame(data)
                        st.session_state['transformed_df'] = df
                        st.success(f"Loaded {len(df)} transformed records")
                    else:
                        st.warning("No transformed data available")
                else:
                    st.error(f"Failed to fetch transformed data: {response.status_code}")
            except Exception as e:
                st.error(f"Error fetching transformed data: {str(e)}")
    
    # Display transformed data if available
    if 'transformed_df' in st.session_state:
        st.subheader("Transformed Data Preview")
        df = st.session_state['transformed_df']
        st.dataframe(df, use_container_width=True, height=400)
