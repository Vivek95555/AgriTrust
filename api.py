from flask import Flask, request, jsonify
from crop_grow_recom import recommend_region
from wheather_pre_by_city import wheather_pred_by_city
from soil_health import soil_health_analysis
from scheme_loan import get_farmer_details
from scheme_loan_guj import get_farmer_details_guj

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Crop Suitability & Loan Recommender API"})

@app.route('/recommend_region', methods=['POST'])
def recommend_region_api():
    data = request.get_json()
    crop = data.get("crop")
    region = recommend_region(crop)
    return jsonify({"recommended_region": region})

@app.route('/predict_weather', methods=['POST'])
def predict_weather_api():
    data = request.get_json()
    city = data.get("city")
    weather = wheather_pred_by_city(city)
    return jsonify({"weather_forecast": weather})

@app.route('/soil_health_analysis', methods=['POST'])
def soil_health_analysis_api():
    file = request.files.get("soil_image")
    manual_location = request.form.get("location", "Nadiad")
    crop_type = request.form.get("crop_type", "Wheat")
    soil_analysis_needed = request.form.get("soil_analysis_needed", "yes")
    
    if file:
        soil_result = soil_health_analysis(file, manual_location, soil_analysis_needed, crop_type)
        return jsonify({"soil_health_analysis": soil_result})
    else:
        return jsonify({"error": "No soil image uploaded"}), 400

@app.route('/get_loan_details', methods=['POST'])
def get_loan_details_api():
    data = request.get_json()
    state = data.get("state", "Gujarat")
    crop_loan_type = data.get("crop_loan_type", "Wheat")
    loan_amount = data.get("loan_amount", 100000)
    loan_details = get_farmer_details(state, crop_loan_type, loan_amount)
    return jsonify({"loan_details": loan_details})

@app.route('/get_loan_details_guj', methods=['POST'])
def get_loan_details_guj_api():
    data = request.get_json()
    state = data.get("state", "Gujarat")
    crop_loan_type = data.get("crop_loan_type", "Wheat")
    loan_amount = data.get("loan_amount", 100000)
    loan_details_guj = get_farmer_details_guj(state, crop_loan_type, loan_amount)
    return jsonify({"loan_details_guj": loan_details_guj})

if __name__ == '__main__':
    app.run(debug=True)
