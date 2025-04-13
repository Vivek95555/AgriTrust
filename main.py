import streamlit as st
import io
import os
from crop_grow_recom import recommend_region
from wheather_pre_by_city import wheather_pred_by_city
from soil_health import soil_health_analysis
from scheme_loan import get_farmer_details
from scheme_loan_guj import get_farmer_details_guj
from soil_report_analysis import analyze_soil_report

st.set_page_config(page_title="Crop Suitability & Loan Recommender", layout="wide")

st.sidebar.title("🌱 Select a Feature")
option = st.sidebar.radio("Choose a model:", [
    "Crop Growth Region Recommendation",
    "Weather Prediction by City",
    "Soil Health Analysis",
    "Soil Report PDF Analysis",
    "Crop Loan & Government Scheme Recommender (English)",
    "Crop Loan & Government Scheme Recommender (Gujarati)"
])

if option == "Crop Growth Region Recommendation":
    st.title("🌾 Crop Growth Region Recommendation")
    crop = st.text_input("Enter crop name")
    if st.button("Recommend Region"):
        region = recommend_region(crop)
        st.success(f"🌍 Recommended Region: {region}")

elif option == "Weather Prediction by City":
    st.title("☁️ Weather Prediction by City")
    city = st.text_input("Enter city name")
    if st.button("Predict Weather"):
        weather = wheather_pred_by_city(city)
        st.success(f"🌦️ Weather Forecast: {weather}")

elif option == "Soil Health Analysis":
    st.title("🌱 Soil Health Analysis")
    uploaded_file = st.file_uploader("Upload soil image", type=["jpeg", "jpg", "png"])
    manual_location = st.text_input("Enter location")
    crop_type = st.text_input("Enter crop type")
    soil_analysis_needed = st.radio("Perform Soil Analysis?", ["yes", "no"], index=0)
    if uploaded_file and st.button("Analyze Soil"):
        soil_result = soil_health_analysis(uploaded_file, manual_location, soil_analysis_needed, crop_type)
        if isinstance(soil_result, tuple):
            st.subheader("🔍 Soil Health Analysis Result:")
            st.write(f"{soil_result[0]}")
        else:
            st.success(f"Analysis Result: {soil_result}")

# PDF analysis section with Gemini integration
elif option == "Soil Report PDF Analysis":
    st.title("📄 Soil Report PDF Analysis")
    st.write("Upload a soil analysis report PDF to get crop recommendations and insights.")
    
    uploaded_pdf = st.file_uploader("Upload Soil Analysis PDF", type=["pdf"], key="soil_pdf_uploader")
    
    if uploaded_pdf is not None and st.button("Analyze Report"):
        with st.spinner("Processing soil report..."):
            try:
                # Get the PDF content as bytes and create BytesIO object
                pdf_bytes = uploaded_pdf.getvalue()
                pdf_io = io.BytesIO(pdf_bytes)
                
                # Pass BytesIO object to the analysis function
                result = analyze_soil_report(pdf_io)
                
                if isinstance(result, tuple):
                    soil_text, recommendations = result
                    
                    # Show extracted text in an expandable section
                    with st.expander("View Extracted Text"):
                        st.text_area("Soil Report Text", soil_text, height=200)
                    
                    # Display recommendations
                    st.subheader("🌿 Crop Recommendations & Insights")
                    st.markdown(recommendations)
                    
                    # Add download button
                    st.download_button(
                        "Download Recommendations",
                        recommendations,
                        file_name="crop_recommendations.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(result)
            except Exception as e:
                st.error(f"Error processing PDF: {str(e)}")
    else:
        st.info("Please upload a soil analysis PDF report to get started.")

elif option == "Crop Loan & Government Scheme Recommender (English)":
    st.title("💰 Crop Loan & Government Scheme Recommender")
    state = st.text_input("Enter state")
    crop_loan_type = st.text_input("Enter crop type for loan")
    loan_amount = st.number_input("Enter loan amount", min_value=1000, value=100000)
    if st.button("Get Loan & Scheme Details"):
        loan_details = get_farmer_details(state, crop_loan_type, loan_amount)
        st.success(f"📜 Loan & Scheme Details: {loan_details}")

elif option == "Crop Loan & Government Scheme Recommender (Gujarati)":
    st.title("💰 Crop Loan & Government Scheme Recommender (Gujarati)")
    state = st.text_input("Enter state")
    crop_loan_type = st.text_input("Enter crop type for loan", "Wheat")
    loan_amount = st.number_input("Enter loan amount", min_value=1000, value=100000)
    if st.button("Get Loan & Scheme Details (Gujarati)"):
        loan_details_guj = get_farmer_details_guj(state, crop_loan_type, loan_amount)
        st.success(f"📜 લોન અને યોજના વિગતો: {loan_details_guj}")