from flask import Flask, request, jsonify
import os
import PyPDF2

app = Flask(__name__)

def check_api_key(request):
    api_key = request.headers.get('X-API-KEY')
    correct_key = os.environ.get('API_KEY')
    return api_key == correct_key

@app.route('/extract_text', methods=['POST'])
@check_api_key  # Ensure API key is valid
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    try:
        if file.filename.lower().endswith(('.pdf', '.txt')):
            text = extract_text_from_file(file)
            return jsonify({'text': text})
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def extract_text_from_file(file):
    if file.filename.lower().endswith('.pdf'):
        with open(file, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = '\n'.join(page.extract_text() for page in pdf_reader.pages)
    else:  # Assuming text file
        with open(file, 'r') as text_file:
            text = text_file.read()
    return text

if __name__ == '__main__':
    app.run(debug=True)  # Debug mode for easier testing
