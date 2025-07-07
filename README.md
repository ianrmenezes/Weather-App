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

### 4. 📰 Weather News
- Latest weather-related news and updates
- Global weather stories and climate information
- Curated weather headlines and descriptions

## 🌐 Deployment (for Developers or Curious Techies)

Want to run this app yourself or customize it? Here's how you can get it online!

### 🚀 Option 1: Streamlit Cloud (Easiest & Recommended)

This is the quickest way to make your weather app live and shareable:

1. Push your code to GitHub (if it's not already there)
2. Go to Streamlit Cloud and sign in with your GitHub account
3. Click on "New app"
4. Select your GitHub repo and set the main file as `app.py`
5. Add your API key:
   - Key: `OPENWEATHER_API_KEY`
   - Value: your actual OpenWeather API key
6. Hit Deploy

That's it — your app will be live on the internet! You'll get a link you can share with anyone.

### ⚡ Other Hosting Options (If You Want More Control)

If you're feeling adventurous, you can also deploy to other platforms:

#### 🛠️ Railway
1. Go to railway.app
2. Link your GitHub repo
3. Add your `OPENWEATHER_API_KEY` as an environment variable
4. Click Deploy, and you're done!

#### 🌐 Render
1. Visit render.com
2. Create a new Web Service
3. Connect your GitHub repository
4. Set up the build and start commands:
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py`
5. Add your environment variable as usual

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

### Weather News Section
- Latest weather headlines and stories
- Global climate updates and weather events
- Curated weather-related news content

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **OpenWeather** – for the awesome weather API
- **Streamlit** – for making web apps easy
- **The Python community** – for the amazing libraries