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
</style>
""", unsafe_allow_html=True)

# API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY", "your_api_key_here")
BASE_URL = "http://api.openweathermap.org/data/2.5"

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
        <div class="weather-card fade-in" style="max-width: 320px; margin: 0 auto;">
            <div class="weather-icon-large">{weather_icon}</div>
            <div class="temperature-display">{temp:.1f}°C</div>
            <div style="text-align: center; margin: 0.2rem 0;">
                <h4 style="margin: 0.2rem 0; font-size: 1.1rem;">{weather_desc}</h4>
                <p style="margin: 0.2rem 0; font-size: 0.85rem;">{city}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Weather metrics in a grid below
    st.markdown("### 📊 Weather Details")
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        climate_info = get_climate_summary(city, temp, weather_desc)
        st.markdown(f"""
        <div class="climate-summary">
            <h6>🌤️ Weather Overview</h6>
            <p style="font-size: 0.9rem;"><strong>Current Season:</strong> {climate_info['season']}</p>
            <p style="font-size: 0.9rem;"><strong>Climate Type:</strong> {climate_info['climate']}</p>
            <p style="font-size: 0.9rem;"><strong>Description:</strong> {climate_info['description']}</p>
            <p style="font-size: 0.9rem;"><strong>Hottest Month:</strong> July (typically 25-30°C)</p>
            <p style="font-size: 0.9rem;"><strong>Coldest Month:</strong> January (typically 0-5°C)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset'])
        
        st.markdown(f"""
        <div class="feature-highlight" style="padding: 1.2rem; margin-bottom: 0.5rem;">
            <h5 style="color: black; margin: 0.3rem 0;">🌅 Sunrise</h5>
            <p style="font-size: 1.3rem; font-weight: bold; color: black; margin: 0.5rem 0;">{sunrise.strftime('%H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="feature-highlight" style="padding: 1.2rem;">
            <h5 style="color: black; margin: 0.3rem 0;">🌇 Sunset</h5>
            <p style="font-size: 1.3rem; font-weight: bold; color: black; margin: 0.5rem 0;">{sunset.strftime('%H:%M')}</p>
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
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h6>{row['Date']}</h6>
                    <p style="font-size: 0.9rem;">{row['Icon']} {row['Weather']}</p>
                </div>
                <div style="text-align: right;">
                    <h6>{row['Min Temp']}°C / {row['Max Temp']}°C</h6>
                    <p style="font-size: 0.9rem;">Avg: {row['Avg Temp']}°C | 💧 {row['Avg Humidity']}%</p>
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
    
    # Small sidebar with just city input
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; color: white; text-align: center;">
            <h4>📍 Enter City</h4>
        </div>
        """, unsafe_allow_html=True)
        
        city = st.text_input("City name:", value="London", key="city_input")
        
        # Add space to push developer credit to bottom
        st.markdown("<br>" * 8, unsafe_allow_html=True)
        
        # Developer credit at bottom of sidebar
        st.markdown("""
        <div class="sidebar-credit">
            <p style="margin: 0; font-size: 1rem; font-weight: bold;">🚀 Developed by Ian Menezes</p>
            <p style="margin: 0; font-size: 0.8rem;">A beautiful weather app built with Python and Streamlit</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Weather display logic in main area
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
            # Create tabs for different features
            tab1, tab2, tab3 = st.tabs(["🌡️ Current Weather", "📅 5-Day Forecast", "🗺️ Weather Map"])
            
            with tab1:
                display_current_weather(weather_data, city)
            
            with tab2:
                st.header(f"📅 5-Day Forecast for {city}")
                display_forecast(forecast_data)
            
            with tab3:
                display_weather_map(weather_data, forecast_data)
        else:
            st.error("❌ Could not fetch weather data. Please check the city name and try again.")

if __name__ == "__main__":
    main() 