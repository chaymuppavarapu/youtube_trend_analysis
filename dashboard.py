import streamlit as st
import pandas as pd
from yt_api_scraper import get_trending_videos
import plotly.express as px
from datetime import datetime
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="YouTube Trends Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("📊 YouTube Trends Dashboard")
st.markdown("Real-time analysis of trending videos on YouTube")

# Sidebar controls
st.sidebar.header("Controls")
region_code = st.sidebar.selectbox(
    "Select Region",
    ["US", "GB", "CA", "AU", "IN", "JP", "KR", "FR", "DE", "BR"],
    format_func=lambda x: {
        "US": "United States", "GB": "United Kingdom", "CA": "Canada",
        "AU": "Australia", "IN": "India", "JP": "Japan", "KR": "South Korea",
        "FR": "France", "DE": "Germany", "BR": "Brazil"
    }[x]
)

video_count = st.sidebar.slider("Number of Videos", 10, 50, 20)

# Fetch data
with st.spinner("Fetching trending videos..."):
    videos = get_trending_videos(max_results=video_count, region_code=region_code)
    if not videos:
        st.error("Failed to fetch videos. Please try again later.")
        st.stop()
    
    # Convert to DataFrame
    df = pd.DataFrame(videos)
    df['published_at'] = pd.to_datetime(df['published_at'])

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

with col1:
    total_views = df['view_count'].sum()
    st.metric("Total Views", f"{total_views:,}")

with col2:
    total_likes = df['like_count'].sum()
    st.metric("Total Likes", f"{total_likes:,}")

with col3:
    total_comments = df['comment_count'].sum()
    st.metric("Total Comments", f"{total_comments:,}")

# Create tabs for different visualizations
tab1, tab2, tab3 = st.tabs(["📈 Trending Videos", "📊 Analytics", "🎥 Video Details"])

with tab1:
    # Bar chart of views by video
    fig = px.bar(
        df.sort_values('view_count', ascending=True).tail(10),
        x='view_count',
        y='title',
        orientation='h',
        title='Top 10 Trending Videos by Views',
        labels={'view_count': 'Views', 'title': 'Video Title'},
        color='view_count',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Engagement ratio (likes/views)
        df['engagement_ratio'] = (df['like_count'] / df['view_count'] * 100).round(2)
        fig = px.scatter(
            df,
            x='view_count',
            y='like_count',
            title='Views vs Likes Correlation',
            labels={'view_count': 'Views', 'like_count': 'Likes'},
            hover_data=['title', 'engagement_ratio'],
            color='engagement_ratio',
            size='comment_count'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Channel analysis
        channel_stats = df.groupby('channel').agg({
            'view_count': 'sum',
            'title': 'count'
        }).reset_index()
        channel_stats.columns = ['channel', 'total_views', 'video_count']
        fig = px.pie(
            channel_stats,
            values='total_views',
            names='channel',
            title='Views Distribution by Channel'
        )
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Detailed video table
    st.subheader("Trending Videos Details")
    
    # Format the DataFrame for display
    display_df = df[['title', 'channel', 'view_count', 'like_count', 'comment_count', 'url']].copy()
    display_df['view_count'] = display_df['view_count'].apply(lambda x: f"{x:,}")
    display_df['like_count'] = display_df['like_count'].apply(lambda x: f"{x:,}")
    display_df['comment_count'] = display_df['comment_count'].apply(lambda x: f"{x:,}")
    
    # Add clickable links
    display_df['url'] = display_df['url'].apply(lambda x: f'<a href="{x}" target="_blank">Watch Video</a>')
    
    # Display the table with clickable links
    st.write(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
