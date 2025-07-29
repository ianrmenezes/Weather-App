import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import streamlit.components.v1 as components
import json
import time
import math # Added for math.cos and math.sin in display_weather_map

# Load environment variables
load_dotenv()

# Page configuration with enhanced styling
st.set_page_config(
    page_title="🌤️ Weather App",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Modern CSS Reset and Base Styles */
    * {
        box-sizing: border-box;
    }
    
    /* Enhanced Space Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 25%, #24243e 50%, #302b63 75%, #0f0c29 100%);
        min-height: 100vh;
    }
    
    /* Animated Star Background */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(2px 2px at 20px 30px, #fff, transparent),
            radial-gradient(2px 2px at 40px 70px, #fff, transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, #fff, transparent),
            radial-gradient(2px 2px at 160px 30px, #fff, transparent),
            radial-gradient(1px 1px at 200px 60px, #fff, transparent),
            radial-gradient(2px 2px at 240px 20px, #fff, transparent),
            radial-gradient(1px 1px at 280px 50px, #fff, transparent),
            radial-gradient(2px 2px at 320px 80px, #fff, transparent);
        background-repeat: repeat;
        background-size: 350px 100px;
        opacity: 0.4;
        animation: twinkle 4s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: 0;
    }
    
    @keyframes twinkle {
        0% { opacity: 0.3; }
        100% { opacity: 0.6; }
    }
    
    /* Modern Header Design */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem 1.5rem 1.5rem 1.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        z-index: 10;
        backdrop-filter: blur(10px);
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
        z-index: -1;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.7; transform: scale(1.1); }
    }
    
    /* Enhanced City Input Card */
    .city-input-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 25px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 400px;
        color: white;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        z-index: 10;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .city-input-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
    }
    
    /* Modern Weather Cards */
    .weather-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
        transition: all 0.3s ease;
    }
    
    .weather-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    
    /* Enhanced Metric Cards */
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 0.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        position: relative;
        z-index: 10;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        background: rgba(255,255,255,0.15);
        box-shadow: 0 12px 30px rgba(0,0,0,0.2);
    }
    
    /* Modern Forecast Cards */
    .forecast-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        z-index: 10;
        transition: all 0.3s ease;
    }
    
    .forecast-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    }
    
    /* Enhanced Climate Summary */
    .climate-summary {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        color: white;
        height: 100%;
        backdrop-filter: blur(10px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        position: relative;
        z-index: 10;
        transition: all 0.3s ease;
    }
    
    .climate-summary:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    }
    
    /* Modern Feature Highlights */
    .feature-highlight {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.5rem 0;
        border-left: 5px solid #FF8C00;
        color: black;
        height: 100%;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        z-index: 10;
        transition: all 0.3s ease;
    }
    
    .feature-highlight:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.25);
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 1rem 2rem;
        font-weight: bold;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        font-size: 1rem;
        position: relative;
        z-index: 10;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #5a6fd8 0%, #6a5acd 100%);
    }
    
    /* Modern Input Styling */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 15px;
        color: white;
        padding: 1rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
        background: rgba(255,255,255,0.15);
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7);
    }
    
    /* Enhanced Charts and Maps */
    .chart-container {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    }
    
    .map-container {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
        transition: all 0.3s ease;
    }
    
    .map-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    }
    
    /* Modern Tab Styling */
    div[data-testid="stRadio"] label {
        background: rgba(255,255,255,0.1);
        color: #fff;
        border: none;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        cursor: pointer;
        margin-right: 1rem;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(102,126,234,0.15);
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stRadio"] label[data-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        font-weight: bold;
        box-shadow: 0 12px 35px rgba(102,126,234,0.3);
        transform: translateY(-2px);
    }
    
    div[data-testid="stRadio"] label:hover {
        background: rgba(102,126,234,0.2);
        color: #fff;
        transform: translateY(-1px);
    }
    
    /* Enhanced Weather News */
    .news-card {
        background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2);
        color: white;
        position: relative;
        z-index: 10;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .news-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
    }
    
    .news-item {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }
    
    .news-item:hover {
        background: rgba(255,255,255,0.15);
        transform: translateY(-2px);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 1.5rem 1rem;
            margin-bottom: 1.5rem;
        }
        
        .city-input-card {
            margin: 1.5rem auto;
            padding: 1.5rem;
        }
        
        .weather-card {
            padding: 1.5rem;
        }
        
        .metric-card {
            padding: 1rem;
            margin: 0.3rem;
        }
        
        div[data-testid="stRadio"] label {
            padding: 0.8rem 1.5rem;
            font-size: 1rem;
            margin-right: 0.5rem;
        }
    }
    
    /* Smooth Animations */
    .fade-in {
        animation: fadeIn 0.8s ease-out;
    }
    
    @keyframes fadeIn {
        from { 
            opacity: 0; 
            transform: translateY(30px); 
        }
        to { 
            opacity: 1; 
            transform: translateY(0); 
        }
    }
    
    /* Enhanced Typography */
    h1, h2, h3, h4, h5, h6 {
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Modern Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a5acd 100%);
    }
    
    /* Ensure all content is visible */
    .main .block-container {
        position: relative;
        z-index: 10;
    }
    
    .stMarkdown, .stButton, .stTextInput, .stRadio {
        position: relative;
        z-index: 10;
    }
