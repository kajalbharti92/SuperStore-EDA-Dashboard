# Superstore EDA Dashboard

## Overview

This Streamlit-based dashboard performs exploratory data analysis (EDA) on a Superstore dataset, allowing users to visualize and analyze sales data. The dashboard includes charts, filters, and downloadable data for further analysis.

## Instructions

1. **Upload Data:**
   - Click on the file upload button (`:file_folder:`) to upload a CSV, TXT, XLS, or XLSX file containing the Superstore data.

2. **Date Range Selection:**
   - Select the start and end dates using the provided date input fields to filter the data based on the chosen date range.

3. **Filter Data:**
   - Use the sidebar to filter data based on Region, State, and City. The filters dynamically update the displayed charts.

4. **Category and Region Analysis:**
   - View category-wise sales and region-wise sales through interactive bar and pie charts.

5. **Time Series Analysis:**
   - Explore time series analysis with a line chart depicting monthly sales trends.

6. **Hierarchical View with Treemap:**
   - Visualize sales hierarchy using a treemap based on Region, Category, and Sub-Category.

7. **Segment and Category Pie Charts:**
   - Analyze sales distribution by segment and category using interactive pie charts.

8. **Month-wise Sub-Category Sales Summary:**
   - Access a summary table and a pivot table for month-wise sub-category sales.

9. **Scatter Plot:**
   - Examine the relationship between sales and profits using an interactive scatter plot.

10. **Download Data:**
    - Download the original dataset and selected analysis results as CSV files for further exploration.

## Code Explanation

The Python code utilizes Streamlit for the dashboard interface and Plotly for interactive visualizations. Data handling is performed using Pandas. The code is structured into sections, covering data upload, filtering, visualization, and data download.

## Setup

To run the code locally, make sure to have the required Python packages installed. You can install them using the following:

```bash
pip install streamlit plotly pandas

After installation, run the code using:

streamlit run filename.py

Replace filename.py with the actual filename containing the code.

Feel free to customize and extend the code for additional analyses or visualizations based on your specific needs.


Replace `filename.py` with the actual filename containing the code. This Markdown file provides a clear structure for users to understand the functionality and usage of the Superstore EDA Dashboard.

