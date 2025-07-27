import os
from dotenv import load_dotenv
from flask import Flask, request, render_template_string
import pytesseract
from PIL import Image
from openai import OpenAI

# 自动加载根目录下的 .env
load_dotenv()

# 结果页面模板
RESULT_HTML = """
<!doctype html>
<title>OCR & DeepSeek 结果</title>
<h2>OCR 识别到的题干</h2>
<pre style="white-space: pre-wrap;">{{ ocr_text }}</pre>
<h2>DeepSeek 给出的解答与思路</h2>
<pre style="white-space: pre-wrap;">{{ deepseek_answer }}</pre>
"""

# 上传表单页面
INDEX_HTML = """
<!doctype html>
<title>Question OCR</title>
<h1>Upload Image</h1>
<form method="post" enctype="multipart/form-data" action="/upload">
  <input type="file" name="image">
  <input type="submit" value="Upload">
</form>
"""

app = Flask(__name__)
# 保证 JSON 响应可以返回 Unicode（调试时留用，渲染模板不会受影响）
app.config['JSON_AS_ASCII'] = False

# 配置 DeepSeek / OpenAI 客户端
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
MODEL_NAME = "deepseek-chat"

# 上传文件夹
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "No file uploaded", 400

    file = request.files['image']
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # OCR 提取
    text = pytesseract.image_to_string(Image.open(filepath)).strip()

    # 调用 DeepSeek / OpenAI 生成解答
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are an expert A-Level tutor."},
            {"role": "user", "content": f"请针对这道题目给出答案和详细解题思路：\n{text}"}
        ],
        stream=False
    )
    deepseek_answer = resp.choices[0].message.content.strip()

    # 渲染结果页面
    return render_template_string(
        RESULT_HTML,
        ocr_text=text,
        deepseek_answer=deepseek_answer
    )

if __name__ == '__main__':
    # debug=True 开发时可见错误详情，生产环境请关掉
    app.run(debug=True)