</style>
""", unsafe_allow_html=True)

# --- Inject JavaScript to forcibly hide the tab indicator ---
components.html('''
<script>
window.addEventListener('DOMContentLoaded', function() {
  function hideTabIndicator() {
    // Find all tablists
    document.querySelectorAll('[data-testid="stTabs"] [role="tablist"]').forEach(tablist => {
      // Hide any direct child div with a red border or background
      Array.from(tablist.children).forEach(child => {
        const style = window.getComputedStyle(child);
        if (
          style.borderTopColor === 'rgb(255, 0, 0)' ||
          style.backgroundColor === 'rgb(255, 0, 0)' ||
          style.borderTop.includes('red') ||
          style.borderTop.includes('#f00')
        ) {
          child.style.display = 'none';
        }
        // Also hide if it has a borderTopWidth > 0 and is not a tab button
        if (
          parseInt(style.borderTopWidth) > 0 &&
          !child.getAttribute('role')
        ) {
          child.style.display = 'none';
        }
      });
    });
  }
  hideTabIndicator();
  // Also run again after a short delay in case of rerender
  setTimeout(hideTabIndicator, 1000);
});
</script>
''', height=0)

# API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Weather News Configuration
WEATHER_NEWS_CACHE_DURATION = 3600  # 1 hour in seconds
WEATHER_NEWS_CACHE_KEY = "weather_news_cache"

def get_weather_news():
    """Fetch weather news from multiple sources with caching"""
    current_time = time.time()
    
    # Check if force refresh is requested
    force_refresh = st.session_state.get("force_news_refresh", False)
    
    # Check if we have cached news and it's still fresh (unless force refresh is requested)
    if not force_refresh and WEATHER_NEWS_CACHE_KEY in st.session_state:
        cached_data = st.session_state[WEATHER_NEWS_CACHE_KEY]
        if current_time - cached_data['timestamp'] < WEATHER_NEWS_CACHE_DURATION:
            return cached_data['news']
    
    # Clear the force refresh flag
    if force_refresh:
        st.session_state["force_news_refresh"] = False
        st.session_state["weather_news_displayed"] = True
    
    # Try to fetch real weather news from NewsAPI (if API key is available)
    news_api_key = os.getenv("NEWS_API_KEY")
    
    if news_api_key:
        try:
            # Fetch weather-related news from NewsAPI (more specific query)
            news_url = "https://newsapi.org/v2/everything"
            params = {
                'q': '"weather forecast" OR "severe weather" OR "climate change" OR "storm warning" OR flooding OR hurricane OR tornado OR wildfire OR heatwave OR blizzard OR "extreme weather" OR "weather alert" -entertainment -health -sports -finance',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 20,
                'apiKey': news_api_key
            }
            
            response = requests.get(news_url, params=params, timeout=10)
            if response.status_code == 200:
                news_data = response.json()
                articles = news_data.get('articles', [])
                
                # Filter out unrelated articles by checking for weather keywords in title/description
                keywords = [
                    'weather', 'forecast', 'storm', 'hurricane', 'tornado', 'flood', 'wildfire', 'heatwave', 'blizzard', 'climate', 'rain', 'snow', 'drought', 'typhoon', 'cyclone', 'lightning', 'thunder', 'wind', 'temperature', 'cold', 'hot', 'heat', 'freezing', 'frost', 'hail', 'meteorological', 'atmosphere', 'precipitation', 'severe weather', 'storm warning', 'flooding', 'extreme', 'alert', 'warning'
                ]
                filtered_articles = []
                for article in articles:
                    title = article.get('title', '') or ''
                    description = article.get('description', '') or ''
                    text = (title + ' ' + description).lower()
                    if any(kw in text for kw in keywords):
                        filtered_articles.append(article)
                
                # If we don't have enough filtered articles, use all articles (they should be weather-related from the query)
                if len(filtered_articles) < 3:
                    filtered_articles = articles[:10]  # Take first 10 articles
                
                if filtered_articles:
                    weather_news = []
                    for article in filtered_articles[:3]:  # Get top 3 filtered articles
                        # Use description instead of content since content is truncated by NewsAPI
                        content = article.get('content', '') or ''
                        description = article.get('description', '') or ''
                        
                        # If content is truncated, use description instead
                        if content and '[+' in content:
                            display_content = description
                        else:
                            display_content = content if content else description
                        
                        weather_news.append({
                            'title': article.get('title', 'Weather Update') or 'Weather Update',
                            'description': article.get('description', 'Weather-related news') or 'Weather-related news',
                            'content': display_content or 'No content available',
                            'url': article.get('url', '#') or '#',
                            'source': article.get('source', {}).get('name', 'News Source') or 'News Source',
                            'published_at': article.get('publishedAt', '') or '',
                            'icon': get_weather_news_icon(article.get('title', '') or '')
                        })
                    
                    # Cache the news
                    st.session_state[WEATHER_NEWS_CACHE_KEY] = {
                        'news': weather_news,
                        'timestamp': current_time
                    }
                    
                    return weather_news
            else:
                st.warning(f"⚠️ NewsAPI returned status code: {response.status_code}")
        except Exception as e:
            st.warning(f"Could not fetch real-time weather news: {str(e)}")
    
    # Fallback to curated weather news if API fails or no key
    if not news_api_key:
        # Show info about NewsAPI key (only once per session)
        if "news_api_info_shown" not in st.session_state:
            st.info("💡 Want real-time weather news? Get a free NewsAPI key from newsapi.org and add it as NEWS_API_KEY in your environment variables!")
            st.session_state["news_api_info_shown"] = True
    
    # Always return fallback news if API fails or no key
    fallback_news = get_fallback_weather_news()
    
    # Cache the fallback news
    st.session_state[WEATHER_NEWS_CACHE_KEY] = {
        'news': fallback_news,
        'timestamp': current_time
    }
    
    return fallback_news

def get_weather_news_icon(title):
    """Get appropriate weather icon based on news title"""
    if not title:
        return '🌤️'
    
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['tornado', 'cyclone', 'hurricane']):
        return '🌪️'
    elif any(word in title_lower for word in ['flood', 'rain', 'monsoon']):
        return '🌧️'
    elif any(word in title_lower for word in ['fire', 'wildfire', 'blaze']):
        return '🔥'
    elif any(word in title_lower for word in ['snow', 'blizzard', 'winter']):
        return '❄️'
    elif any(word in title_lower for word in ['heat', 'drought', 'hot']):
        return '🌡️'
    elif any(word in title_lower for word in ['storm', 'thunder']):
        return '⛈️'
    else:
        return '🌤️'

def get_fallback_weather_news():
    """Provide curated fallback weather news when API is unavailable"""
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    return [
        {
            'title': 'Global Climate Patterns Shift',
            'description': 'Scientists observe unusual weather patterns across multiple continents',
            'content': 'Recent climate data shows significant shifts in global weather patterns, affecting regions from the Arctic to the tropics. Researchers are monitoring these changes closely and studying their potential impact on global weather systems.',
            'url': 'https://www.climate.gov/news-features',
            'source': 'Climate.gov',
            'published_at': current_date,
            'icon': '🌍'
        },
        {
            'title': 'Extreme Weather Events Increase',
            'description': 'Frequency of severe storms and natural disasters rises globally',
            'content': 'Meteorologists report an increase in extreme weather events worldwide, including hurricanes, floods, and heatwaves affecting millions of people. Climate scientists are analyzing the correlation between rising global temperatures and weather intensity.',
            'url': 'https://www.wmo.int/news',
            'source': 'World Meteorological Organization',
            'published_at': current_date,
            'icon': '⛈️'
        },
        {
            'title': 'Renewable Energy Weather Impact',
            'description': 'Weather conditions significantly affect renewable energy production',
            'content': 'Solar and wind energy production varies dramatically with weather conditions, highlighting the importance of accurate weather forecasting for energy planning. Advanced weather prediction models are helping optimize renewable energy grid management.',
            'url': 'https://www.energy.gov/weather',
            'source': 'Department of Energy',
            'published_at': current_date,
            'icon': '☀️'
        }
    ]

def display_weather_news():
    """Display the entire Global Weather News section with guaranteed content"""
    
    # Always get fresh weather news
    weather_news = get_weather_news()
    
    # Ensure we always have news to display
    if not weather_news or not isinstance(weather_news, list) or len(weather_news) == 0:
        weather_news = get_fallback_weather_news()

    # Calculate time since last update
    if WEATHER_NEWS_CACHE_KEY in st.session_state:
        last_update = st.session_state[WEATHER_NEWS_CACHE_KEY]['timestamp']
        time_since_update = time.time() - last_update
        minutes_since_update = int(time_since_update // 60)
    else:
        minutes_since_update = 0

    # Create the news container
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem auto;
        max-width: 700px;
        color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; gap: 0.8rem;">
                <span style="font-size: 1.5rem;">🌍</span>
                <h2 style="margin: 0; font-size: 1.2rem; font-weight: bold;">Global Weather News</h2>
            </div>
            <div style="
                background: rgba(255,255,255,0.1);
                padding: 0.4rem 0.8rem;
                border-radius: 8px;
                font-size: 0.8rem;
            ">
                {f"Updated {minutes_since_update} min ago" if minutes_since_update > 0 else "Just updated"}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Display each news article
    for i, news in enumerate(weather_news):
        # Ensure all fields have default values
        title = news.get('title', 'Weather Update')
        description = news.get('description', 'Weather-related news')
        content = news.get('content', 'Weather information and updates')
        url = news.get('url', '#')
        source = news.get('source', 'Weather Source')
        
        # Format date
        try:
            published_at = news.get('published_at')
            if published_at and published_at != '':
                pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                formatted_date = pub_date.strftime('%b %d, %Y')
            else:
                formatted_date = "Recent"
        except:
            formatted_date = "Recent"
        
        # Display the news article
        st.markdown(f"""
        <div style="
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <span style="font-size: 2rem;">📰</span>
                <div style="flex: 1;">
                    <h3 style="
                        font-weight: bold;
                        color: #fff;
                        font-size: 1.2rem;
                        margin-bottom: 0.5rem;
                    ">{title}</h3>
                    <p style="
                        color: #fff;
                        font-size: 1rem;
                        margin-bottom: 0.5rem;
                        opacity: 0.9;
                    ">{description}</p>
                    <p style="
                        color: #e0e0e0;
                        font-size: 0.9rem;
                        margin-bottom: 0.5rem;
                        line-height: 1.4;
                    ">{content}</p>
                    <div style="
                        color: #d0f0ff;
                        font-size: 0.9rem;
                        margin-bottom: 0.5rem;
                    ">
                        Source: <a href='{url}' target='_blank' style='color:#fff; text-decoration:underline;'>{source}</a> • {formatted_date}
                    </div>
                    <a href='{url}' target='_blank' style='
                        background: rgba(255,255,255,0.2);
                        color: #fff;
                        padding: 0.5rem 1rem;
                        border-radius: 8px;
                        text-decoration: none;
                        font-size: 0.9rem;
                        border: 1px solid rgba(255,255,255,0.3);
                        display: inline-block;
                    '>📖 Read Full Article</a>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

