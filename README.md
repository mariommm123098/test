# OCR Question Lookup Demo

This is a minimal Flask web application that demonstrates how to upload an image,
run OCR on it, and look up a matching question in a small sample dataset.

## Setup

Install system dependencies (Tesseract OCR):

```bash
sudo apt-get update && sudo apt-get install -y tesseract-ocr
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

```bash
python app.py
```

Navigate to `http://localhost:5000` in your browser and upload an image of a question.
The server will perform OCR and try to match the question text in `sample_dataset.json`.

This is a small proof-of-concept to illustrate how a full question search system
might be implemented.
