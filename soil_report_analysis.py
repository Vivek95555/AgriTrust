import PyPDF2
import io
import os
import google.generativeai as genai

# Set up Gemini API key - hardcoded for this example
# In production, use environment variables or a safer method
API_KEY = "AIzaSyDAkDANkg9qFkRiSqErrFeq-TWd65vVo3w"
genai.configure(api_key=API_KEY)

def analyze_soil_report(pdf_file):
    """
    Analyze a soil report PDF and provide crop recommendations using Gemini API.
    
    Args:
        pdf_file: A BytesIO object containing the PDF file data
    
    Returns:
        tuple: (extracted_text, recommendations) or error message string
    """
    try:
        # Extract text directly from BytesIO object
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        # Extract text from each page
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        
        if not text.strip():
            return "Could not extract text from the PDF. It might be scanned or protected."
        
        # Use Gemini to analyze the soil report
        model = genai.GenerativeModel('models/gemini-1.5-pro')
        
        prompt = f"""You are a soil and agriculture expert. Analyze the following soil report and provide detailed 
        crop recommendations based on the soil properties. Include information about suitable crops, 
        recommended fertilizers, and any soil amendments needed.
        
        Soil report:
        {text}
        """
        
        response = model.generate_content(prompt)
        recommendations = response.text
        
        # Return both the extracted text and recommendations
        return (text, recommendations)
        
    except PyPDF2.errors.PdfReadError:
        return "The PDF file is damaged or cannot be read. Please upload a valid PDF."
    except Exception as e:
        return f"Error analyzing the soil report: {str(e)}"