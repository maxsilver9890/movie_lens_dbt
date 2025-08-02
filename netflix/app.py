# app.py

import streamlit as st
import pandas as pd
import snowflake.connector
from queries import (
    top_rated_movies_summary,
    user_engagement,
    rating_over_the_years,
    tag_relevance_analysis
)

# 🚀 Snowflake connection
@st.cache_resource
def get_connection():
    return snowflake.connector.connect(
        user='maxsilver9890',
        password='wT8kiuNbHtUTBNf',
        account='PFOBQAM-IW03734',
        warehouse='COMPUTE_WH',
        database='MOVIELENS',
        schema='DEV'
    )

conn = get_connection()

# 🔍 Run query and return DataFrame
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        columns = [col[0] for col in cur.description]
        data = cur.fetchall()
    return pd.DataFrame(data, columns=columns)

# 🎨 Streamlit page setup
st.set_page_config(page_title="🎬 MovieLens Dashboard", layout="wide")

# Custom CSS for classy striped background and layout
# 🎨 Custom CSS for a classy, light, professional theme
st.markdown("""
    <style>
        /* --- Import Google Font --- */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

        /* --- Main Background --- */
        /* Pattern from https://www.heropatterns.com/ */
        body {
            background-color: #F0F2F6; /* A soft, light gray background */
            background-image: url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23DDE1E8' fill-opacity='0.6' fill-rule='evenodd'%3E%3Cpath d='M0 0h20v1H0zM0 2h20v1H0zM0 4h20v1H0zM0 6h20v1H0zM0 8h20v1H0zM0 10h20v1H0zM0 12h20v1H0zM0 14h20v1H0zM0 16h20v1H0zM0 18h20v1H0z'/%3E%3C/g%3E%3C/svg%3E");
        }

        /* --- Font and Text Color --- */
        .main, [data-testid="stSidebar"] * {
            font-family: 'Roboto', sans-serif;
            color: #1E1E1E; /* Dark gray for text for high contrast */
        }
        
        /* --- Floating Card Effect for Containers --- */
        .stDataFrame, .stChart, [data-testid="stMetric"], [data-testid="stSidebar"] {
            background-color: #FFFFFF; /* White background for cards */
            border: 1px solid #E6EAF1; /* A very light border */
            border-radius: 10px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.05); /* Soft shadow for depth */
            padding: 1.5rem;
            transition: box-shadow 0.3s ease-in-out;
        }

        .stDataFrame:hover, .stChart:hover, [data-testid="stMetric"]:hover {
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08); /* A slightly larger shadow on hover */
        }

        /* --- Headers and Title Styling --- */
        h1, h2, h3 {
            font-family: 'Roboto', sans-serif;
            font-weight: 700; /* Bolder headers */
            color: #005A9C; /* A professional blue for headers */
        }

        /* --- Sidebar Specifics --- */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            padding: 1rem;
        }

        /* --- Chart and DataFrame Styling --- */
        .stDataFrame, .stChart {
            margin-top: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎬 MovieLens Dashboard")
st.markdown("Welcome to the interactive dashboard powered by **Snowflake** and **Streamlit**. Use the sidebar to explore various analyses.")
st.divider()

# 📊 Sidebar for analysis selection
st.sidebar.header("🔎 Explore")
options = {
    "🎥 Top Rated Movies": top_rated_movies_summary,
    "👤 User Engagement": user_engagement,
    "📅 Rating Over the Years": rating_over_the_years,
    "🏷️ Tag Relevance Analysis": tag_relevance_analysis
}
selection = st.sidebar.radio("Select a section", list(options.keys()))

# 📦 Execute query
query = options[selection]()
df = run_query(query)
df.columns = [col.lower() for col in df.columns]

# 📈 Visualizations by section
st.subheader(selection)
st.markdown(" ")

if selection == "🎥 Top Rated Movies":
    st.markdown("### ⭐ Top Rated Movies")
    st.markdown("Shows the top movies based on average user ratings.")

    df["average_rating"] = pd.to_numeric(df["average_rating"], errors="coerce")
    top10 = df.sort_values("average_rating", ascending=False).head(10)

    st.bar_chart(top10.set_index("movie_title")["average_rating"])
    st.markdown(" ")
    st.dataframe(top10, use_container_width=True)

elif selection == "👤 User Engagement":
    st.markdown("### 👥 User Engagement Overview")
    st.markdown("How active are users based on number of ratings submitted?")

    df["number_of_ratings"] = pd.to_numeric(df["number_of_ratings"], errors="coerce")
    top_users = df.sort_values("number_of_ratings", ascending=False).head(30)

    st.line_chart(top_users.set_index("user_id")["number_of_ratings"])
    st.markdown(" ")
    st.dataframe(top_users, use_container_width=True)

elif selection == "📅 Rating Over the Years":
    st.markdown("### ⏳ Ratings Given Over the Years")
    st.markdown("Visualizes how user activity evolved year-by-year.")

    if "rating_year" in df.columns and "ratings_given" in df.columns:
        df["ratings_given"] = pd.to_numeric(df["ratings_given"], errors="coerce")
        st.line_chart(df.set_index("rating_year")["ratings_given"])
        st.markdown(" ")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No year-wise data available for visualization.")

elif selection == "🏷️ Tag Relevance Analysis":
    st.markdown("### 🏷️ Most Relevant Tags")
    st.markdown("Top tags used by users and their average relevance scores.")

    df["avg_relevance"] = pd.to_numeric(df["avg_relevance"], errors="coerce")
    top_tags = df.sort_values("avg_relevance", ascending=False).head(15)

    st.bar_chart(top_tags.set_index("tag_name")["avg_relevance"])
    st.markdown(" ")
    st.dataframe(top_tags, use_container_width=True)

# 📌 Footer
st.divider()
st.markdown("<center><small>© 2025 MovieLens Analytics | Built with ❤️ using Streamlit & Snowflake</small></center>", unsafe_allow_html=True)
