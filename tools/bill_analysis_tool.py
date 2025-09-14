import base64
import os
from mistralai import Mistral


def encode_pdf(pdf_path):
    """Encode the pdf to base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def make_better_url(pdf_path):
    return pdf_path.replace("\\", "/")


def extract_bill_data(ocr_text):
    """Extract key data points from OCR text with validation."""

    # Simple extraction patterns
    data = {}

    lines = ocr_text.split('\n')
    for line in lines:
        line = line.strip()

        # Extract total amount
        if 'ΠΟΣΟ ΠΛΗΡΩΜΗΣ' in line or 'Συνολικό ποσό' in line:
            # Look for euro amounts
            for i, l in enumerate(lines[max(0, lines.index(line) - 2):lines.index(line) + 3]):
                if '€' in l:
                    data['total_amount'] = l.strip()
                    break

        # Extract consumption
        if 'kWh' in line and any(char.isdigit() for char in line):
            data['consumption'] = line.strip()

        # Extract billing period
        if '/' in line and len(line.split('/')) >= 3:  # Date format
            if 'περίοδος' in line.lower() or 'period' in line.lower():
                data['billing_period'] = line.strip()

    return data


# Path to pdf
pdf_path = "C:\\Users\\johnb\\Downloads\\getbill.pdf"
pdf_path = make_better_url(pdf_path)

# Getting the base64 string
base64_pdf = encode_pdf(pdf_path)

if base64_pdf:
    api_key = os.environ["MISTRAL_API_KEY"]
    client = Mistral(api_key=api_key)

    # OCR extraction only
    ocr_response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "document_url",
            "document_url": f"data:application/pdf;base64,{base64_pdf}"
        },
        include_image_base64=False
    )

    # Extract structured data from OCR
    extracted_data = extract_bill_data(str(ocr_response))

    # Focused analysis prompt
    system_prompt = f"""
    Analyze this Greek electricity bill data extracted via OCR. Focus only on factual information present in the text.

    OCR Text: {ocr_response}

    Extracted Key Data: {extracted_data}

    Provide a detailed analysis with:
    1. Bill summary (amount, consumption, period)
    2. Notable charges or fees
    3. Any obvious anomalies
    4. Anything else that you think are important. Make sure that the infos that you give are spotless

    IMPORTANT: Only state facts clearly visible in the text. If information is unclear or missing, say so explicitly. Do not estimate or assume values.
    """


    chat_response = client.chat.complete(
        model="ministral-8b-2410",
        messages=[{"role": "user", "content": system_prompt}],
        temperature=0.1
    )

    print("\n=== LLM ANALYSIS ===")
    print(chat_response.choices[0].message.content)

