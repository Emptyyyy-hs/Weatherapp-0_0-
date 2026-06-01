<h1 align="center">🌦️ Weather App</h1>

<p align="center">
  <img src="https://github.com/user-attachments/assets/20d6c480-92dd-4b95-aaf4-f106175bbfdd"width="900" />
  <img src="https://github.com/user-attachments/assets/11385a93-79e0-46a4-9a65-95d7522188ed"width="900" />
  <img src="https://github.com/user-attachments/assets/c31e84c7-53f7-4fed-858d-895fa5f6a2da"width="900" />
   
  
</p>

<p align="center">
  Real-time weather information with temperature, humidity, wind speed, and city search.
</p>






# Weather App 🌤️

A simple desktop weather app built with Python and Tkinter.
Shows real-time weather for any city using the OpenWeatherMap API.

---

## What it shows

- Current temperature (switch between °C and °F)
- Weather condition with emoji icon
- Humidity, wind speed and direction
- Pressure, visibility, cloud cover
- Feels like temperature
- Sunrise and sunset times (local to the searched city)

---

## How to run

### Step 1 — Get a free API key

1. Go to [openweathermap.org](https://openweathermap.org) and create a free account
2. Click on your username → "My API Keys"
3. Copy the key shown there (it activates within ~10 minutes)

### Step 2 — Add your API key

Open `weather_app.py` and replace this line near the top:

```python
API_KEY = "your_api_key_here"
```

Paste your actual key inside the quotes.

### Step 3 — Run the app

**Windows:** Double-click `run.bat`

```bash
pip install requests
python weather_app.py
```

---

## Requirements

- Python 3.8 or higher
- `requests` library (the run scripts install this automatically)
- Tkinter (comes built-in with Python)

---

## Project files

```
weather_app/
├── weather_app.py   main application code
├── run.bat          one-click launcher for Windows
├── requirements.txt pip install list
└── README.md       
```

---

## Built with

- Python 3
- Tkinter (for the GUI)
- requests (for calling the weather API)
- OpenWeatherMap free API
---

## ✨ Features

- 🔍 **City Search** — Search weather for any city worldwide
- 🌡️ **Temperature** — Displays current temperature and "feels like" in Celsius
- 😊 **Emoji Weather Icons** — Dynamic emoji that reflect real conditions (day/night aware)
- 💧 **Humidity & Pressure** — Full atmospheric data
- 💨 **Wind Speed & Direction** — Speed in km/h with compass direction (N, NE, SW, etc.)
- 👁️ **Visibility** — Atmospheric visibility in km
- ☁️ **Cloud Cover** — Percentage cloud coverage
- 🌅 **Sunrise & Sunset** — Local times adjusted to the city's timezone
- 🌙 **Day/Night Awareness** — Different emojis for day vs night conditions
- ⚡ **Non-blocking UI** — API calls run on a background thread (no freezing!)
- ❌ **Error Handling** — Friendly messages for invalid cities or network failures
---

## 🌦️ Weather Emoji Reference

| Condition        | Emoji |
|------------------|-------|
| Clear Sky (Day)  | ☀️    |
| Clear Sky (Night)| 🌙    |
| Few Clouds       | 🌤️   |
| Partly Cloudy    | ⛅    |
| Overcast         | ☁️    |
| Thunderstorm     | ⛈️   |
| Drizzle          | 🌦️   |
| Rain             | 🌧️   |
| Snow             | ❄️    |
| Freezing Rain    | 🌨️   |
| Fog / Mist       | 🌫️   |
| Haze             | 🌁    |
| Tornado          | 🌪️   |
| Volcanic Ash     | 🌋    |
---
## 📡 API Reference

This app uses the **OpenWeatherMap Current Weather API**:

```
GET http://api.openweathermap.org/data/2.5/weather
  ?q={city_name}
  &appid={API_KEY}
  &units=metric
```

**Key fields used:**
- `main.temp`, `main.feels_like`, `main.humidity`, `main.pressure`
- `wind.speed`, `wind.deg`
- `weather[0].id`, `weather[0].description`, `weather[0].icon`
- `clouds.all`, `visibility`
- `sys.sunrise`, `sys.sunset`, `sys.country`
- `timezone` (UTC offset in seconds)

---
