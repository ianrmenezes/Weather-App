# 🌤️ Weather App

A beautiful and interactive weather application built with Python and Streamlit that provides current weather conditions and forecasts for any city around the world.

## ✨ Features

### 1. 🌡️ Current Weather Display
- Real-time temperature, humidity, and wind speed
- Weather description with intuitive icons
- Additional details: pressure, visibility, rain data
- Sunrise and sunset times
- "Feels like" temperature

### 2. 📅 5-Day Weather Forecast
- Interactive temperature and humidity charts using Plotly
- Detailed hourly forecasts for the next 5 days
- Daily weather summaries with min/max temperatures
- Weather condition icons and descriptions
- Visual data representation with line and bar charts

### 3. 🗺️ Interactive Weather Maps
- Interactive maps using Folium
- Current weather location markers
- Forecast markers for upcoming weather conditions
- Popup information with weather details
- Geographic visualization of weather data

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- OpenWeather API key (free)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Weather-App
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your API key**
   - Sign up at [OpenWeather](https://openweathermap.org/api)
   - Get your free API key
   - Create a `.env` file in the project directory
   - Add your API key: `OPENWEATHER_API_KEY=your_actual_api_key`

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Navigate to [http://localhost:8501](http://localhost:8501) (or the port shown in your terminal)
   - Enter a city name and explore the weather data!

## 📋 Dependencies

- **Streamlit**: Web application framework
- **Requests**: HTTP library for API calls
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive charts and visualizations
- **Folium**: Interactive maps
- **Streamlit-Folium**: Streamlit integration for maps
- **Python-dotenv**: Environment variable management

## 🎯 How to Use

1. **Enter a city name** in the sidebar input field
2. **Click "Get Weather"** to fetch current and forecast data
3. **Explore the three tabs**:
   - **Current Weather**: Live conditions and detailed metrics
   - **5-Day Forecast**: Extended predictions with interactive charts
   - **Weather Map**: Geographic visualization of weather data

## 🔧 Configuration

The app uses environment variables for configuration. Create a `.env` file with:

```
OPENWEATHER_API_KEY=your_api_key_here
```

## 📊 Data Sources

- **OpenWeather API**: Provides current weather and forecast data
- **Free tier**: 1,000 calls per day (sufficient for personal use)

## 🎨 Features in Detail

### Current Weather Tab
- Temperature metrics with "feels like" comparison
- Humidity and wind speed indicators
- Weather condition with emoji icons
- Atmospheric pressure and visibility
- Rain data (if available)
- Sunrise and sunset times

### Forecast Tab
- Interactive temperature line chart
- Humidity bar chart with color coding
- Daily weather summaries
- Min/max temperature ranges
- Average conditions per day

### Map Tab
- Interactive map centered on the selected city
- Current weather marker (red)
- Forecast markers (blue) for upcoming conditions
- Popup information with weather details
- Geographic context for weather data

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new weather data visualizations
- Improving the UI/UX
- Adding more weather APIs
- Creating additional features

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- OpenWeather for providing the weather API
- Streamlit for the amazing web app framework
- The Python community for excellent libraries