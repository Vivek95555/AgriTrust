import google.generativeai as genai

# ✅ Replace with your valid Gemini API key
API_KEY = "AIzaSyDAkDANkg9qFkRiSqErrFeq-TWd65vVo3w"

def validate_api_key():
    """Check if the API key is working before proceeding."""
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content("Test API key")
        if response.text:
            print("✅ API Key is valid!")
            return True
    except Exception as e:
        print(f"❌ API Key Error: {e}")
        return False

def get_farmer_details(state,crop,income:float):
    """Take input manually from the user"""
    
    return fetch_recommendations({"state": state, "crop": crop, "income": income})
    

def fetch_recommendations(farmer):
    """Get precise government scheme and loan recommendations"""
    prompt = f"""
    I am a farmer from {farmer['state']} growing {farmer['crop']}. 
    My annual income is ₹{farmer['income']}.

    Suggest 2-3 **government schemes and agriculture loans** **specific** to {farmer['state']}.
    Ensure they are relevant to {farmer['crop']} and my income level.

    **Response format (short & precise)**:
    - **Scheme Name**: [Brief benefits] (Eligibility)
    - **Loan Option**: [Interest rate, subsidy, key details]
    
    Only show valid options for {farmer['state']}.
    """

    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)

    return response.text.strip()

# if validate_api_key():
#     farmer = get_farmer_details()
#     recommendations = fetch_recommendations(farmer)
#     print("\n📌 **Best Government Schemes & Loans for You:**\n")
#     print(recommendations)
# else:
#     print("❌ Invalid API key. Please check and try again.")
