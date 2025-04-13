import google.generativeai as genai

# ✅ Replace with your valid Gemini API key
API_KEY = "AIzaSyDAkDANkg9qFkRiSqErrFeq-TWd65vVo3w"

def validate_api_key():
    """Check if the API key is working before proceeding."""
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro")
        test_prompt = "Say 'Hello' in Gujarati."
        response = model.generate_content(test_prompt)
        if response.text:
            print("✅ API Key is valid!")
            return True
    except Exception as e:
        print(f"❌ API Key Error: {e}")
        return False

def get_farmer_details_guj(state,crop,income):
   
    return fetch_recommendations({"state": state, "crop": crop, "income": income})

def fetch_recommendations(farmer):
    """Ask Gemini to recommend schemes & loans specific to the state, crop, and income"""
    prompt = f"""
    હું {farmer['state']} રાજ્યનો ખેડૂત છું અને {farmer['crop']} પાક ઉગાઉં છું.
    મારી વાર્ષિક આવક ₹{farmer['income']} છે.
    
    કૃપા કરીને **ગુજરાતી ભાષામાં** {farmer['state']} રાજ્ય માટે શ્રેષ્ઠ 2-3 સરકારી યોજનાઓ અને કૃષિ લોનની માહિતી આપો,
    જે ખાસ કરીને {farmer['crop']} માટે લાભપ્રદ હોય. 
        
    શરતો:  
    1️⃣ માત્ર {farmer['state']} માટે માન્ય યોજનાઓ આપો.  
    2️⃣ કૃપા કરીને **ટૂંકા અને સ્પષ્ટ જવાબો** આપો.  
    3️⃣ જો કોઈ ખાસ યોજના ન હોય, તો **વિશેષ માહિતી આપો**.  
      
    📌 આ માહિતી ગુજરાતીમાં હોવી જોઈએ!
    """
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    
    return response.text


