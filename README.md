# 🌤️ Weather App

A beautiful and interactive weather application built with Python and Streamlit that provides current weather conditions and forecasts for any city around the world.

## 🌐 Live App

**Try it now 👉** [Weather App](https://weather-app-erachaxm6d22gb6axgh4wd.streamlit.app)

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
- Daily summaries with min/max temperatures
- Weather condition icons and descriptions
- Visual data with line and bar charts

### 3. 🗺️ Interactive Weather Maps
- Interactive maps using Folium
- Current weather location markers
- Forecast markers for upcoming weather
- Popups with weather details
- Geographic visualization of conditions

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

## 🌐 Deployment

### Streamlit Cloud (Recommended)

**Streamlit Cloud is the best option for deploying Streamlit apps:**

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Sign up for Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account

3. **Deploy your app**
   - Click "New app"
   - Select your repository: `your-username/Weather-App`
   - Set the main file path: `app.py`
   - Add your environment variables:
     - Key: `OPENWEATHER_API_KEY`
     - Value: Your OpenWeather API key
   - Click "Deploy"

4. **Your app will be live** at: `https://your-app-name-your-username.streamlit.app`

### Alternative Deployment Options

#### Railway
- Go to [railway.app](https://railway.app)
- Connect your GitHub repository
- Add environment variable: `OPENWEATHER_API_KEY`
- Deploy automatically

#### Render
- Go to [render.com](https://render.com)
- Create a new Web Service
- Connect your GitHub repository
- Set build command: `pip install -r requirements.txt`
- Set start command: `streamlit run app.py`
- Add environment variable: `OPENWEATHER_API_KEY`

### Why Not Vercel?

Vercel is designed for static sites and serverless functions, not for Python applications like Streamlit that require:
- Persistent server environment
- WebSocket connections for real-time updates
- Python runtime with specific dependencies

## 📋 Dependencies

- **Streamlit** – Web framework
- **Requests** – API calls
- **Pandas** – Data handling
- **Plotly** – Interactive charts
- **Folium** – Map rendering
- **Streamlit-Folium** – Folium integration
- **Python-dotenv** – Environment variable handling

## 🎯 How to Use

1. Open the app in your browser
2. Enter a city name in the sidebar
3. Click "Get Weather"
4. Navigate through the tabs:
   - **Current Weather**: Live details
   - **5-Day Forecast**: Charts and trends
   - **Weather Map**: Visual geographic data

## 📊 Data Sources

- **OpenWeather API** — Provides current and forecast weather data
- (Free tier includes 1,000 calls/day – perfect for personal use)

## 🎨 Features in Detail

### Current Weather Tab
- "Feels like" temperature
- Humidity, wind, and pressure
- Weather condition icons
- Visibility and rain info
- Sunrise/sunset times

### Forecast Tab
- Temperature line chart
- Humidity bar chart
- Daily summaries
- Min/max temperatures

### Map Tab
- Map centered on selected city
- Red marker = current weather
- Blue markers = forecasts
- Popup weather details

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding new weather data visualizations
- Improving the UI/UX
- Adding more weather APIs
- Creating additional features

## 📝 License

This project is open source and available under the MIT License.

## �� Acknowledgments

- **OpenWeather** – for the awesome weather API
- **Streamlit** – for making web apps easy
- **The Python community** – for the amazing libraries