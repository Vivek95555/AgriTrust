import google.generativeai as genai
import os
import requests
from PIL import Image
from datetime import datetime

# Configure Gemini API
api_key = "AIzaSyDAkDANkg9qFkRiSqErrFeq-TWd65vVo3w"  # Replace with your actual API key
genai.configure(api_key=api_key)

# Weather API configuration
weather_api_key = "68ceae54736449fe90542050251903"  # Replace with your weather API key
weather_base_url = "https://api.weatherapi.com/v1/current.json"  # Adjust if using a different weather API


def get_weather_data(location):
    """Fetch weather data for a specific location"""
    try:
        params = {
            "key": weather_api_key,
            "q": location,
            "aqi": "yes",  # Include air quality data if available
        }

        response = requests.get(weather_base_url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error fetching weather data: {str(e)}"


def format_weather_for_analysis(weather_data):
    """Format weather data for soil health analysis"""
    try:
        # Extract relevant weather information
        current = weather_data.get("current", {})
        location = weather_data.get("location", {})

        formatted_data = {
            "temperature": current.get("temp_c"),
            "humidity": current.get("humidity"),
            "precipitation": current.get("precip_mm"),
            "wind_speed": current.get("wind_kph"),
            "uv_index": current.get("uv"),
            "location": f"{location.get('name')}, {location.get('region')}, {location.get('country')}",
            "last_updated": current.get("last_updated"),
        }

        return formatted_data
    except Exception as e:
        return f"Error formatting weather data: {str(e)}"


def analyze_soil_health(image_path, weather_data):
    """Analyze soil health based on image and weather data"""
    try:
        image = Image.open(image_path)

        # Format weather data for the prompt
        weather_str = "\n".join(
            [f"{key}: {value}" for key, value in weather_data.items()]
        )

        prompt = f"""
        Provide a comprehensive soil health analysis based on this soil image and the following weather data:

        Weather Data:
        {weather_str}

        For the soil image, please analyze and provide:
        1. Soil type classification (sandy, clay, loam, etc.)
        2. Color analysis and what it indicates about soil health
        3. Visible organic matter assessment
        4. Signs of soil structure and aggregation
        5. Any visible issues (compaction, erosion, crusting, waterlogging)
        6. Overall soil health score (0-100) based on visible characteristics
        7. Three specific recommendations to improve soil health
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([prompt, image])

        return response.text
    except Exception as e:
        return f"Error analyzing soil health: {str(e)}"


def recommend_yield_improvements(soil_analysis, crop_type, weather_data):
    """Generate recommendations to improve crop yield based on soil and weather"""
    try:
        # Format weather data for the prompt
        weather_str = "\n".join(
            [f"{key}: {value}" for key, value in weather_data.items()]
        )

        prompt = f"""
        Based on the following soil analysis, weather data, and crop type, provide detailed recommendations to maximize crop yield:

        Crop Type: {crop_type}

        Weather Data:
        {weather_str}

        Soil Analysis:
        {soil_analysis}

        Please provide:
        1. Five specific, actionable recommendations for improving yield of {crop_type} in these conditions
        2. Optimal irrigation strategy considering the soil type and weather
        3. Fertilization recommendations (timing and approach)
        4. Pest and disease management strategies specific to this crop and conditions
        5. Harvest timing optimization for maximum yield

        For each recommendation, include expected impact on yield (low, medium, high) and implementation difficulty (easy, moderate, difficult).
        """

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        return f"Error generating yield improvement recommendations: {str(e)}"


def track_soil_health(image_path, location, crop_type=None, save_history=True):
    """Track soil health over time and provide yield improvement recommendations"""
    # Get current weather data
    weather_raw = get_weather_data(location)

    if isinstance(weather_raw, str) and weather_raw.startswith("Error"):
        return weather_raw, None

    weather_formatted = format_weather_for_analysis(weather_raw)

    # Analyze soil health
    soil_analysis = analyze_soil_health(image_path, weather_formatted)

    # Generate yield improvement recommendations if crop type is provided
    yield_recommendations = None
    if crop_type:
        yield_recommendations = recommend_yield_improvements(
            soil_analysis, crop_type, weather_formatted
        )

    # Save to history if requested
    if save_history:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_file = f"soil_health_history_{timestamp}.txt"

        with open(history_file, "w") as f:
            f.write(
                f"Soil Health Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )
            f.write(f"Location: {weather_formatted.get('location', 'Unknown')}\n")
            f.write(
                f"Weather Conditions: {weather_formatted.get('temperature')}°C, {weather_formatted.get('humidity')}% humidity\n\n"
            )
            f.write(soil_analysis)

            if yield_recommendations:
                f.write(
                    f"\n\n=== YIELD IMPROVEMENT RECOMMENDATIONS FOR {crop_type.upper()} ===\n\n"
                )
                f.write(yield_recommendations)

    return soil_analysis, yield_recommendations


# Main execution
def soil_health_analysis(image_path, location, wants_yield_recs,crop_type):

    # Ask if user wants crop yield recommendations
    wants_yield_recs = wants_yield_recs.lower().strip()

    crop_type = None
    # if wants_yield_recs in ["yes", "y", "true", "1"]:
    #     crop_type = input("\nEnter crop type (e.g., 'wheat', 'corn', 'rice'): ")

    print("\nAnalyzing soil and generating recommendations...")
    soil_health_analysis, yield_recommendations = track_soil_health(
        image_path, location, crop_type
    )

    print("\n=== SOIL HEALTH ANALYSIS ===")
    return soil_health_analysis, yield_recommendations
    # print(soil_health_analysis)

    # if yield_recommendations:
    #     print(f"\n=== YIELD IMPROVEMENT RECOMMENDATIONS FOR {crop_type.upper()} ===")
    #     print(yield_recommendations)
