import json
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template_string
import pytesseract
from PIL import Image
from openai import OpenAI

load_dotenv()  # Automatically read .env before using os.getenv

RESULT_HTML = """
<!doctype html>
<title>OCR & DeepSeek 结果</title>
<h2>OCR 识别到的题干</h2>
<pre style="white-space: pre-wrap;">{{ ocr_text }}</pre>
<h2>DeepSeek 给出的解答与思路</h2>
<pre style="white-space: pre-wrap;">{{ deepseek_answer }}</pre>
"""
load_dotenv()  # Automatically read .env before using os.getenv

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # ensure JSON responses keep Unicode

# Configure DeepSeek API client
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
MODEL_NAME = "deepseek-chat"


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
    deepseek_answer = resp.choices[0].message.content.strip()

    return render_template_string(
        RESULT_HTML,
        ocr_text=text.strip(),
        deepseek_answer=deepseek_answer
    )
    return jsonify({
        'ocr_text': text.strip(),
        'deepseek_answer': deepseek_answer
    ai_answer = resp.choices[0].message.content.strip()

    # Search dataset for an example match
    match = search_dataset(text)

    return jsonify({
        'ocr_text': text.strip(),
        'ai_answer': ai_answer,
        'match': match
    })



if __name__ == '__main__':
    app.run(debug=True)
