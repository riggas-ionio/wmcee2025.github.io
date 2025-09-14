from decouple import config
import requests
import datetime

# --- SETTINGS ---

LAT, LON = 40.6401, 22.9444   # Thessaloniki coordinates
TOKEN = config('BOT_TOKEN')
CHAT_ID = config('CHAT_ID')
CITY = config('CITY')
LAT, LON = config('LAT'), config('LON')


# --- GET WEATHER ---
def get_forecast(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&daily=temperature_2m_max,temperature_2m_min,weathercode"
        "&timezone=auto"
    )
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

# Simple mapping for weather codes (Open-Meteo docs)
WEATHER_CODES = {
    0: "Clear",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate showers",
    82: "Violent showers",
    95: "Thunderstorm",
    96: "Thunderstorm w/ slight hail",
    99: "Thunderstorm w/ heavy hail",
}
WEATHER_ICONS = {
    0: "☀️",   # Clear
    1: "🌤️",  # Mainly clear
    2: "⛅",   # Partly cloudy
    3: "☁️",   # Overcast
    45: "🌫️",  # Fog
    48: "🌫️",  # Depositing rime fog
    51: "🌦️",  # Light drizzle
    53: "🌦️",  # Moderate drizzle
    55: "🌧️",  # Dense drizzle
    61: "🌧️",  # Slight rain
    63: "🌧️",  # Moderate rain
    65: "🌧️",  # Heavy rain
    71: "🌨️",  # Slight snow
    73: "🌨️",  # Moderate snow
    75: "❄️",   # Heavy snow
    80: "🌦️",  # Rain showers
    81: "🌧️",  # Moderate showers
    82: "⛈️",  # Violent showers
    95: "⛈️",  # Thunderstorm
    96: "⛈️🌨️", # Thunderstorm w/ slight hail
    99: "⛈️❄️", # Thunderstorm w/ heavy hail
}

def summarize_forecast(data, days=3):
    summary = [f"🌤 Weather forecast for {CITY} (next {days} days):"]
    for i in range(days):
        date = data["daily"]["time"][i]
        tmin = data["daily"]["temperature_2m_min"][i]
        tmax = data["daily"]["temperature_2m_max"][i]
        code = data["daily"]["weathercode"][i]
        desc = WEATHER_CODES.get(code, "Unknown")
        icon = WEATHER_ICONS.get(code, "❓")
        summary.append(f"{date}: {icon}  {desc}, {tmin:.0f}°C – {tmax:.0f}°C")
    
    # Add link for more details
    summary.append("\n🔗 5-days detailed forecast: https://meteo.gr/cf-en.cfm?city_id=1")
            
    return "\n".join(summary)

# --- SEND TO TELEGRAM ---
def send_telegram_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, data=payload)
    r.raise_for_status()

# --- MAIN ---
if __name__ == "__main__":
    forecast = get_forecast(LAT, LON)
    text = summarize_forecast(forecast, days=3)
    send_telegram_message(TOKEN, CHAT_ID, text)
    print(f"✅ Forecast sent to Telegram! \n{text}")
