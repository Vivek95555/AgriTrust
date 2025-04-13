import os
import requests
import google.generativeai as genai
import streamlit as st

# ✅ Step 1: Define Climate Requirements for Various Crops
crop_conditions = {
    "Wheat": {"min_temp": 10, "max_temp": 25, "min_humidity": 50, "max_humidity": 70},
    "Rice": {"min_temp": 20, "max_temp": 35, "min_humidity": 60, "max_humidity": 90},
    "Maize": {"min_temp": 18, "max_temp": 32, "min_humidity": 50, "max_humidity": 80},
    "Cotton": {"min_temp": 20, "max_temp": 35, "min_humidity": 40, "max_humidity": 70},
    "Potato": {"min_temp": 10, "max_temp": 22, "min_humidity": 60, "max_humidity": 80},
    "Tobacco": {"min_temp": 15, "max_temp": 30, "min_humidity": 60, "max_humidity": 85},
    "Sugarcane": {"min_temp": 20, "max_temp": 35, "min_humidity": 65, "max_humidity": 85},
    "Groundnut": {"min_temp": 20, "max_temp": 30, "min_humidity": 50, "max_humidity": 75},
    "Mustard": {"min_temp": 10, "max_temp": 25, "min_humidity": 40, "max_humidity": 70},
    "Soybean": {"min_temp": 20, "max_temp": 30, "min_humidity": 50, "max_humidity": 80},
    "Onion": {"min_temp": 13, "max_temp": 24, "min_humidity": 60, "max_humidity": 75},
    "Tomato": {"min_temp": 16, "max_temp": 27, "min_humidity": 60, "max_humidity": 80},
    "Chili": {"min_temp": 18, "max_temp": 30, "min_humidity": 60, "max_humidity": 75},
    "Coffee": {"min_temp": 15, "max_temp": 25, "min_humidity": 70, "max_humidity": 90},
    "Tea": {"min_temp": 13, "max_temp": 28, "min_humidity": 70, "max_humidity": 90}
}

# ✅ Step 2: Improved locations list covering major agricultural regions of India
INDIAN_LOCATIONS = [
    "Punjab, India",  # North India - Wheat, Rice
    "Haryana, India",  # North India - Wheat, Rice
    "Uttar Pradesh, India",  # North India - Sugarcane, Wheat
    "Bihar, India",  # East India - Rice, Maize
    "West Bengal, India",  # East India - Rice, Jute
    "Assam, India",  # Northeast India - Tea, Rice
    "Gujarat, India",  # West India - Cotton, Groundnut
    "Maharashtra, India",  # West India - Cotton, Sugarcane
    "Karnataka, India",  # South India - Coffee, Ragi
    "Tamil Nadu, India",  # South India - Rice, Sugarcane
    "Andhra Pradesh, India",  # South India - Rice, Cotton
    "Telangana, India",  # South India - Cotton, Rice
    "Madhya Pradesh, India",  # Central India - Soybean, Wheat
    "Chhattisgarh, India",  # Central India - Rice
    "Rajasthan, India",  # Northwest India - Mustard, Millet
    "Himachal Pradesh, India",  # North India - Apple, Potatoes
    "Kerala, India",  # South India - Coconut, Spices
    "Odisha, India"  # East India - Rice, Vegetables
]

# ✅ Step 3: Fetch Weather Data for a Given Location
def get_weather(api_key, location):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}&aqi=no"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "location": data["location"]["name"],
            "region": data["location"]["region"],
            "country": data["location"]["country"],
            "temperature": data["current"]["temp_c"],
            "humidity": data["current"]["humidity"],
            "condition": data["current"]["condition"]["text"],
            "wind_speed": data["current"]["wind_kph"],
            "precipitation": data["current"]["precip_mm"],
            "latitude": data["location"]["lat"],
            "longitude": data["location"]["lon"]
        }
    except Exception as e:
        if 'st' in globals():
            st.error(f"Error fetching weather data for {location}: {str(e)}")
        else:
            print(f"Error fetching weather data for {location}: {str(e)}")
        return None

