import streamlit as st
import pandas as pd

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Live News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    df = pd.read_csv("news_data.csv")
    df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
    return df

df = load_data()

# -------------------- SIDEBAR --------------------
st.sidebar.title("🔎 Filters")

categories = st.sidebar.multiselect(
    "Select Category",
    options=df['category'].unique(),
    default=df['category'].unique()
)

filtered_df = df[df['category'].isin(categories)]




# -------------------- TITLE --------------------
st.title("📰 Live News Analytics Dashboard")
st.markdown("Analyze real-time distribution of news categories")

# -------------------- METRICS --------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total Articles", len(filtered_df))
col2.metric("Total Categories", filtered_df['category'].nunique())
col3.metric("Top Category", filtered_df['category'].mode()[0])

st.markdown("---")

# -------------------- CHARTS --------------------
col1, col2 = st.columns(2)

# Bar Chart
with col1:
    st.subheader("📊 Category Distribution")
    st.bar_chart(filtered_df['category'].value_counts())

# Pie Chart (custom)
with col2:
    st.subheader("🥧 Category Share")
    st.write(filtered_df['category'].value_counts(normalize=True))

# -------------------- TIME TREND --------------------
st.subheader("📈 Category Trend Over Time")

filtered_df['date'] = filtered_df['publishedAt'].dt.date
trend = filtered_df.groupby(['date', 'category']).size().unstack()

st.line_chart(trend)

# -------------------- TOP SOURCES --------------------
st.subheader("🏢 Top News Sources")

st.bar_chart(filtered_df['source'].value_counts().head(10))

# -------------------- DATA TABLE --------------------
st.subheader("📋 Raw Data")

st.dataframe(filtered_df, use_container_width=True)

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown("Built with ❤️ by TEAM [Akash das ,Adityanath yadav ,Akash dalai & Ravikant kumar.]. Data sourced from [NewsAPI.org](https://newsapi.org/)")