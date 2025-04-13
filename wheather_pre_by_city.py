import requests
import google.generativeai as genai

# ✅ Step 1: Fetch Real-Time Weather Data for User-Entered Location
def get_weather(api_key, location):
    """Fetches real-time weather data for the given location."""
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "location": data["location"]["name"],
            "temperature": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"]
        }
    return None

# ✅ Step 2: Use AI to Suggest the Best Crop for the Entered Location
def suggest_best_crop(gemini_api_key, weather_data):
    """Uses Google Gemini AI to suggest the most suitable crop based on weather conditions."""
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("models/gemini-1.5-pro")

    prompt = f"""
    A farmer is located in {weather_data['location']} with the following real-time weather conditions:
    - Temperature: {weather_data['temperature']}°C
    - Humidity: {weather_data['humidity']}%

    Based on these conditions, suggest the best crops to grow, considering the climate, soil suitability, and rainfall patterns.
    Provide a ranked list with reasoning.
    """

    response = model.generate_content(prompt)
    return response.text

# ✅ Step 3: Main Function
def wheather_pred_by_city(location:str):
    WEATHER_API_KEY = "68ceae54736449fe90542050251903"  # Replace with your WeatherAPI.com key
    GEMINI_API_KEY = "AIzaSyDAkDANkg9qFkRiSqErrFeq-TWd65vVo3w"  # Replace with your Gemini API key

    

    print("\n🔍 Fetching real-time weather data...\n")
    weather_data = get_weather(WEATHER_API_KEY, location)

    if not weather_data:
        print("❌ Unable to fetch weather data. Please check the location and try again.")
        return

    print(f"✅ Weather in {weather_data['location']}: {weather_data['temperature']}°C, {weather_data['humidity']}% Humidity\n")

    print("🤖 AI Analyzing Best Crops for Your Climate...\n")
    best_crops = suggest_best_crop(GEMINI_API_KEY, weather_data)

    print("🌾 Recommended Crops to Grow:\n")
    return best_crops
