import json
import os
from flask import Flask, request, jsonify, render_template_string
import pytesseract
from PIL import Image

app = Flask(__name__)

# Load example dataset
with open('sample_dataset.json', 'r') as f:
    DATASET = json.load(f)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

INDEX_HTML = """
<!doctype html>
<title>Question OCR</title>
<h1>Upload Image</h1>
<form method=post enctype=multipart/form-data action="/upload">
  <input type=file name=image>
  <input type=submit value=Upload>
</form>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Perform OCR
    text = pytesseract.image_to_string(Image.open(filepath))

    # Search dataset for an example match
    match = search_dataset(text)

    return jsonify({
        'ocr_text': text.strip(),
        'match': match
    })


def search_dataset(text):
    text_lower = text.lower()
    for item in DATASET:
        if item['question'].lower() in text_lower:
            return item
    return {'message': 'No match found in dataset'}


if __name__ == '__main__':
    app.run(debug=True)
