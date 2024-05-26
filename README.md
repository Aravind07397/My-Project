# PhonePe Pulse Data Visualization

This project aims to visualize PhonePe Pulse data using Streamlit, Plotly, MySQL, and Pandas. PhonePe Pulse is a collection of data insights on digital payments trends and consumer behavior.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)

## Introduction

The PhonePe Pulse Data Visualization project offers an interactive web application to visualize various data insights related to digital transactions and user behavior on the PhonePe platform. It leverages Streamlit for the web application framework, Plotly for interactive visualizations, MySQL for data storage, and Pandas for data manipulation.

## Features

- Visualize aggregated transaction data by state, year, and quarter.
- Analyze user behavior patterns based on transaction counts, brands, and percentages.
- Explore mapped transaction and user data by state and district.
- Identify top transactions and users based on transaction counts and registered users.
- Interactive pie charts, bar charts, and choropleth maps for data visualization.
- Filter data by quarter for deeper analysis.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Document Information Extractor
The Document Information Extractor is a Python-based project aimed at extracting structured data from various document formats, including PDFs, Word documents, and plain text files. This tool is particularly useful for automating the extraction of specific data points or metadata from documents, streamlining the process of information retrieval and analysis.

## Features
Multi-format Support: Extract information from PDFs, Word documents, and plain text files.
Customizable Extraction: Define rules and patterns to extract specific data points or metadata from documents.
Structured Output: Output extracted information in a structured format, such as JSON or CSV, for further analysis and processing.
Scalability: Process large collections of documents efficiently, thanks to optimized extraction algorithms.
Ease of Use: Simple command-line interface for initiating document extraction with minimal configuration.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Airbnb Data Visualization Dashboard

This project is a Streamlit application for visualizing Airbnb listings data. The dashboard provides various insights such as basic statistics, distribution of property types, average prices, room type distributions, and more. It also includes geospatial visualizations if the dataset contains latitude and longitude information.

## Features

- **Basic Statistics**: Summary statistics of the dataset.
- **Distribution of Property Types**: Bar chart showing the count of different property types.
- **Average Price per Property Type**: Bar chart showing the average price for each property type.
- **Room Type Distribution**: Pie chart showing the distribution of different room types.
- **Number of Reviews Distribution**: Histogram showing the distribution of the number of reviews.
- **Review Score Rating Distribution**: Histogram showing the distribution of review scores.
- **Availability in the Next 30 Days**: Histogram showing the availability of listings in the next 30 days.
- **Geospatial Visualization**: Map and detailed visualization of listings (if latitude and longitude columns are present).

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/airbnb-visualization.git
    cd airbnb-visualization
    ```

2. **Set up a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the MySQL database**:
    - Ensure you have MySQL installed and running.
    - Create a database named `myproject`.
    - Import your Airbnb dataset into a table named `airabnb`.

5. **Configure the database connection**:
    - Update the database connection parameters in `app.py` (host, user, password, database) to match your MySQL setup.

## Running the Application

Run the following command to start the Streamlit application:

```bash
streamlit run app.py
