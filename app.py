import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="wide"
)

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

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius"""
    return kelvin - 273.15

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

def display_current_weather(weather_data):
    """Display current weather information"""
    if not weather_data:
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Temperature",
            value=f"{weather_data['main']['temp']:.1f}°C",
            delta=f"{weather_data['main']['feels_like']:.1f}°C (feels like)"
        )
    
    with col2:
        st.metric(
            label="Humidity",
            value=f"{weather_data['main']['humidity']}%"
        )
    
    with col3:
        st.metric(
            label="Wind Speed",
            value=f"{weather_data['wind']['speed']} m/s"
        )
    
    # Weather description
    weather_desc = weather_data['weather'][0]['description'].title()
    weather_icon = get_weather_icon(weather_data['weather'][0]['icon'])
    
    st.markdown(f"### {weather_icon} {weather_desc}")
    
    # Additional details
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.info(f"**Pressure:** {weather_data['main']['pressure']} hPa")
    
    with col2:
        st.info(f"**Visibility:** {weather_data['visibility']/1000:.1f} km")
    
    with col3:
        if 'rain' in weather_data:
            st.info(f"**Rain (1h):** {weather_data['rain'].get('1h', 0)} mm")
        else:
            st.info("**Rain (1h):** 0 mm")
    
    with col4:
        sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise'])
        sunset = datetime.fromtimestamp(weather_data['sys']['sunset'])
        st.info(f"**Sunrise:** {sunrise.strftime('%H:%M')}")
        st.info(f"**Sunset:** {sunset.strftime('%H:%M')}")

def display_forecast(forecast_data):
    """Display 5-day weather forecast"""
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
            'Icon': weather_icon
        })
    
    df = pd.DataFrame(daily_data)
    
    # Create temperature chart
    fig_temp = px.line(df, x='Time', y='Temperature (°C)', 
                      title='Temperature Forecast (5 Days)',
                      markers=True)
    fig_temp.update_layout(xaxis_title="Time", yaxis_title="Temperature (°C)")
    st.plotly_chart(fig_temp, use_container_width=True)
    
    # Create humidity chart
    fig_humidity = px.bar(df, x='Time', y='Humidity (%)',
                         title='Humidity Forecast (5 Days)',
                         color='Humidity (%)')
    fig_humidity.update_layout(xaxis_title="Time", yaxis_title="Humidity (%)")
    st.plotly_chart(fig_humidity, use_container_width=True)
    
    # Display forecast table
    st.subheader("Detailed Forecast")
    
    # Group by date and show daily summary
    daily_summary = df.groupby('Date').agg({
        'Temperature (°C)': ['min', 'max', 'mean'],
        'Humidity (%)': 'mean',
        'Weather': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0],
        'Icon': lambda x: x.mode()[0] if len(x.mode()) > 0 else x.iloc[0]
    }).round(1)
    
    daily_summary.columns = ['Min Temp', 'Max Temp', 'Avg Temp', 'Avg Humidity', 'Weather', 'Icon']
    daily_summary = daily_summary.reset_index()
    
    # Display daily summary
    for _, row in daily_summary.iterrows():
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.write(f"**{row['Date']}**")
        
        with col2:
            st.write(f"{row['Icon']} {row['Weather']}")
        
        with col3:
            st.write(f"**{row['Min Temp']}°C** / **{row['Max Temp']}°C**")
        
        with col4:
            st.write(f"Avg: **{row['Avg Temp']}°C**")
        
        with col5:
            st.write(f"Humidity: **{row['Avg Humidity']}%**")
        
        st.divider()

def display_weather_map(weather_data, forecast_data):
    """Display interactive weather map"""
    if not weather_data:
        return
    
    # Create a map centered on the city
    lat = weather_data['coord']['lat']
    lon = weather_data['coord']['lon']
    
    m = folium.Map(location=[lat, lon], zoom_start=10)
    
    # Add current weather marker
    current_temp = weather_data['main']['temp']
    current_desc = weather_data['weather'][0]['description']
    current_icon = get_weather_icon(weather_data['weather'][0]['icon'])
    
    folium.Marker(
        [lat, lon],
        popup=f"{current_icon} {current_desc}<br>Temperature: {current_temp}°C",
        tooltip=f"Current Weather: {current_temp}°C",
        icon=folium.Icon(color='red', icon='info-sign')
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
                popup=f"{forecast_icon} {forecast_desc}<br>Temperature: {forecast_temp}°C<br>Time: {forecast_time}",
                tooltip=f"Forecast {forecast_time}: {forecast_temp}°C",
                icon=folium.Icon(color='blue', icon='cloud')
            ).add_to(m)
    
    # Display the map
    st.subheader("Weather Map")
    folium_static(m)

def main():
    st.title("🌤️ Weather App")
    st.markdown("Get current weather conditions and forecasts for any city around the world!")
    
    # Sidebar for city input
    st.sidebar.header("📍 Location")
    city = st.sidebar.text_input("Enter city name:", value="London")
    
    if st.sidebar.button("Get Weather", type="primary"):
        if not API_KEY or API_KEY == "your_api_key_here":
            st.error("⚠️ Please set your OpenWeather API key in the .env file!")
            st.info("Get your free API key from: https://openweathermap.org/api")
            return
        
        # Get weather data
        with st.spinner("Fetching weather data..."):
            weather_data = get_weather_data(city, API_KEY)
            forecast_data = get_forecast_data(city, API_KEY)
        
        if weather_data:
            st.success(f"✅ Weather data loaded for {city}")
            
            # Create tabs for different features
            tab1, tab2, tab3 = st.tabs(["🌡️ Current Weather", "📅 5-Day Forecast", "🗺️ Weather Map"])
            
            with tab1:
                st.header(f"Current Weather in {city}")
                display_current_weather(weather_data)
            
            with tab2:
                st.header(f"5-Day Forecast for {city}")
                display_forecast(forecast_data)
            
            with tab3:
                display_weather_map(weather_data, forecast_data)
        else:
            st.error("❌ Could not fetch weather data. Please check the city name and try again.")
    
    # Instructions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Instructions")
    st.sidebar.markdown("""
    1. Enter a city name in the input field
    2. Click 'Get Weather' to fetch data
    3. Explore the three tabs:
       - **Current Weather**: Live conditions
       - **5-Day Forecast**: Extended predictions
       - **Weather Map**: Interactive map view
    """)
    
    # API key setup instructions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Setup")
    st.sidebar.markdown("""
    To use this app, you need an OpenWeather API key:
    1. Sign up at [OpenWeather](https://openweathermap.org/api)
    2. Create a `.env` file in this directory
    3. Add: `OPENWEATHER_API_KEY=your_api_key_here`
    """)

if __name__ == "__main__":
    main() 