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
    /* Custom tab styling */
    [data-testid="stTabs"] {
        background: transparent;
    }

    [data-testid="stTabs"] > div:first-child {
        background: transparent !important;
        border: none !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    [data-testid="stTabs"] div[role="tablist"] {
        background: transparent !important;
        border: none !important;
        display: flex;
        gap: 8px;
        padding: 0 !important;
        margin-bottom: 16px;
    }

    [data-testid="stTabs"] button[role="tab"] {
        background: rgba(255, 255, 255, 0.1) !important;
        border: none !important;
        border-radius: 8px !important;
        color: rgba(255, 255, 255, 0.7) !important;
        padding: 8px 16px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
        background: rgba(102, 126, 234, 0.6) !important;
        color: white !important;
        font-weight: bold !important;
    }

    [data-testid="stTabs"] button[role="tab"]:hover {
        background: rgba(102, 126, 234, 0.4) !important;
        color: white !important;
    }

    /* Remove all default tab styling */
    [data-testid="stTabs"] *::before,
    [data-testid="stTabs"] *::after {
        display: none !important;
        content: none !important;
        border: none !important;
        background: none !important;
    }

    /* Space background with stars - simplified */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Simple star overlay */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(1px 1px at 20px 30px, #fff, transparent),
            radial-gradient(1px 1px at 40px 70px, #fff, transparent),
            radial-gradient(1px 1px at 90px 40px, #fff, transparent),
            radial-gradient(1px 1px at 130px 80px, #fff, transparent),
            radial-gradient(1px 1px at 160px 30px, #fff, transparent);
        background-repeat: repeat;
        background-size: 200px 100px;
        opacity: 0.6;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Main styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        z-index: 10;
    }
    
    .weather-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0.8rem;
        border-radius: 20px;
        color: white;
        margin: 0.3rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.2);
        text-align: center;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
    }
    
    .metric-card {
        background: rgba(255,255,255,0.1);
        padding: 0.6rem;
        border-radius: 15px;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        margin: 0.2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        position: relative;
        z-index: 10;
    }
    
    .forecast-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 0.6rem;
        border-radius: 15px;
        color: white;
        margin: 0.2rem 0;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        position: relative;
        z-index: 10;
    }
    
    .climate-summary {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 0.8rem;
        border-radius: 15px;
        margin: 0.3rem 0;
        border-left: 5px solid #667eea;
        color: white;
        height: 100%;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        position: relative;
        z-index: 10;
    }
    
    .input-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        width: 200px;
        position: relative;
        z-index: 10;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        font-size: 0.9rem;
        position: relative;
        z-index: 10;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    }
    
    .city-input {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 10px;
        color: white;
        padding: 0.5rem;
        position: relative;
        z-index: 10;
    }
    
    .city-input::placeholder {
        color: rgba(255,255,255,0.7);
    }
    
    .weather-icon-large {
        font-size: 2.5rem;
        text-align: center;
        margin: 0.3rem 0;
    }
    
    .temperature-display {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        margin: 0.3rem 0;
    }
    
    .chart-container {
        background: rgba(255,255,255,0.95);
        padding: 0.8rem;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        margin: 0.3rem 0;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
    }
    
    .map-container {
        background: rgba(255,255,255,0.95);
        padding: 0.8rem;
        border-radius: 15px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        margin: 0.3rem 0;
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
    }
    
    .feature-highlight {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 0.6rem;
        border-radius: 15px;
        margin: 0.3rem 0;
        border-left: 5px solid #FF8C00;
        color: black;
        height: 100%;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        position: relative;
        z-index: 10;
    }
    .sun-time {
        font-size: 2.1rem;
        font-weight: 400;
        color: #222;
        text-shadow: 0 1px 6px rgba(0,0,0,0.08);
        letter-spacing: 1px;
        text-align: center;
        margin-top: 0.1rem;
        margin-bottom: 0.1rem;
    }
    
    .loading-animation {
        text-align: center;
        padding: 0.8rem;
    }
    
    .developer-credit {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        backdrop-filter: blur(10px);
        position: relative;
        z-index: 10;
    }
    
    .sidebar-credit {
        background: rgba(255,255,255,0.1);
        padding: 1.2rem 1rem;
        border-radius: 10px;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        word-wrap: break-word;
        box-sizing: border-box;
        margin-top: 1rem;
        width: 100%;
        max-width: none;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        position: relative;
        z-index: 10;
    }
    
    /* Custom animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .weather-card {
            padding: 0.8rem;
        }
        .temperature-display {
            font-size: 2rem;
        }
    }
    
    /* Make sidebar smaller */
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
        width: 200px;
        position: relative;
        z-index: 10;
    }
    
    section[data-testid="stSidebar"] > div > div {
        width: 200px;
        position: relative;
        z-index: 10;
    }
    
    /* Ensure all Streamlit elements are visible */
    [data-testid="stSidebar"] {
        position: relative;
        z-index: 10;
    }
    
    [data-testid="stSidebar"] * {
        position: relative;
        z-index: 10;
    }
    
    /* Force all content to be visible */
    .main .block-container, .main .block-container * {
        position: relative;
        z-index: 10;
    }
    
    .stMarkdown, .stButton, .stTextInput, .stTabs, .stColumns {
        position: relative;
        z-index: 10;
    }

    /* --- FORCE REMOVE RED TAB INDICATOR --- */
    [data-testid="stTabs"] [data-testid^="stTab"]::before,
    [data-testid="stTabs"] [data-testid^="stTab"]::after,
    [data-testid="stTabs"] [role="tab"]::before,
    [data-testid="stTabs"] [role="tab"]::after,
    [data-testid="stTabs"] [data-testid^="stTabPanel"]::before,
    [data-testid="stTabs"] [data-testid^="stTabPanel"]::after {
        display: none !important;
        content: none !important;
        border: none !important;
        background: none !important;
        box-shadow: none !important;
        height: 0 !important;
        width: 0 !important;
    }
    [data-testid="stTabs"] [role="tablist"] {
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="stTabs"] [role="tab"] {
        border: none !important;
        box-shadow: none !important;
    }

    /* --- ULTRA FORCE REMOVE RED TAB INDICATOR --- */
    [data-testid="stTabs"] div[role="tablist"] > div {
        border: none !important;
        border-top: none !important;
        border-bottom: none !important;
        background: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
        height: auto !important;
        min-height: 0 !important;
    }
    [data-testid="stTabs"] div[role="tablist"] > * {
        border: none !important;
        border-top: none !important;
        border-bottom: none !important;
        background: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stTabs"] div[role="tablist"] [style*="red"],
    [data-testid="stTabs"] div[role="tablist"] [style*="#f00"],
    [data-testid="stTabs"] div[role="tablist"] [style*="rgb(255, 0, 0)"] {
        border: none !important;
        background: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* Hide the default radio dot */
    div[data-testid="stRadio"] > label > div:first-child { display: none !important; }
    /* Style the radio as tabs */
    div[data-testid="stRadio"] label {
        background: rgba(255,255,255,0.08);
        color: #fff;
        border: none;
        border-radius: 10px 10px 0 0;
        padding: 10px 28px;
        font-size: 1.08rem;
        font-weight: 500;
        cursor: pointer;
        margin-right: 8px;
        margin-bottom: -2px;
        transition: background 0.2s, color 0.2s;
        box-shadow: 0 2px 8px rgba(102,126,234,0.08);
    }
    div[data-testid="stRadio"] label[data-selected="true"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        font-weight: bold;
        border-bottom: 2px solid transparent;
        box-shadow: 0 4px 16px rgba(102,126,234,0.18);
    }
    div[data-testid="stRadio"] label:hover {
        background: rgba(102,126,234,0.18);
        color: #fff;
    }
    div[data-testid="stRadio"] { margin-bottom: 18px; }

    /* Sidebar as full-height flex column */
    [data-testid="stSidebar"] > div:first-child {
        display: flex !important;
        flex-direction: column !important;
        height: 100vh !important;
        min-height: 100vh !important;
        padding: 0 !important;
    }
    .sidebar-main {
        flex: 1 1 auto;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        width: 100%;
    }
    .sidebar-enter-city {
        position: static !important;
        width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        border-radius: 14px !important;
        box-sizing: border-box;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding-top: 0.7rem;
        padding-bottom: 0.7rem;
        color: white;
        text-align: center;
        z-index: 1;
    }
    .sidebar-credit {
        flex-shrink: 0;
        width: 100% !important;
        border-radius: 0 !important;
        box-sizing: border-box;
        background: rgba(255,255,255,0.1);
        padding: 1.2rem 1rem;
        color: white;
        font-size: 1.1rem;
        font-weight: bold;
        border-top: 1px solid rgba(255,255,255,0.2);
        margin: 0 !important;
        text-align: center;
    }
    /* Modern, right-aligned collapse button */
    [data-testid="stSidebarCollapseControl"] {
        display: none !important;
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
    
    # Check if we have cached news and it's still fresh
    if WEATHER_NEWS_CACHE_KEY in st.session_state:
        cached_data = st.session_state[WEATHER_NEWS_CACHE_KEY]
        if current_time - cached_data['timestamp'] < WEATHER_NEWS_CACHE_DURATION:
            return cached_data['news']
    
    # Try to fetch real weather news from NewsAPI (if API key is available)
    news_api_key = os.getenv("NEWS_API_KEY")
    
    if news_api_key:
        try:
            # Fetch weather-related news from NewsAPI
            news_url = "https://newsapi.org/v2/everything"
            params = {
                'q': 'weather OR climate OR storm OR hurricane OR tornado OR flood OR wildfire',
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': 6,
                'apiKey': news_api_key
            }
            
            response = requests.get(news_url, params=params, timeout=10)
            if response.status_code == 200:
                news_data = response.json()
                articles = news_data.get('articles', [])
                
                if articles:
                    weather_news = []
                    for article in articles[:3]:  # Get top 3 articles
                        weather_news.append({
                            'title': article.get('title', 'Weather Update'),
                            'description': article.get('description', 'Weather-related news'),
                            'content': article.get('content', ''),
                            'url': article.get('url', '#'),
                            'source': article.get('source', {}).get('name', 'News Source'),
                            'published_at': article.get('publishedAt', ''),
                            'icon': get_weather_news_icon(article.get('title', ''))
                        })
                    
                    # Cache the news
                    st.session_state[WEATHER_NEWS_CACHE_KEY] = {
                        'news': weather_news,
                        'timestamp': current_time
                    }
                    return weather_news
        except Exception as e:
            st.warning(f"Could not fetch real-time weather news: {e}")
    
    # Fallback to curated weather news if API fails or no key
    if not news_api_key:
        # Show info about NewsAPI key (only once per session)
        if "news_api_info_shown" not in st.session_state:
            st.info("💡 Want real-time weather news? Get a free NewsAPI key from newsapi.org and add it as NEWS_API_KEY in your environment variables!")
            st.session_state["news_api_info_shown"] = True
    
    fallback_news = get_fallback_weather_news()
    
    # Cache the fallback news
    st.session_state[WEATHER_NEWS_CACHE_KEY] = {
        'news': fallback_news,
        'timestamp': current_time
    }
    
    return fallback_news

def get_weather_news_icon(title):
    """Get appropriate weather icon based on news title"""
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
            'content': 'Recent climate data shows significant shifts in global weather patterns, affecting regions from the Arctic to the tropics. Researchers are monitoring these changes closely.',
            'url': 'https://www.climate.gov/news-features',
            'source': 'Climate.gov',
            'published_at': current_date,
            'icon': '🌍'
        },
        {
            'title': 'Extreme Weather Events Increase',
            'description': 'Frequency of severe storms and natural disasters rises globally',
            'content': 'Meteorologists report an increase in extreme weather events worldwide, including hurricanes, floods, and heatwaves affecting millions of people.',
            'url': 'https://www.wmo.int/news',
            'source': 'World Meteorological Organization',
            'published_at': current_date,
            'icon': '⛈️'
        },
        {
            'title': 'Renewable Energy Weather Impact',
            'description': 'Weather conditions significantly affect renewable energy production',
            'content': 'Solar and wind energy production varies dramatically with weather conditions, highlighting the importance of accurate weather forecasting for energy planning.',
            'url': 'https://www.energy.gov/weather',
            'source': 'Department of Energy',
            'published_at': current_date,
            'icon': '☀️'
        }
    ]

def display_weather_news():
    """Display the entire Global Weather News section inside a single card container with gradient background and a working Streamlit refresh button."""
    # Get fresh weather news
    weather_news = get_weather_news()

    # Calculate time since last update
    if WEATHER_NEWS_CACHE_KEY in st.session_state:
        last_update = st.session_state[WEATHER_NEWS_CACHE_KEY]['timestamp']
        time_since_update = time.time() - last_update
        minutes_since_update = int(time_since_update // 60)
    else:
        minutes_since_update = 0

    # Card style for the news section
    st.markdown(f"""
    <div style='width: 100%; max-width: 900px; margin: 0 auto 2rem auto; background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%); box-shadow: 0 4px 24px rgba(0,0,0,0.12); border-radius: 18px; padding: 2.2rem 2.2rem 1.5rem 2.2rem;'>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.2rem;">
            <div style="display: flex; align-items: center; gap: 0.7rem;">
                <span style='font-size: 2rem;'>🌍</span>
                <span style="font-size: 1.5rem; font-weight: bold; color: #fff; letter-spacing: 0.5px;">Global Weather News</span>
            </div>
            <div id="refresh-news-btn-container" style="display: flex; align-items: center; gap: 0.7rem;">
                <span id="refresh-news-btn-anchor"></span>
                <span style="font-size: 0.98rem; color: #d0f0ff; font-style: italic;">Updated {minutes_since_update} min ago</span>
            </div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 1.1rem;">
    """, unsafe_allow_html=True)

    # Place the Streamlit button using the anchor
    components.html("""
    <script>
    // Move the Streamlit button into the card
    window.addEventListener('DOMContentLoaded', function() {
        var btn = document.querySelector('button[kind="secondary"]');
        var anchor = document.getElementById('refresh-news-btn-anchor');
        if (btn && anchor && !anchor.hasChildNodes()) {
            anchor.appendChild(btn);
        }
    });
    </script>
    """, height=0)
    if st.button("🔄 Refresh News", key="refresh_news_button", help="Refresh News", type="secondary"):
        if WEATHER_NEWS_CACHE_KEY in st.session_state:
            del st.session_state[WEATHER_NEWS_CACHE_KEY]
        st.rerun()

    for i, news in enumerate(weather_news):
        # Format the published date
        try:
            if news['published_at']:
                pub_date = datetime.fromisoformat(news['published_at'].replace('Z', '+00:00'))
                formatted_date = pub_date.strftime('%b %d, %Y')
            else:
                formatted_date = "Recent"
        except:
            formatted_date = "Recent"
        st.markdown(f"""
            <div style="display: flex; align-items: flex-start; gap: 1rem; background: rgba(255,255,255,0.04); border-radius: 12px; padding: 1.1rem 1rem; margin-bottom: 0.1rem;">
                <span style="font-size: 2rem; flex-shrink: 0;">{news['icon']}</span>
                <div style="flex: 1;">
                    <span style="font-weight: bold; color: #fff; font-size: 1.18rem;">{news['title']}</span><br/>
                    <span style="color: #fff; font-size: 1.02rem; font-weight: 500;">{news['description']}</span><br/>
                    <span style="color: #e0e0e0; font-size: 0.98rem;">{news['content'][:180]}{'...' if len(news['content']) > 180 else ''}</span><br/>
                    <span style="color: #d0f0ff; font-size: 0.96rem;">Source: <a href='{news['url']}' target='_blank' style='color:#fff; text-decoration:underline;'>{news['source']}</a> • {formatted_date}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

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
        st.error(f"Error fetching weather data: {e}")
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
        st.error(f"Error fetching forecast data: {e}")
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
    
    # Center the main weather display
    col1, col2, col3 = st.columns([1.2, 1.6, 1.2])
    
    with col2:
        st.markdown(f"""
        <div class="weather-card fade-in" style="max-width: 320px; margin: 0 auto; display: flex; flex-direction: column; align-items: center; justify-content: center;">
            <div class="weather-icon-large">{weather_icon}</div>
            <div class="temperature-display">{temp:.1f}°C</div>
            <div style="margin: 0.2rem 0; width: 100%; display: flex; flex-direction: column; align-items: flex-start;">
                <h4 style="margin: 0.2rem 0 0.2rem 18px; font-size: 1.1rem; align-self: flex-start;">{weather_desc}</h4>
                <p style="margin: 0.2rem 0 0.2rem 18px; font-size: 0.85rem; align-self: flex-start;">{city}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Weather metrics in a grid below
    st.markdown("### 🌡️ Weather Details")
    
    # First row of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h6>🌡️ Feels Like</h6>
            <h5>{weather_data['main']['feels_like']:.1f}°C</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h6>💧 Humidity</h6>
            <h5>{weather_data['main']['humidity']}%</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h6>💨 Wind</h6>
            <h5>{weather_data['wind']['speed']} m/s</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h6>☁️ Cloud Cover</h6>
            <h5>{weather_data['clouds']['all']}%</h5>
        </div>
        """, unsafe_allow_html=True)
    
    # Second row of metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h6>🌧️ Precipitation</h6>
            <h5>{weather_data.get('rain', {}).get('1h', 0)} mm</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h6>📊 Pressure</h6>
            <h5>{weather_data['main']['pressure']} hPa</h5>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h6>👁️ Visibility</h6>
            <h5>{weather_data['visibility']/1000:.1f} km</h5>
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
        <div class="metric-card">
            <h6>☀️ UV Index</h6>
            <h5>{uv_index}</h5>
        </div>
        """, unsafe_allow_html=True)
    
    # Climate overview and sunrise/sunset side by side
    st.markdown("### 🌍 Climate Overview")
    climate_info = get_climate_summary(city, temp, weather_desc)
    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise'])
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset'])
    # --- Parent container for alignment ---
    st.markdown(f"""
    <div style='width: 100%;'>
        <div style="display: flex; gap: 1.5rem; align-items: stretch; margin-bottom: 0.5rem;">
            <div style="flex: 2.2; display: flex; flex-direction: column; min-width: 0;">
                <div class="climate-summary" style="width: 100%; min-height: 200px; display: flex; flex-direction: column; justify-content: stretch;">
                    <h6>🌤️ Weather Overview</h6>
                    <p style="font-size: 0.9rem;"><strong>Current Season:</strong> {climate_info['season']}</p>
                    <p style="font-size: 0.9rem;"><strong>Climate Type:</strong> {climate_info['climate']}</p>
                    <p style="font-size: 0.9rem;"><strong>Description:</strong> {climate_info['description']}</p>
                    <p style="font-size: 0.9rem;"><strong>Hottest Month:</strong> July (typically 25-30°C)</p>
                    <p style="font-size: 0.9rem;"><strong>Coldest Month:</strong> January (typically 0-5°C)</p>
                </div>
            </div>
            <div style="flex: 1; display: flex; flex-direction: column; gap: 1rem; min-width: 0;">
                <div class="feature-highlight" style="padding: 1.2rem; margin-bottom: 0.5rem; min-height: 90px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <div style="font-size: 1.2rem; font-weight: 600; color: black; margin-bottom: 0.5rem; text-align: center;">🌅 Sunrise</div>
                    <div class="sun-time">{sunrise.strftime('%H:%M')}</div>
                </div>
                <div class="feature-highlight" style="padding: 1.2rem; min-height: 90px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                    <div style="font-size: 1.2rem; font-weight: 600; color: black; margin-bottom: 0.5rem; text-align: center;">🌇 Sunset</div>
                    <div class="sun-time">{sunset.strftime('%H:%M')}</div>
                </div>
            </div>
        </div>
        <!-- Weather News will be displayed separately -->
    </div>
    """, unsafe_allow_html=True)

def display_forecast(forecast_data):
    """Display 5-day weather forecast with enhanced charts"""
    if not forecast_data:
        return
    
    # Process forecast data
    forecast_list = forecast_data['list']
    daily_data = []
    
    for item in forecast_list:
        date = datetime.fromtimestamp(item['dt'])
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
    
    df = pd.DataFrame(daily_data)
    
    # Enhanced temperature chart
    fig_temp = go.Figure()
    
    fig_temp.add_trace(go.Scatter(
        x=df['Time'],
        y=df['Temperature (°C)'],
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#667eea', width=3),
        marker=dict(size=8, color=df['Color'])
    ))
    
    fig_temp.update_layout(
        title='🌡️ Temperature Forecast (5 Days)',
        xaxis_title="Time",
        yaxis_title="Temperature (°C)",
        template='plotly_white',
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Enhanced humidity chart
    fig_humidity = go.Figure()
    
    fig_humidity.add_trace(go.Bar(
        x=df['Time'],
        y=df['Humidity (%)'],
        name='Humidity',
        marker_color='#764ba2',
        opacity=0.8
    ))
    
    fig_humidity.update_layout(
        title='💧 Humidity Forecast (5 Days)',
        xaxis_title="Time",
        yaxis_title="Humidity (%)",
        template='plotly_white',
        height=300,
        showlegend=False
    )
    
    st.plotly_chart(fig_humidity, use_container_width=True)
    
    # Daily summary cards
    st.subheader("📅 Daily Forecast Summary")
    
    daily_summary = df.groupby('Date').agg({
        'Temperature (°C)': ['min', 'max', 'mean'],
        'Humidity (%)': 'mean',
        'Weather': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
        'Icon': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
    }).round(1)
    
    daily_summary.columns = ['Min Temp', 'Max Temp', 'Avg Temp', 'Avg Humidity', 'Weather', 'Icon']
    daily_summary = daily_summary.reset_index()
    
    # Display daily summary in cards
    for _, row in daily_summary.iterrows():
        st.markdown(f"""
        <div class="forecast-card fade-in">
            <div style="display: flex; flex-direction: row; justify-content: space-between; align-items: flex-start;">
                <div style="display: flex; flex-direction: column; align-items: flex-start; margin-right: 1.5rem;">
                    <span style="font-size: 1.05rem; font-weight: 600; margin-bottom: 0.1rem;">{row['Date']}</span>
                    <span style="font-size: 0.98rem; margin-top: 0;">{row['Icon']} {row['Weather']}</span>
                </div>
                <div style="text-align: right; align-self: center;">
                    <h6 style="margin: 0;">{row['Min Temp']}°C / {row['Max Temp']}°C</h6>
                    <span style="font-size: 0.9rem;">Avg: {row['Avg Temp']}°C | 💧 {row['Avg Humidity']}%</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_weather_map(weather_data, forecast_data):
    """Display interactive weather map with enhanced styling"""
    if not weather_data:
        return
    
    # Create a map centered on the city
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    
    m = folium.Map(
        location=[lat, lon], 
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add current weather marker with enhanced popup
    current_temp = weather_data['main']['temp']
    current_desc = weather_data['weather'][0]['description']
    current_icon = get_weather_icon(weather_data['weather'][0]['icon'])
    
    folium.Marker(
        [lat, lon],
        popup=f"""
        <div style="text-align: center;">
            <h3>{current_icon} Current Weather</h3>
            <p><strong>{current_desc}</strong></p>
            <p><strong>Temperature:</strong> {current_temp}°C</p>
            <p><strong>Humidity:</strong> {weather_data['main']['humidity']}%</p>
            <p><strong>Wind:</strong> {weather_data['wind']['speed']} m/s</p>
        </div>
        """,
        tooltip=f"Current Weather: {current_temp}°C",
        icon=folium.Icon(color='red', icon='info-sign', prefix='fa')
    ).add_to(m)
    
    # Add forecast markers if available
    if forecast_data:
        forecast_list = forecast_data['list']
        for i, item in enumerate(forecast_list[:8]):  # Show first 8 forecasts
            forecast_lat = lat + (i * 0.01)  # Offset slightly for visibility
            forecast_lon = lon + (i * 0.01)
            forecast_temp = item['main']['temp']
            forecast_desc = item['weather'][0]['description']
            forecast_icon = get_weather_icon(item['weather'][0]['icon'])
            forecast_time = datetime.fromtimestamp(item['dt']).strftime('%H:%M')
            
            folium.Marker(
                [forecast_lat, forecast_lon],
                popup=f"""
                <div style="text-align: center;">
                    <h4>{forecast_icon} Forecast</h4>
                    <p><strong>{forecast_desc}</strong></p>
                    <p><strong>Temperature:</strong> {forecast_temp}°C</p>
                    <p><strong>Time:</strong> {forecast_time}</p>
                </div>
                """,
                tooltip=f"Forecast {forecast_time}: {forecast_temp}°C",
                icon=folium.Icon(color='blue', icon='cloud', prefix='fa')
            ).add_to(m)
    
    # Display the map
    st.markdown('<div class="map-container">', unsafe_allow_html=True)
    st.subheader("🗺️ Weather Map")
    folium_static(m, width=800, height=350)
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    # Enhanced header
    st.markdown("""
    <div class="main-header">
        <h1>🌤️ Weather App</h1>
        <p style="font-size: 1rem; margin: 0;">Get real-time weather conditions and forecasts for any city around the world!</p>
    </div>
    """, unsafe_allow_html=True)

    # City input card at the top of the main page (text left, icon after text)
    st.markdown("""
    <div style="
        max-width: 320px;
        margin: 2rem auto 1.5rem auto;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        color: white;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: center;
        padding: 1.1rem 1.2rem 1.2rem 1.2rem;
        min-height: 90px;
    ">
        <div style="display: flex; flex-direction: row; align-items: center; justify-content: flex-start; width: 100%; min-height: 38px;">
            <h4 style="margin: 0; color: white; font-size: 1.08rem; font-weight: bold; text-align: left;">Enter City</h4>
            <span style="font-size: 1.3rem; margin-left: 0.6rem; display: flex; align-items: center;">📍</span>
        </div>
    """, unsafe_allow_html=True)
    city = st.text_input("City name:", value="London", key="city_input", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

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
        st.markdown("""
        <style>
        /* Hide the default radio dot */
        div[data-testid=\"stRadio\"] > label > div:first-child { display: none !important; }
        /* Style the radio as tabs */
        div[data-testid=\"stRadio\"] label {
            background: rgba(255,255,255,0.08);
            color: #fff;
            border: none;
            border-radius: 10px 10px 0 0;
            padding: 10px 28px;
            font-size: 1.08rem;
            font-weight: 500;
            cursor: pointer;
            margin-right: 8px;
            margin-bottom: -2px;
            transition: background 0.2s, color 0.2s;
            box-shadow: 0 2px 8px rgba(102,126,234,0.08);
        }
        div[data-testid=\"stRadio\"] label[data-selected=\"true\"] {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: #fff;
            font-weight: bold;
            border-bottom: 2px solid transparent;
            box-shadow: 0 4px 16px rgba(102,126,234,0.18);
        }
        div[data-testid=\"stRadio\"] label:hover {
            background: rgba(102,126,234,0.18);
            color: #fff;
        }
        div[data-testid=\"stRadio\"] { margin-bottom: 18px; }
        </style>
        """, unsafe_allow_html=True)
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
            display_forecast(st.session_state["forecast_data"])
        elif selected_tab == "🗺️ Weather Map":
            display_weather_map(st.session_state["weather_data"], st.session_state["forecast_data"])

    # Display weather news
    display_weather_news()

if __name__ == "__main__":
    main() 