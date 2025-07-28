import os
import json
import re
from dotenv import load_dotenv
from flask import Flask, request, render_template_string
import pytesseract
from PIL import Image
from openai import OpenAI

# ---------------------------------------------------------------------
# 环境准备
# ---------------------------------------------------------------------
load_dotenv()                                           # 读取 .env

DEEPSEEK_API_KEY  = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
MODEL_NAME = "deepseek-chat"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------------------------------------------------
# 载入考纲数据（Syllabus_data.json）
# ---------------------------------------------------------------------
with open("Syllabus_data.json", "r", encoding="utf-8") as f:
    SYLLABUS_DATA = json.load(f)

STOP_WORDS = {
    "the", "and", "of", "to", "a", "in", "is", "with", "for", "on",
    "an", "at", "be", "by", "or", "as", "it"
}

def tokenize(text: str):
    """取出纯字母 token，转小写，过滤停用词和1-2字母 token"""
    tokens = re.findall(r"[A-Za-z]+", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 2]

def search_syllabus(query: str, data):
    q_tokens = tokenize(query)
    hits = []
    for entry in data:
        e_tokens = tokenize(" ".join(entry["keywords"]))
        score = sum(1 for t in q_tokens if t in e_tokens)
        # 微调：二次方程、三角函数等可根据正则加额外分
        if score > 0:
            hits.append((score, entry))
    hits.sort(reverse=True, key=lambda x: x[0])
    return [h[1] for h in hits[:5]]      # 只取前 5 个最高分

# ---------------------------------------------------------------------
# Flask 模板
# ---------------------------------------------------------------------
INDEX_HTML = """
<!doctype html>
<title>Question OCR</title>
<h1>Upload Image</h1>
<form method="post" enctype="multipart/form-data" action="/upload">
  <input type="file" name="image">
  <input type="submit" value="Upload">
</form>
"""

RESULT_HTML = """
<!doctype html>
<title>OCR & DeepSeek 结果</title>

<h2>OCR 识别到的题干</h2>
<pre style="white-space: pre-wrap;">{{ ocr_text }}</pre>

<h2>DeepSeek 给出的解答与思路</h2>
<pre style="white-space: pre-wrap;">{{ deepseek_answer }}</pre>

<h2>对应考纲定位</h2>
{% if syllabus_hits %}
  <ul>
  {% for hit in syllabus_hits %}
    <li>
      <strong>{{ hit.topic }} ({{ hit.syllabus_reference }})</strong><br>
      {{ hit.book }}，{{ hit.chapter }}，pp.{{ hit.page_range }}
    </li>
  {% endfor %}
  </ul>
{% else %}
  <p>未匹配到任何考纲条目。</p>
{% endif %}
"""

# ---------------------------------------------------------------------
# Flask 应用
# ---------------------------------------------------------------------
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False    # 仅调试时需要

@app.route("/")
def index():
    return render_template_string(INDEX_HTML)

@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return "No file uploaded", 400

    file = request.files["image"]
    path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(path)

    # 1) OCR
    ocr_text = pytesseract.image_to_string(Image.open(path)).strip()

    # 2) DeepSeek
    resp = client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {"role": "system", "content": "You are an expert A‑Level tutor."},
            {"role": "user",   "content": f"请针对这道题目给出答案和详细解题思路：\n{ocr_text}"}
        ],
        stream = False
    )
    deepseek_answer = resp.choices[0].message.content.strip()

    # 3) 考纲定位
    syllabus_hits = search_syllabus(ocr_text, SYLLABUS_DATA)

    # 4) 渲染
    return render_template_string(
        RESULT_HTML,
        ocr_text = ocr_text,
        deepseek_answer = deepseek_answer,
        syllabus_hits = syllabus_hits
    )

if __name__ == "__main__":
    app.run(debug=True)        # 开发阶段开启 debug
