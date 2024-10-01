import streamlit as st
import anthropic
import os
from PIL import Image
import io
import base64
import json

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def analyze_document(image):
    base64_image = image_to_base64(image)
    
    prompt = """Analyze the following image and determine if it's a passport or a driver's license. 
    If it's neither, indicate that it's an unsupported document type.
    
    If it's a passport or driver's license, extract all relevant information and determine if it appears to be legitimate.
    
    For a passport, extract: full name, date of birth, passport number, issue date, expiry date, issuing country.
    For a driver's license, extract: full name, date of birth, license number, issue date, expiry date, address.
    
    Also, verify if the document appears genuine and highlight any potential discrepancies or red flags.
    
    Respond in the following JSON format:
    {
        "document_type": "passport/driver's license/unsupported",
        "extracted_info": {
            "full_name": "",
            "date_of_birth": "",
            "document_number": "",
            "issue_date": "",
            "expiry_date": "",
            "additional_info": {}
        },
        "document_validity": {
            "appears_genuine": true/false,
            "confidence_score": 0-100,
            "discrepancies": [],
            "analysis_summary": ""
        }
    }
    
    If the document type is unsupported, only fill in the "document_type" and provide a brief explanation in "analysis_summary".
    """

    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": base64_image}}
            ]}
        ]
    )
    
    return json.loads(message.content[0].text)

def main():
    st.title("Document Verification Tool")

    st.header("Upload Document")
    st.write("Supported documents: Passport or Driver's License")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Document", use_column_width=True)

        if st.button("Analyze Document"):
            with st.spinner("Analyzing document..."):
                analysis_result = analyze_document(image)
                
                if analysis_result["document_type"] == "unsupported":
                    st.error("Unsupported document type. We only process passports and driver's licenses.")
                    st.write(analysis_result["document_validity"]["analysis_summary"])
                else:
                    st.subheader(f"Document Type: {analysis_result['document_type'].title()}")
                    
                    st.subheader("Extracted Information")
                    extracted_info = analysis_result["extracted_info"]
                    for key, value in extracted_info.items():
                        if key != "additional_info":
                            st.write(f"{key.replace('_', ' ').title()}: {value}")
                    
                    st.subheader("Additional Information")
                    for key, value in extracted_info["additional_info"].items():
                        st.write(f"{key.replace('_', ' ').title()}: {value}")
                    
                    st.subheader("Document Validity")
                    validity = analysis_result["document_validity"]
                    st.write(f"Appears Genuine: {'Yes' if validity['appears_genuine'] else 'No'}")
                    st.write(f"Confidence Score: {validity['confidence_score']}%")
                    
                    if validity["discrepancies"]:
                        st.warning("Discrepancies Detected:")
                        for discrepancy in validity["discrepancies"]:
                            st.write(f"- {discrepancy}")
                    
                    st.write("Analysis Summary:")
                    st.write(validity["analysis_summary"])

if __name__ == "__main__":
    main()