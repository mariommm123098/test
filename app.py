import json
import os
from flask import Flask, request, jsonify, render_template_string
import pytesseract
from PIL import Image
from openai import OpenAI

app = Flask(__name__)

# Configure DeepSeek API client
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
MODEL_NAME = "deepseek-chat"

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

    # Call DeepSeek for an AI-generated solution
    messages = [
        {"role": "system", "content": "You are an expert A-Level tutor."},
        {"role": "user", "content": f"请针对这道题目给出答案和详细解题思路：\n{text}"}
    ]
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        stream=False
    )
    ai_answer = resp.choices[0].message.content.strip()

    # Search dataset for an example match
    match = search_dataset(text)

    return jsonify({
        'ocr_text': text.strip(),
        'ai_answer': ai_answer,
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
