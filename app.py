import os
import re
import requests
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI, APIError

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("OPENAI_API_KEY")  # set this in your environment
MODEL_NAME = "gpt-4o-mini"

client = OpenAI(api_key=API_KEY) if API_KEY else None


def strip_markdown(text: str) -> str:
    if not text:
        return text

    # Remove bold/italic/code markers (*, **, __, `, ``` etc.)
    text = re.sub(r'(\*{1,2}|_{1,2}|`+)', '', text)

    # Remove markdown headings (#, ##, ### ...)
    text = re.sub(r'^#+\s*', '', text, flags=re.MULTILINE)

    # Remove bullets (-, *, +, •)
    text = re.sub(r'^[\-\*\+•]\s+', '', text, flags=re.MULTILINE)

    # Remove numbered list prefixes like "1. "
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # Remove horizontal rules (---, ***)
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)

    return text.strip()


# -----------------------------------
# Real weather via Open-Meteo (no API key)
# -----------------------------------
def get_real_weather(city: str) -> dict:
    """
    Use Open-Meteo's free APIs:
      1) Geocoding API to turn city name into lat/lon
      2) Forecast API to get current weather

    Returns a small dict with normalized fields.
    Raises an exception if it fails (caller handles it).
    """
    if not city or not city.strip():
        raise ValueError("City name is required for weather lookup.")

    # 1) Geocode city name -> lat/lon
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
        
    }
    geo_resp = requests.get(geo_url, params=geo_params, timeout=5)
    geo_resp.raise_for_status()
    geo_data = geo_resp.json()

    if "results" not in geo_data or not geo_data["results"]:
        raise ValueError(f"Could not find location for '{city}'.")

    loc = geo_data["results"][0]
    latitude = loc["latitude"]
    longitude = loc["longitude"]
    resolved_name = loc.get("name", city)
    country = loc.get("country", "")

    # 2) Fetch current weather for that location
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current_weather": "true",  
        "timezone": "auto",
        "temperature_unit": "fahrenheit",  
        "windspeed_unit": "mph", 
    }
    weather_resp = requests.get(weather_url, params=weather_params, timeout=5)
    weather_resp.raise_for_status()
    weather_data = weather_resp.json()

    current = weather_data.get("current_weather")
    if not current:
        raise ValueError(f"No current weather data available for '{city}'.")

    # Open-Meteo current_weather gives:
    #   temperature (°C), windspeed (km/h), winddirection, weathercode, time
    return {
        "city": resolved_name,
        "country": country,
        "latitude": latitude,
        "longitude": longitude,
        "temperature_f": current.get("temperature"),
        "windspeed_kmh": current.get("windspeed"),
        "weather_code": current.get("weathercode"),
        "time": current.get("time"),
    }


# -----------------------------------
# Core logic: get OpenAI recommendation
# -----------------------------------
def get_openai_response(city: str) -> dict:
    """
    Use Open-Meteo for real weather, then ask OpenAI to create
    a plain-language summary + outfit recommendation.
    """
    if not client:
        return {
            "text": "The AI backend is not configured yet because the OpenAI API key is missing on the server.",
            "sources": [],
        }

    if not city or not city.strip():
        return {
            "text": "I need a city name to help you decide what to wear.",
            "sources": [],
        }

    # 1) Get real weather data from Open-Meteo
    try:
        weather = get_real_weather(city)
    except Exception as e:
        print("Open-Meteo error:", e, flush=True)
        return {
            "text": "I couldn't fetch the live weather data for that location right now. Try another city or try again in a bit.",
            "sources": [],
        }

    # Build a compact description string to feed into the model
    weather_text = (
        f"Location: {weather['city']}, {weather['country']}. "
        f"Temperature: {weather['temperature_f']}°F. "
        f"Wind speed: {weather['windspeed_kmh']} km/h. "
        f"Weather code: {weather['weather_code']}. "
        f"Time of observation: {weather['time']}."
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly, witty personal stylist and weather guide. "
                "You are given REAL, live weather data for a location. "
                "Use ONLY this weather data. Do not make up different temperatures or conditions. "
                "First, briefly describe what the weather feels like to a normal person. "
                "Then, in a second paragraph, suggest what they should wear for a casual day out. "
                "Respond in plain, natural language only. Do NOT use markdown, headings, lists, "
                "asterisks, hashes, or bullet points."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Here is the live weather data:\n{weather_text}\n\n"
                "Based only on this, what is the weather like and what should I wear for a casual day out?"
            ),
        },
    ]

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
        )
        raw_text = completion.choices[0].message.content
        clean_text = strip_markdown(raw_text)

        return {
            "text": clean_text,
            "sources": [
                {
                    "title": "Open-Meteo (current weather)",
                    "uri": "https://open-meteo.com/",
                }
            ],
        }

    except APIError as e:
        print("OpenAI API error:", e, flush=True)
        return {
            "text": "I ran into an issue talking to the AI service. Try again in a moment.",
            "sources": [],
        }
    except Exception as e:
        print("Unexpected error in get_openai_response:", e, flush=True)
        return {
            "text": "Something went wrong on the server while I was generating your outfit suggestion.",
            "sources": [],
        }


# -----------------------------------
# Routes
# -----------------------------------
@app.route("/")
def index():
    return "OK", 200


@app.route("/api/get_recommendation", methods=["POST"])
def get_recommendation():
    data = request.json or {}
    city = data.get("city")

    if not city:
        return jsonify({"error": "Please provide a city name."}), 400

    print("Received city:", city, flush=True)
    response_data = get_openai_response(city)
    return jsonify(response_data), 200


# -----------------------------------
# Entry point
# -----------------------------------
if __name__ == "__main__":
    app.run(debug=True, port=5000)
