# app.py

import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
import time # New import for animation
from cryptography.hazmat.primitives import serialization
# Import queries from your file
from queries1 import (
    top_rated_movies_summary,
    user_engagement,
    rating_over_the_years,
    tag_relevance_analysis,
    genre_analysis # New import
)

st.title("🕵️ Secrets Inspector")

# Check if the 'snowflake' section exists
if hasattr(st.secrets, "snowflake"):
    st.success("✅ 'snowflake' section was found in your secrets!")
    st.info("Check the keys below to ensure they are all correct.")
    # Display the keys found within the [snowflake] section
    st.write(st.secrets.snowflake.keys())
else:
    st.error("❌ The 'snowflake' section was NOT found.")
    st.warning("Below are all the secrets the app can see. Check for typos in the section header (e.g., 'snowflak' instead of 'snowflake').")
    # Display all available secrets to find the typo
    st.write(st.secrets.to_dict())

st.stop() # Stop the rest of the app from running
# --- END OF DEBUGGING CODE ---


# --- Page Configuration ---
st.set_page_config(
    page_title="MovieLens Pro Dashboard",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Styling ---
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

        html, body, [class*="st-"], [class*="css-"] {
            font-family: 'Inter', sans-serif;
        }

        /* --- Main Background & Theme --- */
        body {
            background-color: #0a0a1a; /* Deep blue-black */
            color: #EAEAEA;
        }
        .main {
            background-image: radial-gradient(circle at 50% 0%, rgba(76, 0, 255, 0.2), rgba(0,0,0,0) 30%),
                              radial-gradient(circle at 0% 100%, rgba(255, 0, 110, 0.15), rgba(0,0,0,0) 40%),
                              radial-gradient(circle at 100% 100%, rgba(0, 179, 255, 0.15), rgba(0,0,0,0) 40%);
            background-attachment: fixed;
        }

        /* --- Glassmorphism Cards --- */
        [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
            background: rgba(10, 10, 26, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
        }
        
        /* --- Sidebar --- */
        [data-testid="stSidebar"] {
            background: rgba(10, 10, 26, 0.8);
            border-right: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* --- Headers & Text --- */
        h1, h2, h3 {
            font-weight: 700;
            color: #FFFFFF;
        }
        .st-emotion-cache-10trblm {
            text-align: center;
        }
        
        /* --- Custom Metric Styling for Animation --- */
        .metric-container {
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 1.5rem 1rem;
            text-align: center;
        }
        .metric-label {
            font-size: 1.1rem;
            color: #A0A0B0;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #FFFFFF;
        }

        /* --- Footer --- */
        .footer {
            text-align: center;
            padding: 1rem;
            color: #A0A0B0;
            font-size: 0.9rem;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()
#-----------------------------------------------
#Credentials
# from dotenv import load_dotenv
# import os
# load_dotenv()

# --- Snowflake Connection ---
# @st.cache_resource
# def get_connection():
#     try:
#         return snowflake.connector.connect(
#             user=os.getenv("SNOWFLAKE_USER"),
#             password=os.getenv("SNOWFLAKE_PASSWORD"),
#             account=os.getenv("SNOWFLAKE_ACCOUNT"),
#             warehouse='COMPUTE_WH',
#             database='MOVIELENS',
#             schema='DEV'
#         )
#     except Exception as e:
#         st.error(f"❄️ Snowflake connection failed. Please check your credentials and network. Error: {e}")
#         return None

# --- Snowflake Connection ---
@st.cache_resource
def get_connection():
    """Establishes a connection to Snowflake using a private key from Streamlit secrets."""
    try:
        # Load encrypted private key from Streamlit secrets
        p_key_bytes = st.secrets.snowflake.private_key.encode('utf-8')
        
        # Decrypt the private key
        private_key = serialization.load_pem_private_key(
            p_key_bytes,
            password=st.secrets.snowflake.private_key_passphrase.encode('utf-8')
        )
        
        # Get the private key in PKCS8 format for the connector
        pkcs8_private_key = private_key.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Establish the connection using st.secrets
        return snowflake.connector.connect(
            user=st.secrets.snowflake.user,
            account=st.secrets.snowflake.account,
            warehouse=st.secrets.snowflake.warehouse,
            database=st.secrets.snowflake.database,
            schema=st.secrets.snowflake.schema,
            private_key=pkcs8_private_key  # Use the decrypted private key
        )
    except Exception as e:
        st.error(f"❄️ Snowflake connection failed. Please check your credentials and network. Error: {e}")
        return None

conn = get_connection()
if conn is None:
    st.stop()


# --- Data Fetching ---
@st.cache_data(ttl=600)
def run_query(query):
    if conn is None:
        st.warning("Cannot run query; Snowflake connection is not available.")
        return pd.DataFrame()
    
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            columns = [col[0].lower() for col in cur.description]
            return pd.DataFrame(cur.fetchall(), columns=columns)
    except Exception as e:
        st.error(f"❌ Query execution failed for the '{selection}' section.")
        st.code(query, language="sql")
        st.error(f"Error details: {e}")
        return pd.DataFrame()

# Helper function to display styled dataframes
def display_styled_dataframe(df, cmap, subset, formatter=None):
    try:
        styler = df.style
        if formatter:
            styler = styler.format(formatter)
        styler = styler.background_gradient(cmap=cmap, subset=subset)
        st.dataframe(styler, use_container_width=True)
    except ImportError:
        st.info("💡 To see color gradients in the table, please install matplotlib: `pip install matplotlib`")
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not apply table styling. Displaying raw data. Error: {e}")
        st.dataframe(df, use_container_width=True)


# --- Sidebar Navigation ---
with st.sidebar:
    st.title("💎 MovieLens Pro")
    st.markdown("---")
    
    options = {
        "Executive Summary": "executive_summary",
        "Genre Analysis": "genre_analysis",
        "Top Rated Movies": "top_rated_movies",
        "User Engagement": "user_engagement",
        "Rating Trends": "rating_trends",
        "Tag Analysis": "tag_analysis"
    }
    
    selection = st.radio("Select Analysis", list(options.keys()), key="navigation")

# --- Main Dashboard ---
st.title("🎬 MovieLens Analytics Dashboard")
st.markdown("---")

# --- Page Routing ---
if selection == "Executive Summary":
    st.subheader("🚀 At a Glance: The State of Cinema")
    
    movies_df = run_query("SELECT COUNT(*) FROM MOVIELENS.DEV.dim_movies;")
    ratings_df = run_query("SELECT COUNT(*), COUNT(DISTINCT user_id) FROM MOVIELENS.DEV.fct_ratings;")
    
    if not ratings_df.empty:
        total_movies = int(movies_df.iloc[0,0])
        total_ratings = int(ratings_df.iloc[0,0])
        total_users = int(ratings_df.iloc[0,1])

        # --- ANIMATION LOGIC STARTS HERE ---
        col1, col2, col3 = st.columns(3)
        
        # Create placeholders for the metrics
        with col1:
            movie_metric = st.empty()
        with col2:
            rating_metric = st.empty()
        with col3:
            user_metric = st.empty()

        # Animate the numbers
        for i in range(101):
            # Calculate the current value for each metric
            current_movies = int(total_movies * (i/100))
            current_ratings = int(total_ratings * (i/100))
            current_users = int(total_users * (i/100))
            
            # Update the placeholders with custom HTML for styling
            movie_metric.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Total Movies Analyzed 🍿</div>
                    <div class="metric-value">{current_movies:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
            rating_metric.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Total Ratings Submitted 🌟</div>
                    <div class="metric-value">{current_ratings:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
            user_metric.markdown(f"""
                <div class="metric-container">
                    <div class="metric-label">Unique Active Users 👥</div>
                    <div class="metric-value">{current_users:,}</div>
                </div>
            """, unsafe_allow_html=True)
            
            time.sleep(0.01) # Control the speed of the animation

        # Ensure the final, correct numbers are displayed
        movie_metric.markdown(f"""<div class="metric-container"><div class="metric-label">Total Movies Analyzed 🍿</div><div class="metric-value">{total_movies:,}</div></div>""", unsafe_allow_html=True)
        rating_metric.markdown(f"""<div class="metric-container"><div class="metric-label">Total Ratings Submitted 🌟</div><div class="metric-value">{total_ratings:,}</div></div>""", unsafe_allow_html=True)
        user_metric.markdown(f"""<div class="metric-container"><div class="metric-label">Unique Active Users 👥</div><div class="metric-value">{total_users:,}</div></div>""", unsafe_allow_html=True)
        # --- ANIMATION LOGIC ENDS HERE ---

    else:
        st.warning("Could not fetch summary data. Please check the connection and queries.")
    
    st.markdown("---")
    st.info("💡 **Welcome!** This dashboard provides a deep dive into the MovieLens dataset. Use the sidebar to navigate through different analytical views.", icon="💎")

else:
    query_function_map = {
        "Genre Analysis": genre_analysis,
        "Top Rated Movies": top_rated_movies_summary,
        "User Engagement": user_engagement,
        "Rating Trends": rating_over_the_years,
        "Tag Analysis": tag_relevance_analysis
    }
    
    query_func = query_function_map.get(selection)
    
    if query_func:
        df = run_query(query_func())
        
        if df.empty:
            st.warning(f"The query for the '{selection}' section ran successfully but returned no data. Your dashboard appears empty because there's nothing to display. Please check your data source or the query logic in `queries.py`.")
        else:
            if selection == "Genre Analysis":
                st.subheader("🎭 Deep Dive into Movie Genres")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.markdown("#### 📊 Genre Distribution")
                    fig_pie = px.pie(df.head(10), names='genre', values='number_of_movies', title='Top 10 Genres by Movie Count', hole=0.4)
                    fig_pie.update_traces(textinfo='percent+label', pull=[0.05]*10)
                    st.plotly_chart(fig_pie, use_container_width=True)
                with col2:
                    st.markdown("#### ⭐ Average Rating by Genre")
                    df_sorted = df.sort_values('average_rating', ascending=False)
                    fig_bar = px.bar(df_sorted, x='genre', y='average_rating', title='Average User Rating per Genre', color='average_rating', color_continuous_scale=px.colors.sequential.Viridis)
                    st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown("#### 🔢 Full Genre Data")
                df_to_display = df.sort_values('number_of_movies', ascending=False)
                display_styled_dataframe(df_to_display, 'viridis', ['average_rating'], formatter={'average_rating': '{:.2f}'})

            elif selection == "Top Rated Movies":
                st.subheader("🏆 The Best of the Best: Critic & Audience Picks")
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### ⭐ Highest Rated Movies (Critic's Choice)")
                    df_highest_rated = df.sort_values(by=['average_rating', 'total_ratings'], ascending=[False, False]).head(10)
                    fig_highest = px.bar(df_highest_rated, y='movie_title', x='average_rating', orientation='h', title='Top 10 by Average Score', color='average_rating', color_continuous_scale=px.colors.sequential.Cividis_r, labels={'movie_title': 'Movie', 'average_rating': 'Average Rating (out of 5)'})
                    fig_highest.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_highest, use_container_width=True)
                with col2:
                    st.markdown("#### 🔥 Most Popular Movies (People's Choice)")
                    df_most_popular = df.sort_values(by='total_ratings', ascending=False).head(10)
                    fig_most = px.bar(df_most_popular, y='movie_title', x='total_ratings', orientation='h', title='Top 10 by Number of Ratings', color='total_ratings', color_continuous_scale=px.colors.sequential.Plasma, labels={'movie_title': 'Movie', 'total_ratings': 'Number of Ratings'})
                    fig_most.update_layout(yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_most, use_container_width=True)
                st.markdown("---")
                st.markdown("#### 💎 Hidden Gems: Highly Rated, Less Seen")
                median_ratings = df['total_ratings'].median()
                hidden_gems = df[(df['average_rating'] >= 4.0) & (df['total_ratings'] < median_ratings)]
                hidden_gems = hidden_gems.sort_values('average_rating', ascending=False).head(10)
                if not hidden_gems.empty:
                    st.info("These movies have excellent scores but haven't been discovered by as many people. Give them a try!", icon="💡")
                    display_styled_dataframe(hidden_gems, 'cividis', ['average_rating', 'total_ratings'], formatter={'average_rating': '{:.2f}'})
                else:
                    st.warning("No 'Hidden Gems' found based on the current criteria.")

            elif selection == "User Engagement":
                st.subheader("🔥 Power Users & Community Engagement")
                st.markdown("#### 📊 User Activity Segments")
                bins = [0, 50, 200, 500, float('inf')]
                labels = ['Casual Fans (1-50)', 'Active Critics (51-200)', 'Super Fans (201-500)', 'Hall of Famers (501+)']
                df['user_category'] = pd.cut(df['number_of_ratings'], bins=bins, labels=labels, right=True)
                category_counts = df['user_category'].value_counts().reset_index()
                category_counts.columns = ['category', 'count']
                fig_bar = px.bar(category_counts, x='category', y='count', title='Number of Users by Engagement Level', labels={'category': 'User Segment', 'count': 'Number of Users'}, color='category', color_discrete_sequence=px.colors.sequential.Plasma_r)
                fig_bar.update_layout(xaxis={'categoryorder':'array', 'categoryarray': labels})
                st.plotly_chart(fig_bar, use_container_width=True)
                st.markdown("#### 🏆 Top 20 Most Active Users")
                display_styled_dataframe(df.head(20), 'plasma', ['number_of_ratings'])

            elif selection == "Rating Trends":
                st.subheader("📈 A Journey Through Time: Rating Trends")
                df = df.sort_values('rating_year')
                fig = px.area(df, x='rating_year', y='ratings_given', title='Total Ratings Submitted Per Year', markers=True)
                fig.update_layout(xaxis_title='Year', yaxis_title='Number of Ratings')
                st.plotly_chart(fig, use_container_width=True)

            elif selection == "Tag Analysis":
                st.subheader("🏷️ The DNA of Movies: Tag Relevance")
                st.markdown("#### ✨ Top 20 Most Relevant Tags")
                df_top20 = df.head(20)
                fig = px.bar(df_top20, x='avg_relevance', y='tag_name', orientation='h', title='Most Relevant Tags According to Users', color='avg_relevance', color_continuous_scale=px.colors.sequential.Magma)
                fig.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title='Average Relevance Score')
                st.plotly_chart(fig, use_container_width=True)

# 📌 Footer
st.divider()
st.markdown("<center><small>© 2025 MovieLens Analytics | Built with ❤️ using Streamlit & Snowflake</small></center>", unsafe_allow_html=True)