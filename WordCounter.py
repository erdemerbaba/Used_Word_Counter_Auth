import os
import PyPDF2
from collections import Counter
import string
from functools import wraps

# Authentication
AUTH_TOKEN = "your_secure_token"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = input("Enter authentication token: ")
        if token != AUTH_TOKEN:
            print("Invalid token! Authentication failed.")
            return
        return f(*args, **kwargs)
    return decorated

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''.join([page.extract_text() for page in reader.pages])
        return text
    except FileNotFoundError:
        print(f"Error: {pdf_path} not found.")
        return ""
    except Exception as e:
        print(f"An error occurred while reading {pdf_path}: {str(e)}")
        return ""

# Get the most common words
def get_most_common_words(text, num_words=15):
    translator = str.maketrans('', '', string.punctuation)
    cleaned_text = text.translate(translator).lower()
    words = cleaned_text.split()
    filtered_words = [word for word in words if len(word) >= 5]
    counter = Counter(filtered_words)
    return counter.most_common(num_words)

# Analyze PDFs with authentication
@token_required
def analyze_pdfs(pdf_paths):
    results = {}
    for pdf_path in pdf_paths:
        text = extract_text_from_pdf(pdf_path)
        if text:
            most_common_words = get_most_common_words(text)
            results[pdf_path] = most_common_words
    return results

# Generate PDF filenames
def generate_pdf_filenames(start, end, template='{:03}.pdf'):
    return [template.format(i) for i in range(start, end + 1)]

# Main function
def main():
    pdf_files = generate_pdf_filenames(1, 2)
    analysis_results = analyze_pdfs(pdf_files)
    for pdf, words in analysis_results.items():
        print(f"Top 15 words in {pdf}: {words}\n")

if __name__ == "__main__":
    main()
