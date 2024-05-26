import streamlit as st
import pandas as pd
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# Database connection
cnx = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='Bala@9944',
    database='myproject'
)

# Query to load the dataset
query = "SELECT * FROM airabnb"
df = pd.read_sql(query, cnx)
cnx.close()

# Streamlit app
st.title("Airbnb Listings Dashboard")

# Set a custom theme
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f5f5;
            color: #333;
        }
        .stTitle {
            color: #2e77d0;
        }
        .stSubheader {
            color: #2e77d0;
        }
    </style>
    """, unsafe_allow_html=True)

# Display DataFrame columns
st.write("Columns in the dataset:", df.columns)

# Basic statistics
st.subheader("Basic Statistics")
st.write(df.describe())

# Distribution of property types
st.subheader("Distribution of Property Types")
property_type_counts = df['property_type'].value_counts()
fig, ax = plt.subplots()
property_type_counts.plot(kind='bar', color='skyblue', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Average price per property type
st.subheader("Average Price per Property Type")
avg_price_property_type = df.groupby('property_type')['price'].mean()
fig, ax = plt.subplots()
avg_price_property_type.plot(kind='bar', color='lightgreen', ax=ax)
plt.xticks(rotation=45)
st.pyplot(fig)

# Room type distribution
st.subheader("Room Type Distribution")
room_type_counts = df['room_type'].value_counts()
fig, ax = plt.subplots()
ax.pie(room_type_counts, labels=room_type_counts.index, autopct='%1.1f%%', colors=sns.color_palette("pastel"))
st.pyplot(fig)

# Number of reviews distribution
st.subheader("Number of Reviews Distribution")
fig, ax = plt.subplots()
sns.histplot(df['number_of_reviews'], bins=30, kde=True, ax=ax, color='purple')
st.pyplot(fig)

# Review score rating distribution
st.subheader("Review Score Rating Distribution")
fig, ax = plt.subplots()
sns.histplot(df['review_score_rating'], bins=30, kde=True, ax=ax, color='orange')
st.pyplot(fig)

# Availability in the next 30 days
st.subheader("Availability in the Next 30 Days")
fig, ax = plt.subplots()
sns.histplot(df['availability_30'], bins=30, kde=True, ax=ax, color='teal')
st.pyplot(fig)

# Check if latitude and longitude columns exist
if 'latitude' in df.columns and 'longitude' in df.columns:
    # Geospatial visualization of listings
    st.subheader("Geospatial Visualization of Listings")
    df['latitude'] = df['latitude'].astype(float)
    df['longitude'] = df['longitude'].astype(float)
    st.map(df[['latitude', 'longitude']])

    # More detailed geospatial visualization with pydeck
    st.subheader("Detailed Geospatial Visualization")
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=200,
        pickable=True,
        opacity=0.8
    )

    view_state = pdk.ViewState(
        latitude=df['latitude'].mean(),
        longitude=df['longitude'].mean(),
        zoom=10,
        pitch=50
    )

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}\n{property_type}\n{price}"},
    )

    st.pydeck_chart(r)
else:
    st.write("Latitude and Longitude columns are not available in the dataset.")
