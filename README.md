# Retail Sales Data ETL & Analytics Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)
![Pandas](https://img.shields.io/badge/Pandas-2.2.0-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.0-teal)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive Streamlit-based application for Extracting, Transforming, and Loading retail sales data with advanced analytics capabilities. This platform provides a complete ETL pipeline with interactive visualizations and data insights.

## Features

### Phase 1: EXTRACTION

- **Data Ingestion**: Upload CSV files or fetch data from external APIs
- **Data Preview**: Interactive table display with sorting and filtering
- **Data Statistics**: Row count, column count, and data source information
- **Column Analysis**: Data types, null counts, and column information
- **External API Support**: Fetch data from approved domains (JSONPlaceholder, HCL APIs)

### Phase 2: TRANSFORMATION

- **Data Cleaning**: Automatic handling of null values, negative prices, and data inconsistencies
- **Feature Engineering**: Creation of derived columns (total_sales_amount, order_amount, date parts)
- **Data Validation**: Schema validation and quality checks
- **Transformation Report**: Detailed summary of issues fixed and features added
- **Aggregation Analysis**: Sales by store, category, month, and date

### Phase 3: LOAD

- **Transformation Results**: Preview of cleaned and transformed data
- **Database Integration**: Placeholder for database submission functionality
- **Data Persistence**: Storage of processed data for analytics

### Phase 4: ANALYTICS

- **Interactive Visualizations**: Bar charts, pie charts, line charts, and histograms
- **Sales Insights**: Revenue distribution, category performance, and store analysis
- **Trend Analysis**: Monthly sales trends and revenue patterns
- **Statistical Metrics**: Mean, median, and maximum revenue calculations

## Architecture

### Frontend (Streamlit)

- **UI Framework**: Streamlit for interactive web interface
- **Data Handling**: Pandas for data manipulation and analysis
- **Visualization**: Matplotlib for custom charts and graphs
- **Styling**: Custom CSS for enhanced UI/UX

### Backend Integration

- **ETL API**: FastAPI backend for data processing
- **Transformation Engine**: Advanced data cleaning and feature engineering
- **Aggregation Service**: Multi-dimensional data aggregation
- **External API Support**: RESTful API integration for data fetching

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

## Setup Steps

1. Clone the repository:

```bash
git clone https://github.com/madhanmohanreddyperam06/HCL-Hackathon.git
cd Retail-Sales-Data-ETL-Analytics-Platform
```

1. Create and activate virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

## Usage Guide

### Step 1: Data Extraction (Phase 1)

1. **Upload CSV File**:
   - Select "Upload CSV File" from the dropdown
   - Choose your retail sales data file
   - Click "Upload File" to send data to backend
   - Click "Get Data" to fetch and preview the uploaded data

2. **Fetch from External API**:
   - Select "Fetch from External API" from the dropdown
   - Enter API URL (supported domains: jsonplaceholder.typicode.com, hcl-hacthon-store-one-details-1.onrender.com)
   - Click "Fetch from External API" to retrieve data
   - Click "Get Data" to preview the fetched data

### Step 2: Data Transformation (Phase 2)

1. Click the "Transform" button after data is loaded
2. View transformation summary with metrics
3. Review issues fixed and validation warnings
4. Explore aggregation summaries (sales by store, category, month, date)

### Step 3: Data Loading (Phase 3)

1. Preview transformed data in "Transformation Results" section
2. Click "Submit to Database" to save processed data (placeholder functionality)

### Step 4: Analytics (Phase 4)

1. Select chart type from dropdown:
   - Sales by Store (Bar Chart)
   - Sales by Category (Pie Chart)
   - Sales by Month (Line Chart)
   - Revenue Distribution (Histogram)
2. View interactive visualizations with detailed statistics

## Supported File Formats

### Input Formats

- **CSV** (Comma Separated Values)
  - Standard retail sales data format
  - Supports large files with streaming
  - Automatic schema detection

- **JSON** (via External API)
  - RESTful API integration
  - Structured data format
  - Real-time data fetching

### Expected Schema

The application expects retail sales data with the following columns:

- `order_id`: Unique order identifier
- `order_date`: Date of the order (YYYY-MM-DD format)
- `store_id`: Store identifier
- `product_id`: Product identifier
- `product_category`: Product category
- `quantity_sold`: Number of units sold
- `unit_price`: Price per unit

## Backend APIs

### ETL Processing API

- **URL**: <https://hcl-final-hackathon-backend.onrender.com>
- **Endpoints**:
  - `POST /upload` - Upload CSV files
  - `GET /data` - Fetch uploaded data
  - `POST /fetch-external` - Fetch from external APIs

### Transformation API

- **URL**: <https://hcl-final-hackathon-backend.onrender.com>
- **Endpoints**:
  - `POST /transform` - Transform data
  - `GET /transformed` - Get transformed data
  - `GET /aggregations/*` - Get aggregated analytics
  - `POST /submit-to-database` - Submit to database (placeholder)

## Technology Stack

### Frontend

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Matplotlib**: Data visualization
- **Requests**: HTTP client for API calls
- **Python**: Core programming language

### Backend

- **FastAPI**: REST API framework
- **NumPy**: Numerical computing
- **PyArrow**: Data serialization
- **Python**: Core programming language

### DevOps

- **Git**: Version control
- **GitHub**: Code repository
- **Virtual Environment**: Dependency isolation
- **pip**: Package management

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

- **Repository**: <https://github.com/madhanmohanreddyperam06/HCL-Hackathon>
- **Issues**: <https://github.com/madhanmohanreddyperam06/HCL-Hackathon/issues>

## Acknowledgments

- Streamlit team for the amazing framework
- FastAPI community for the robust backend framework
- Pandas and NumPy teams for powerful data processing tools
