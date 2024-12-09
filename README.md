# DE_streaming-Python

## Overview

`DE_streaming_Python` is a real-time streaming and data aggregation system built in Python. It simulates streaming real estate data, processes the data, and presents the results through a dynamic Streamlit dashboard. This system handles large datasets, aggregates key metrics, and visualizes the data in real-time.

## Features

- **Data Simulation**: Simulates streaming of real estate data in batches from a CSV file.
- **Data Processing**: Filters, processes, and aggregates the data based on price, area, and other parameters.
- **Real-Time Dashboard**: Displays real-time analytics in a Streamlit dashboard with interactive charts and metrics.
- **Multithreading**: Uses multiple threads for streaming, processing, and aggregation in parallel.
- **Data Aggregation**: Aggregates data on-the-fly and saves the results to a CSV file for further analysis.

## Requirements

Make sure you have the following Python libraries installed:

```bash
pip install -r requirements.txt
```
## Libraries Used

### `pandas` - Data Manipulation and Analysis

[pandas](https://pandas.pydata.org/) is the go-to library for data manipulation and analysis in Python. In this project, `pandas` is used for:
- **Reading and loading data**: Efficiently loading large datasets from CSV files.
- **Data cleaning and transformation**: Handling missing values, converting columns, and reshaping the data.
- **Aggregating**: Grouping data by categories and calculating key metrics (average price, area, etc.).
- **Filtering**: Selecting data based on specific conditions (e.g., price range, area).

### `plotly` - Interactive Data Visualizations

[plotly](https://plotly.com/) is an advanced visualization library that creates interactive plots and dashboards. In this project, `plotly` is used for:
- **Creating interactive charts**: Dynamic bar charts, histograms, and other visualizations that allow users to explore data in real time.
- **Customization**: Adjusting colors, labels, axes, and layout to create engaging and informative charts.
- **Responsive design**: Ensuring that visualizations adjust well across different screen sizes, especially within the Streamlit dashboard.

### `streamlit` - Real-Time Dashboard Framework

[streamlit](https://streamlit.io/) is a powerful framework for creating real-time, interactive dashboards with minimal code. It is used in this project for:
- **Displaying real-time data**: As the data is streamed and processed, the dashboard updates automatically, showing key metrics and visualizations.
- **Interactive widgets**: Filters and controls such as sliders and dropdowns, allowing users to adjust parameters like price range and property types.
- **Rapid prototyping**: Streamlit's simplicity allows for fast development and iteration of the dashboard without the need for complex front-end code.

Together, these libraries enable the project to efficiently process and visualize real-time real estate data, offering an intuitive and responsive user interface.

## How It Works

This project simulates a real-time stream of real estate data and processes it in parallel to display dynamic analytics on a **Streamlit** dashboard. Here’s a breakdown of the key steps:

### 1. Simulate Streaming
The `simulate_stream()` function mimics a real-time data stream. It:
- Reads real estate data from a CSV file in **batches**.
- Pushes each record to a queue for further processing, simulating real-time ingestion.

### 2. Process the Data
The `process_batch()` function handles each batch of data:
- **Filters** the data based on specific conditions (e.g., price and area).
- Calculates the **average price per square meter** for each record.
- **Groups** the data by **District** and **Property_Type** for aggregation.

### 3. Handle the Stream
The `stream_handler()` function is responsible for:
- Continuously **consuming** records from the queue.
- **Processing data** in batches and aggregating results in real-time.
- Ensures the system can process data **in parallel**, maintaining real-time performance.

### 4. Aggregate Results
The `aggregate_results()` function:
- Periodically saves the aggregated results into a CSV file (`aggregated_results.csv`).
- The aggregation includes key metrics such as **average price**, **area**, **count**, and **price per square meter** for each **District** and **Property_Type**.

### 5. Streamlit Dashboard
The `dashboard.py` file hosts the **Streamlit** dashboard:
- **Displays real-time metrics** such as average price, area, price per square meter, and listings count.
- Provides **interactive filters** to adjust the **price range**, **area range**, and to select **districts** and **property types**.
- **Visualizes the data** in real-time with **interactive bar charts** and **histograms**.

With this flow, you can analyze and visualize real estate data as it streams, ensuring timely insights and actions.

## 6. Running the Application

To run the application, follow these steps:

### 1. Install Dependencies
Ensure that all required libraries are installed by running the following command:

```bash
pip install -r requirements.txt
```

### 2. Start the Streaming Process
Run the streaming, processing, and aggregation of data in the background by executing:
```bash
python stream_processing.py
```
This will initiate the real-time streaming, data processing, and aggregation processes.

### 3. Launch the Streamlit Dashboard
Open the **Streamlit** dashboard to visualize the real-time analytics by running:
```bash
streamlit run c:/Users/user/location_project/DE_streaming_Python/main.py
```

## Logs

The application generates two key log files that track the activity and errors during its execution:

### 1. **`dashboard.log`**
- **Purpose**: Contains logs related to the **Streamlit dashboard**.
- **Contents**: Logs will include data loading errors, updates on data visualization, and any issues encountered during dashboard operations.
- **Usefulness**: This log is important for monitoring the dashboard's performance and troubleshooting any visualization-related problems.

### 2. **`stream_processing.log`**
- **Purpose**: Logs related to **data streaming, processing, and aggregation**.
- **Contents**: This file tracks the data flow, records processed batches, and includes any errors or warnings during the simulation and aggregation processes.
- **Usefulness**: It's vital for tracking the progress of the data stream and for debugging issues in the data processing pipeline.

### Why You Need These Logs:
- **Troubleshooting**: If any errors occur during the data streaming, processing, or dashboard updates, these logs will help you identify and resolve issues.
- **Tracking Progress**: You can monitor the application's progress by checking these logs for details on which stage the system is at, whether it’s data streaming or rendering the dashboard.