def get_weather_data(city, api_key):
    """Get current weather data for a city"""
    url = f"{BASE_URL}/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

def get_forecast_data(city, api_key):
    """Get 5-day forecast data for a city"""
    url = f"{BASE_URL}/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching forecast data: {str(e)}")
        return None

def get_weather_icon(weather_code):
    """Get weather icon based on weather code"""
    icons = {
        '01': '☀️',  # clear sky
        '02': '⛅',  # few clouds
        '03': '☁️',  # scattered clouds
        '04': '☁️',  # broken clouds
        '09': '🌧️',  # shower rain
        '10': '🌦️',  # rain
        '11': '⛈️',  # thunderstorm
        '13': '🌨️',  # snow
        '50': '🌫️',  # mist
    }
    return icons.get(weather_code[:2], '🌤️')

def get_weather_color(temp):
    """Get color based on temperature"""
    if temp < 0:
        return '#87CEEB'  # Light blue for cold
    elif temp < 15:
        return '#98FB98'  # Light green for cool
    elif temp < 25:
        return '#FFD700'  # Gold for warm
    else:
        return '#FF6347'  # Tomato for hot

def get_climate_summary(city, temp, weather_desc):
    """Generate climate summary based on current conditions"""
    if temp < 0:
        climate = "Cold winter conditions"
        season = "Winter"
    elif temp < 15:
        climate = "Cool spring/autumn weather"
        season = "Spring/Autumn"
    elif temp < 25:
        climate = "Pleasant warm weather"
        season = "Spring/Summer"
    else:
        climate = "Hot summer conditions"
        season = "Summer"
    
    return {
        'climate': climate,
        'season': season,
        'description': f"{city} experiences {climate.lower()} with {weather_desc.lower()} conditions."
    }

