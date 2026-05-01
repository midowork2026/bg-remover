import ssl, os, base64, io
from flask import Flask, render_template, request
from transparent_background import Remover
from PIL import Image

ssl._create_default_https_context = ssl._create_unverified_context
app = Flask(__name__)
remover = Remover()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file: return "ارفع صورة!"
    input_image = Image.open(file.stream).convert('RGB')
    output_image = remover.process(input_image)
    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return render_template('index.html', result_image=img_base64)

if __name__ == '__main__':
    return render_template('index.html', result_image=img_base64)
