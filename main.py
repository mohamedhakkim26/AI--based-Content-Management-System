from PIL import Image
import pytesseract
import re

# Configure Tesseract path (update this based on your system)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'  # macOS/Linux

def extract_text_from_image(image_path):
    """
    Extracts text from an image using Tesseract OCR.
    :param image_path: Path to the image file (e.g., 'invoice.png')
    :return: Raw extracted text
    """
    try:
        print(f"Opening image: {image_path}")
        image = Image.open(image_path)
        print("Image opened successfully.")
        
        print("Extracting text using Tesseract...")
        raw_text = pytesseract.image_to_string(image)
        
        if raw_text:
            print("Text extraction successful.")
        else:
            print("No text was extracted from the image.")
        
        return raw_text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def preprocess_text(raw_text):
    """
    Cleans and preprocesses the extracted text.
    :param raw_text: Raw text from OCR
    :return: Cleaned and preprocessed text
    """
    if not raw_text:
        return ""
    
    cleaned_text = " ".join(raw_text.split())
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s.,$€/-]', '', cleaned_text)
    
    corrections = {
        '1nv0ice': 'Invoice',
        'Am0unt': 'Amount',
        'Supp1ies': 'Supplies'
    }
    for wrong, correct in corrections.items():
        cleaned_text = cleaned_text.replace(wrong, correct)
    
    cleaned_text = re.sub(r'(\bOct\b|\bOctober\b)', '10', cleaned_text)
    cleaned_text = re.sub(r'(\bNov\b|\bNovember\b)', '11', cleaned_text)
    
    return cleaned_text

def process_document(image_path):
    """
    Extracts and preprocesses text from an image.
    :param image_path: Path to the image file (e.g., 'invoice.png')
    :return: Cleaned and preprocessed text
    """
    raw_text = extract_text_from_image(image_path)
    if raw_text:
        print("\nRaw Extracted Text:\n", raw_text)
    else:
        print("Failed to extract text from the image.")
        return None
    
    cleaned_text = preprocess_text(raw_text)
    print("\nCleaned and Preprocessed Text:\n", cleaned_text)
    
    return cleaned_text

if __name__ == "__main__":
    print("Script started.")



    image_path = r"C:\Projects\ai_cms_env\invoice.png"
    print(f"Processing image: {image_path}")
    processed_text = process_document(image_path)
    
    if processed_text:
        print("\nFinal Cleaned Text:\n", processed_text)
    else:
        print("No cleaned text to display.")