# ✅ Step 4: Use Gemini AI to Analyze Suitable Locations for a Crop
def get_suitable_locations(gemini_api_key, crop, weather_data, crop_requirements):
    try:
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel("gemini-1.5-pro")

        prompt = f"""
        Analyze the most suitable locations in India for {crop} cultivation based on the following real-time weather data and crop requirements.
        
        Crop Requirements for {crop}:
        - Optimal Temperature Range: {crop_requirements['min_temp']}°C to {crop_requirements['max_temp']}°C
        - Optimal Humidity Range: {crop_requirements['min_humidity']}% to {crop_requirements['max_humidity']}%
        
        Current Weather Data:
        {weather_data}
        
        Please provide:
        1. A ranked list of the top 5 locations in India for {crop} cultivation based on this data
        2. For each location, explain precisely why it's suitable with direct reference to temperature and humidity
        3. Include any specific regions or districts within these states that are particularly well-known for {crop} cultivation
        4. Mention any additional factors that might affect {crop} cultivation in these locations (soil type, rainfall patterns, etc.)
        
        The output should be focused ONLY on India, with accurate geographical information about Indian agricultural regions.
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        error_msg = f"Error with Gemini AI: {str(e)}"
        if 'st' in globals():
            st.error(error_msg)
        else:
            print(error_msg)
        return "No AI response received due to an error."

# ✅ Step 5: Main Function for Crop Recommendation
def recommend_region(crop: str):
    # Try to get API keys from multiple sources
    weather_api_key = None
    if 'st' in globals() and 'WEATHER_API_KEY' in st.session_state:
        weather_api_key = st.session_state['WEATHER_API_KEY']
    if not weather_api_key:
        weather_api_key = os.environ.get("WEATHER_API_KEY")
    if not weather_api_key:
        weather_api_key = "68ceae54736449fe90542050251903"  # Fallback to your hardcoded key
    
    gemini_api_key = None
    if 'st' in globals() and 'GEMINI_API_KEY' in st.session_state:
        gemini_api_key = st.session_state['GEMINI_API_KEY']
    if not gemini_api_key:
        gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        gemini_api_key = "AIzaSyDAkDANkg9qFkRiSqErrFeq-TWd65vVo3w"  # Fallback to your hardcoded key

    # Check if we have valid API keys
    if not weather_api_key or not gemini_api_key:
        return "❌ API keys are missing. Please set them in the app's sidebar."

    # Normalize crop name for lookup (case-insensitive)
    crop_lower = crop.lower()
    matched_crop = None
    for crop_name in crop_conditions:
        if crop_name.lower() == crop_lower:
            matched_crop = crop_name
            break
    
    # If no exact match, try to find a similar crop
    if not matched_crop:
        for crop_name in crop_conditions:
            if crop_lower in crop_name.lower() or crop_name.lower() in crop_lower:
                matched_crop = crop_name
                break
    
    if not matched_crop:
        return f"❌ Crop '{crop}' not found in database. Available crops: {', '.join(sorted(crop_conditions.keys()))}"
    
    crop = matched_crop  # Use the matched crop name
    crop_req = crop_conditions[crop]

    # Get weather data for all locations
    all_weather_data = []
    suitable_locations = []
    
    # Build a result string to return with the analysis
    result_text = f"## Weather Analysis for {crop} Cultivation in India\n\n"
    result_text += f"### Ideal conditions for {crop}:\n"
    result_text += f"- Temperature: {crop_req['min_temp']}°C to {crop_req['max_temp']}°C\n"
    result_text += f"- Humidity: {crop_req['min_humidity']}% to {crop_req['max_humidity']}%\n\n"
    
    result_text += "### Current Weather Conditions:\n\n"
    
    for location in INDIAN_LOCATIONS:
        weather = get_weather(weather_api_key, location)
        if weather and weather["country"] == "India":  # Ensure we're only using Indian locations
            temp, humidity = weather["temperature"], weather["humidity"]
            all_weather_data.append(weather)
            
            is_suitable = (
                crop_req["min_temp"] <= temp <= crop_req["max_temp"] and
                crop_req["min_humidity"] <= humidity <= crop_req["max_humidity"]
            )
            
            # Calculate suitability score (0-100)
            temp_range = crop_req["max_temp"] - crop_req["min_temp"]
            humidity_range = crop_req["max_humidity"] - crop_req["min_humidity"]
            
            # Calculate how far the temperature is from ideal range
            if temp < crop_req["min_temp"]:
                temp_score = 100 - (((crop_req["min_temp"] - temp) / temp_range) * 100)
            elif temp > crop_req["max_temp"]:
                temp_score = 100 - (((temp - crop_req["max_temp"]) / temp_range) * 100)
            else:
                # Perfect temperature gets 100%
                ideal_temp = (crop_req["min_temp"] + crop_req["max_temp"]) / 2
                temp_deviation = abs(temp - ideal_temp)
                temp_halfrange = temp_range / 2
                temp_score = 100 - ((temp_deviation / temp_halfrange) * 50)
            
            # Calculate how far the humidity is from ideal range
            if humidity < crop_req["min_humidity"]:
                humidity_score = 100 - (((crop_req["min_humidity"] - humidity) / humidity_range) * 100)
            elif humidity > crop_req["max_humidity"]:
                humidity_score = 100 - (((humidity - crop_req["max_humidity"]) / humidity_range) * 100)
            else:
                # Perfect humidity gets 100%
                ideal_humidity = (crop_req["min_humidity"] + crop_req["max_humidity"]) / 2
                humidity_deviation = abs(humidity - ideal_humidity)
                humidity_halfrange = humidity_range / 2
                humidity_score = 100 - ((humidity_deviation / humidity_halfrange) * 50)
            
            # Overall score (temperature and humidity weighted equally)
            overall_score = (temp_score + humidity_score) / 2
            weather["suitability_score"] = overall_score
            
            if is_suitable:
                suitable_locations.append(weather)
                result_text += f"✅ **{weather['location']}, {weather['region']}**: Temp={temp}°C, Humidity={humidity}% - **Suitable** (Score: {overall_score:.1f}%)\n\n"
            else:
                result_text += f"❌ **{weather['location']}, {weather['region']}**: Temp={temp}°C, Humidity={humidity}% - **Not ideal** (Score: {overall_score:.1f}%)\n\n"

    # Sort all locations by suitability score
    all_weather_data.sort(key=lambda x: x.get("suitability_score", 0), reverse=True)
    
    # Use AI to analyze the top locations
    if all_weather_data:
        result_text += "## 🌍 AI Analysis of Suitable Regions in India:\n\n"
        
        # Use suitable locations if available, otherwise use top 5 from all data
        data_to_analyze = suitable_locations if len(suitable_locations) > 0 else all_weather_data[:5]
        
        ai_analysis = get_suitable_locations(gemini_api_key, crop, data_to_analyze, crop_req)
        result_text += ai_analysis
        return result_text
    else:
        return f"❌ No weather data could be retrieved for Indian locations. Please check your Weather API key."

# ✅ Example Usage
if __name__ == "__main__":
    crop_name = input("Enter the crop name: ")
    result = recommend_region(crop_name)
    print(result)