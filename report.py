import pymupdf   # PyMuPDF for reading PDFs
import google.generativeai as genai

# Set up Gemini API
GEMINI_API_KEY = "AIzaSyDAkDANkg9qFkRiSqErrFeq-TWd65vVo3w"
genai.configure(api_key=GEMINI_API_KEY)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file."""
    try:
        doc = pymupdf.open(pdf_path)  # Open PDF
        text = "\n".join(page.get_text() for page in doc)  # Extract text from all pages
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {e}"

def get_crop_recommendations(soil_report_text):
    """Send soil report to Gemini AI and get crop recommendations."""
    try:
        prompt = f"""
        Given the following soil analysis report, recommend the most suitable crops and provide key insights.
        Include soil health details, best crop choices, and farming tips.

        Soil Report:
        {soil_report_text}
        """

        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        
        return response.text.strip() if response.text else "No response from AI."
    except Exception as e:
        return f"Error fetching recommendations: {e}"

# --- Main Execution ---
pdf_path = "art-5807.pdf"  # Replace with your actual PDF file
soil_text = extract_text_from_pdf(pdf_path)

if soil_text:
    # print("\nExtracted Soil Report Text:\n", soil_text[:500])  # Show first 500 chars for preview
    recommendations = get_crop_recommendations(soil_text)
    print("\nCrop Recommendations & Insights:\n", recommendations)
else:
    print("Failed to extract text from PDF.")