def display_current_weather(weather_data, city):
    """Display current weather information with enhanced UI in center"""
    if not weather_data:
        return
    
    # Main weather card in center
    temp = weather_data['main']['temp']
    weather_icon = get_weather_icon(weather_data['weather'][0]['icon'])
    weather_desc = weather_data['weather'][0]['description'].title()
    
    # Center the main weather display with smaller, cooler design
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col2:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 1.8rem;
            margin: 1rem auto;
            max-width: 350px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        ">
            <div style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                gap: 0.8rem;
            ">
                <div style="
                    font-size: 3.5rem;
                    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
                    margin-bottom: 0.5rem;
                ">{weather_icon}</div>
                <div style="
                    font-size: 2.5rem;
                    font-weight: 800;
                    color: #fff;
                    text-shadow: 0 3px 6px rgba(0,0,0,0.3);
                    margin-bottom: 0.5rem;
                    letter-spacing: 1px;
                ">{temp:.1f}°C</div>
                <div style="
                    font-size: 1.1rem;
                    font-weight: 600;
                    color: #fff;
                    opacity: 0.95;
                    margin-bottom: 0.5rem;
                    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
                ">{weather_desc}</div>
                <div style="
                    font-size: 0.9rem;
                    color: #fff;
                    opacity: 0.8;
                    text-transform: uppercase;
                    letter-spacing: 2px;
                    font-weight: 500;
                    background: rgba(255,255,255,0.1);
                    padding: 0.4rem 1rem;
                    border-radius: 15px;
                    border: 1px solid rgba(255,255,255,0.2);
                ">{city}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Weather metrics in a grid below
    st.markdown("### 🌡️ Weather Details")
    
    # First row of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">🌡️ Feels Like</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{weather_data['main']['feels_like']:.1f}°C</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">💧 Humidity</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{weather_data['main']['humidity']}%</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">💨 Wind</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{weather_data['wind']['speed']} m/s</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">☁️ Cloud Cover</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{weather_data['clouds']['all']}%</h5>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">🌧️ Precipitation</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{weather_data.get('rain', {}).get('1h', 0)} mm</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">📊 Pressure</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{weather_data['main']['pressure']} hPa</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">👁️ Visibility</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{weather_data['visibility']/1000:.1f} km</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # UV Index (simulated since free API doesn't include it)
        if temp > 25:
            uv_index = "High (8-10)"
        elif temp > 20:
            uv_index = "Moderate (5-7)"
        elif temp > 10:
            uv_index = "Low (3-4)"
        else:
            uv_index = "Very Low (1-2)"
        st.markdown(f"""
        <div class="metric-card fade-in">
            <h6 style="margin-bottom: 0.5rem;">☀️ UV Index</h6>
            <h5 style="margin: 0; font-size: 1.5rem;">{uv_index}</h5>
        </div>
        """, unsafe_allow_html=True)
    
    # Climate overview and sunrise/sunset side by side
    st.markdown("### 🌍 Climate Overview")
    climate_info = get_climate_summary(city, temp, weather_desc)
    timezone_offset = weather_data.get('timezone', 0)  # in seconds
    sunrise = datetime.utcfromtimestamp(weather_data['sys']['sunrise'] + timezone_offset)
    sunset = datetime.utcfromtimestamp(weather_data['sys']['sunset'] + timezone_offset)
    
    # Enhanced layout with better spacing
    st.markdown(f"""
    <div style='width: 100%;'>
        <div style="display: flex; gap: 2rem; align-items: stretch; margin-bottom: 1rem;">
            <div style="flex: 2.2; display: flex; flex-direction: column; min-width: 0;">
                <div class="climate-summary fade-in">
                    <h6 style="margin-bottom: 1rem; font-size: 1.2rem;">🌤️ Weather Overview</h6>
                    <p style="font-size: 1rem; margin-bottom: 0.5rem;"><strong>Current Season:</strong> {climate_info['season']}</p>
                    <p style="font-size: 1rem; margin-bottom: 0.5rem;"><strong>Climate Type:</strong> {climate_info['climate']}</p>
                    <p style="font-size: 1rem; margin-bottom: 0.5rem;"><strong>Description:</strong> {climate_info['description']}</p>
                    <p style="font-size: 1rem; margin-bottom: 0.5rem;"><strong>Hottest Month:</strong> July (typically 25-30°C)</p>
                    <p style="font-size: 1rem; margin-bottom: 0;"><strong>Coldest Month:</strong> January (typically 0-5°C)</p>
                </div>
            </div>
            <div style="flex: 1; display: flex; flex-direction: column; gap: 1rem; min-width: 0;">
                <div class="feature-highlight fade-in" style="padding: 1.5rem; min-height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <div style="font-size: 1.3rem; font-weight: 600; color: black; margin-bottom: 0.5rem; text-align: center;">🌅 Sunrise</div>
                    <div style="font-size: 2.5rem; font-weight: 400; color: #222; text-shadow: 0 1px 6px rgba(0,0,0,0.08); letter-spacing: 1px; text-align: center;">{sunrise.strftime('%H:%M')}</div>
                </div>
                <div class="feature-highlight fade-in" style="padding: 1.5rem; min-height: 100px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <div style="font-size: 1.3rem; font-weight: 600; color: black; margin-bottom: 0.5rem; text-align: center;">🌇 Sunset</div>
                    <div style="font-size: 2.5rem; font-weight: 400; color: #222; text-shadow: 0 1px 6px rgba(0,0,0,0.08); letter-spacing: 1px; text-align: center;">{sunset.strftime('%H:%M')}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_forecast(forecast_data, weather_data=None):
    """Display 5-day weather forecast with enhanced charts"""
    if not forecast_data:
        st.warning("⚠️ No forecast data available. Please try again.")
        return
    
    try:
        # Get timezone offset from weather_data if available
        timezone_offset = 0
        if weather_data and 'timezone' in weather_data:
            timezone_offset = weather_data['timezone']
        elif 'city' in forecast_data and 'timezone' in forecast_data['city']:
            timezone_offset = forecast_data['city']['timezone']
        
        # Process forecast data
        forecast_list = forecast_data.get('list', [])
        if not forecast_list:
            st.warning("⚠️ No forecast data available. Please try again.")
            return
            
        daily_data = []
        
        for item in forecast_list:
            try:
                date = datetime.utcfromtimestamp(item['dt'] + timezone_offset)
                temp = item['main']['temp']
                humidity = item['main']['humidity']
                weather_desc = item['weather'][0]['description']
                weather_icon = get_weather_icon(item['weather'][0]['icon'])
                
                daily_data.append({
                    'Date': date.strftime('%Y-%m-%d'),
                    'Time': date.strftime('%H:%M'),
                    'Temperature (°C)': temp,
                    'Humidity (%)': humidity,
                    'Weather': weather_desc,
                    'Icon': weather_icon,
                    'Color': get_weather_color(temp)
                })
            except (KeyError, TypeError) as e:
                continue  # Skip invalid data points
        
        if not daily_data:
            st.warning("⚠️ No valid forecast data available. Please try again.")
            return
            
        df = pd.DataFrame(daily_data)
        
        # Simple temperature chart without problematic HTML
        fig_temp = go.Figure()
        
        fig_temp.add_trace(go.Scatter(
            x=df['Time'],
            y=df['Temperature (°C)'],
            mode='lines+markers',
            name='Temperature',
            line=dict(
                color='#667eea',
                width=4,
                shape='spline'
            ),
            marker=dict(
                size=10, 
                color=df['Color'],
                line=dict(color='white', width=2),
                symbol='circle'
            ),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig_temp.update_layout(
            title='🌡️ Temperature Forecast',
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            template='plotly_white',
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Simple color explanation using Streamlit components
        st.markdown("**🌡️ Temperature Colors:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("🔵 **Cold** (< 0°C)")
        with col2:
            st.markdown("🟢 **Cool** (0-15°C)")
        with col3:
            st.markdown("🟡 **Warm** (15-25°C)")
        with col4:
            st.markdown("🔴 **Hot** (> 25°C)")
        
        # Simple humidity chart
        fig_humidity = go.Figure()
        
        fig_humidity.add_trace(go.Bar(
            x=df['Time'],
            y=df['Humidity (%)'],
            name='Humidity',
            marker_color='#764ba2',
            opacity=0.8
        ))
        
        fig_humidity.update_layout(
            title='💧 Humidity Forecast',
            xaxis_title="Time",
            yaxis_title="Humidity (%)",
            template='plotly_white',
            height=350,
            showlegend=False
        )
        
        st.plotly_chart(fig_humidity, use_container_width=True)
        
        # Daily summary cards
        st.subheader("📅 Daily Forecast Summary")
        
        # Group by date and calculate summaries
        daily_summary = df.groupby('Date').agg({
            'Temperature (°C)': ['min', 'max', 'mean'],
            'Humidity (%)': 'mean',
            'Weather': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
            'Icon': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
        }).round(1)
        
        # Flatten column names
        daily_summary.columns = ['Min Temp', 'Max Temp', 'Avg Temp', 'Avg Humidity', 'Weather', 'Icon']
        daily_summary = daily_summary.reset_index()
        
        # Display daily summary in cards
        for _, row in daily_summary.iterrows():
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
                border-radius: 15px;
                padding: 1.2rem;
                margin: 1rem 0;
                border: 1px solid rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: #fff; margin-bottom: 0.3rem;">
                            {row['Date']}
                        </div>
                        <div style="font-size: 0.95rem; color: #e0e0e0;">
                            {row['Icon']} {row['Weather']}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 1rem; font-weight: 600; color: #fff; margin-bottom: 0.2rem;">
                            {row['Min Temp']}°C / {row['Max Temp']}°C
                        </div>
                        <div style="font-size: 0.9rem; color: #d0f0ff;">
                            Avg: {row['Avg Temp']}°C | 💧 {row['Avg Humidity']}%
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"❌ Error displaying forecast: {str(e)}")
        st.info("Please try refreshing the page or checking your internet connection.")

def display_weather_map(weather_data, forecast_data):
    """Display interactive weather map with simple, clean, and fantastic design"""
    if not weather_data:
        return
    
    # Create a map centered on the city with clean styling
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    timezone_offset = weather_data.get('timezone', 0)
    
    # Create map with clean tile layer
    m = folium.Map(
        location=[lat, lon], 
        zoom_start=11,
        tiles='CartoDB positron',
        control_scale=True
    )
    
    # Add current weather marker with simple popup
    current_temp = weather_data['main']['temp']
    current_desc = weather_data['weather'][0]['description']
    current_icon = get_weather_icon(weather_data['weather'][0]['icon'])
    
    # Simple, clean popup for current weather
    current_popup_html = f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.5rem;
        color: white;
        font-family: 'Segoe UI', sans-serif;
        min-width: 200px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    ">
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{current_icon}</div>
            <h3 style="margin: 0; font-size: 1.1rem; font-weight: bold;">Current Weather</h3>
            <div style="
                background: rgba(255,255,255,0.1);
                border-radius: 8px;
                padding: 0.8rem;
                margin-top: 0.8rem;
            ">
                <p style="margin: 0.3rem 0; font-size: 1rem;"><strong>{current_temp}°C</strong></p>
                <p style="margin: 0.3rem 0; font-size: 0.9rem;">{current_desc.title()}</p>
            </div>
        </div>
    </div>
    """
    
    # Add current weather marker
    folium.Marker(
        [lat, lon],
        popup=folium.Popup(current_popup_html, max_width=250),
        tooltip=f"📍 {current_temp}°C - {current_desc.title()}",
        icon=folium.Icon(color='red', icon='info-sign', prefix='fa')
    ).add_to(m)
    
    # Add forecast markers if available
    if forecast_data and 'list' in forecast_data:
        forecast_list = forecast_data['list']
        
        # Simple circle around the city
        folium.Circle(
            location=[lat, lon],
            radius=3000,
            color='#667eea',
            fill=True,
            fill_color='#667eea',
            fill_opacity=0.1,
            weight=2,
            opacity=0.6
        ).add_to(m)
        
        # Add forecast markers in a simple pattern
        for i, item in enumerate(forecast_list[:4]):  # Show first 4 forecasts
            angle = (i * 90) * (3.14159 / 180)  # 90 degrees apart
            radius = 0.015
            forecast_lat = lat + (radius * math.cos(angle))
            forecast_lon = lon + (radius * math.sin(angle))
            
            forecast_temp = item['main']['temp']
            forecast_desc = item['weather'][0]['description']
            forecast_icon = get_weather_icon(item['weather'][0]['icon'])
            forecast_time = datetime.utcfromtimestamp(item['dt'] + timezone_offset).strftime('%H:%M')
            
            # Simple forecast popup
            forecast_popup_html = f"""
            <div style="
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                border-radius: 12px;
                padding: 1.5rem;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                min-width: 180px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.2);
            ">
                <div style="text-align: center;">
                    <div style="font-size: 2rem; margin-bottom: 0.5rem;">{forecast_icon}</div>
                    <h4 style="margin: 0; font-size: 1rem; font-weight: bold;">Forecast</h4>
                    <div style="
                        background: rgba(255,255,255,0.1);
                        border-radius: 8px;
                        padding: 0.8rem;
                        margin-top: 0.8rem;
                    ">
                        <p style="margin: 0.3rem 0; font-size: 1rem;"><strong>{forecast_time}</strong></p>
                        <p style="margin: 0.3rem 0; font-size: 0.9rem;"><strong>{forecast_temp}°C</strong></p>
                        <p style="margin: 0.3rem 0; font-size: 0.8rem;">{forecast_desc.title()}</p>
                    </div>
                </div>
            </div>
            """
            
            folium.Marker(
                [forecast_lat, forecast_lon],
                popup=folium.Popup(forecast_popup_html, max_width=220),
                tooltip=f"⏰ {forecast_time}: {forecast_temp}°C",
                icon=folium.Icon(color='blue', icon='cloud', prefix='fa')
            ).add_to(m)
    
    # Map container with title inside
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 1.2rem;
        margin: 1rem 0;
        max-width: 650px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    ">
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.8rem;
            margin-bottom: 1rem;
            margin-left: -1cm;
            text-align: center;
        ">
            <span style="font-size: 1.5rem; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));">🗺️</span>
            <h2 style="margin: 0; font-size: 1.3rem; font-weight: bold; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">Weather Map</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Display the map with proper sizing
    folium_static(m, width=650, height=400)
    
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Modern header with enhanced styling
    st.markdown("""
    <div class="main-header fade-in">
        <div style="max-width: 320px; margin: 0 auto; padding-left: 0.5rem;">
            <h1 style="margin: 0; font-size: 2rem; font-weight: bold; text-align: left;">🌤️ Weather App</h1>
        </div>
        <div style="padding-left: 6in; white-space: nowrap; font-size: 1.1rem; margin: 0; text-align: left; opacity: 0.9;">
            Get real-time weather conditions and forecasts for any city around the world!
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Cool floating input design
    st.markdown("""
    <div style="
        text-align: center;
        margin: 2rem auto;
        max-width: 500px;
        position: relative;
    ">
        <div style="
            display: inline-flex;
            align-items: center;
            gap: 0.8rem;
            background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 50px;
            padding: 0.8rem 1.5rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
            margin-bottom: 1rem;
        ">
            <span style="
                font-size: 1.3rem;
                filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
            ">🌍</span>
            <span style="
                font-size: 1.1rem;
                font-weight: 600;
                color: #fff;
                text-shadow: 0 1px 2px rgba(0,0,0,0.3);
            ">Enter City</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Custom styled text input
    st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.1) !important;
        border: 2px solid rgba(255,255,255,0.3) !important;
        border-radius: 25px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 1rem 1.5rem !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(255,255,255,0.6) !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.3) !important;
        transform: translateY(-2px) !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(255,255,255,0.7) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    city = st.text_input("City name:", value="London", key="city_input", label_visibility="collapsed", placeholder="Enter city name...")

    # Weather display logic in main area
    if "weather_data" not in st.session_state:
        st.session_state["weather_data"] = None
    if "forecast_data" not in st.session_state:
        st.session_state["forecast_data"] = None

    if st.button("🌤️ Get Weather", type="primary", use_container_width=True):
        if not API_KEY or API_KEY == "your_api_key_here":
            st.error("⚠️ Please set your OpenWeather API key in the .env file!")
            st.info("Get your free API key from: https://openweathermap.org/api")
            return
        
        # Check if city input is empty or just whitespace
        if not city or not city.strip():
            st.warning("⚠️ Please enter a valid city!")
            return
            
        # Get weather data with loading animation
        with st.spinner("🌤️ Fetching weather data..."):
            weather_data = get_weather_data(city, API_KEY)
            forecast_data = get_forecast_data(city, API_KEY)
        if weather_data:
            st.session_state["weather_data"] = weather_data
            st.session_state["forecast_data"] = forecast_data
        else:
            st.session_state["weather_data"] = None
            st.session_state["forecast_data"] = None
            st.error("❌ Could not fetch weather data. Please check the city name and try again.")

    # Always render the tab bar and content if weather data exists
    if st.session_state["weather_data"]:
        tab_options = ["🌡️ Current Weather", "📅 5-Day Forecast", "🗺️ Weather Map"]
        selected_tab = st.radio(
            "",
            tab_options,
            horizontal=True,
            key="custom_tabs_radio",
            label_visibility="collapsed"
        )
        if selected_tab == "🌡️ Current Weather":
            display_current_weather(st.session_state["weather_data"], city)
        elif selected_tab == "📅 5-Day Forecast":
            st.header(f"📅 5-Day Forecast for {city}")
            display_forecast(st.session_state["forecast_data"], st.session_state["weather_data"])
        elif selected_tab == "🗺️ Weather Map":
            display_weather_map(st.session_state["weather_data"], st.session_state["forecast_data"])

    # Enhanced refresh button
    st.markdown("""
    <style>
    .refresh-button {
        background: rgba(255,255,255,0.1) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.5rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        margin: 1rem 0 !important;
        backdrop-filter: blur(10px) !important;
    }
    .refresh-button:hover {
        background: rgba(255,255,255,0.2) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Place the button BEFORE the weather news
    if st.button("🔄 Refresh News", key="refresh_news_button", help="Refresh News", type="secondary"):
        # Clear the cache and force refresh
        if WEATHER_NEWS_CACHE_KEY in st.session_state:
            del st.session_state[WEATHER_NEWS_CACHE_KEY]
        
        # Set force refresh flag
        st.session_state["force_news_refresh"] = True
        
        # Clear any previous news display
        if "weather_news_displayed" in st.session_state:
            del st.session_state["weather_news_displayed"]
        
        # Show loading message
        with st.spinner("🔄 Refreshing weather news..."):
            time.sleep(0.5)
            # Actually refresh the news
            weather_news = get_weather_news()
        
        # Show success message
        st.success("✅ Weather news refreshed successfully!")
    
    # Display weather news with guaranteed content
    display_weather_news()

if __name__ == "__main__":
    main() 