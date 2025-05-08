
from flask import Flask, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from flask_cors import CORS
from pdf2image import convert_from_bytes
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "PDF Toolkit API is running."

@app.route('/jpg-to-pdf', methods=['POST'])
def jpg_to_pdf():
    file = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    from PIL import Image
    image = Image.open(image_path).convert('RGB')
    output_path = os.path.join(OUTPUT_FOLDER, 'output.pdf')
    image.save(output_path)
    return send_file(output_path, as_attachment=True)

@app.route('/compress-pdf', methods=['POST'])
def compress_pdf():
    file = request.files['pdf']
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    output_path = os.path.join(OUTPUT_FOLDER, 'compressed.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

@app.route('/pdf-to-word', methods=['POST'])
def pdf_to_word():
    file = request.files['pdf']
    reader = PdfReader(file)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    output_path = os.path.join(OUTPUT_FOLDER, 'output.txt')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    return send_file(output_path, as_attachment=True)

@app.route('/merge-pdf', methods=['POST'])
def merge_pdf():
    files = request.files.getlist('pdfs')
    writer = PdfWriter()
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)
    output_path = os.path.join(OUTPUT_FOLDER, 'merged.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

@app.route('/split-pdf', methods=['POST'])
def split_pdf():
    file = request.files['pdf']
    reader = PdfReader(file)
    writer = PdfWriter()
    writer.add_page(reader.pages[0])
    output_path = os.path.join(OUTPUT_FOLDER, 'split.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

@app.route('/pdf-to-jpg', methods=['POST'])
def pdf_to_jpg():
    file = request.files['pdf']
    images = convert_from_bytes(file.read(), first_page=1, last_page=1)
    output_image = os.path.join(OUTPUT_FOLDER, 'converted.jpg')
    images[0].save(output_image, 'JPEG')
    return send_file(output_image, as_attachment=True)

@app.route('/rotate-pdf', methods=['POST'])
def rotate_pdf():
    file = request.files['pdf']
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate(90)
        writer.add_page(page)
    output_path = os.path.join(OUTPUT_FOLDER, 'rotated.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

@app.route('/delete-page-pdf', methods=['POST'])
def delete_page_pdf():
    file = request.files['pdf']
    reader = PdfReader(file)
    writer = PdfWriter()
    for i in range(1, len(reader.pages)):
        writer.add_page(reader.pages[i])
    output_path = os.path.join(OUTPUT_FOLDER, 'deleted.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

@app.route('/watermark-pdf', methods=['POST'])
def watermark_pdf():
    file = request.files['pdf']
    watermark_text = request.form.get('text', 'WATERMARK')
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        page.add_annotation({
            "/Type": "/Annot",
            "/Subtype": "/Text",
            "/Contents": watermark_text,
            "/Rect": [100, 100, 200, 200]
        })
        writer.add_page(page)
    output_path = os.path.join(OUTPUT_FOLDER, 'watermarked.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

@app.route('/flatten-pdf', methods=['POST'])
def flatten_pdf():
    file = request.files['pdf']
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    output_path = os.path.join(OUTPUT_FOLDER, 'flattened.pdf')
    with open(output_path, 'wb') as f:
        writer.write(f)
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
