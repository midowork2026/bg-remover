from flask import Flask, render_template, request, send_file
import requests
import base64
import os
import io
from PIL import Image # مكتبة معالجة الصور للضغط والتحويل

app = Flask(__name__)

API_KEY = "T8PX6VMNgTofTAD72S4AZZPx"

@app.route('/')
def index():
    return render_template('index.html')

# --- مسارات عرض الصفحات ---
@app.route('/crop')
def crop_page():
    return render_template('crop.html')

@app.route('/compress')
def compress_page():
    return render_template('compress.html')

@app.route('/convert')
def convert_page():
    return render_template('convert.html')

@app.route('/merge')
def merge_page():
    return render_template('merge.html')

# --- تنفيذ الأوامر (المنطق البرمجي) ---

# 1. إزالة الخلفية
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file: return "Select Image First"
    response = requests.post('https://api.remove.bg/v1.0/removebg',
        files={'image_file': file}, data={'size': 'auto'}, headers={'X-Api-Key': API_KEY})
    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('index.html', result_image=img_base64)
    return "Error in API"

# 2. تنفيذ الضغط (Compress)
@app.route('/process_compress', methods=['POST'])
def process_compress():
    file = request.files.get('file')
    quality = int(request.form.get('quality', 80))
    if file:
        img = Image.open(file)
        img_io = io.BytesIO()
        # تحويل لـ RGB لو كانت PNG عشان نعرف نضغطها JPG
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.save(img_io, 'JPEG', quality=quality)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return render_template('compress.html', result_image=img_base64)
    return "Error"

# 3. تنفيذ التحويل (Convert)
@app.route('/process_convert', methods=['POST'])
def process_convert():
    file = request.files.get('file')
    target_format = request.form.get('format', 'PNG').upper()
    if file:
        img = Image.open(file)
        img_io = io.BytesIO()
        if target_format == "JPG":
            target_format = "JPEG"
            if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.save(img_io, target_format)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return render_template('convert.html', result_image=img_base64)
    return "Error"

# 4. تنفيذ الدمج (Merge)
@app.route('/process_merge', methods=['POST'])
def process_merge():
    main_file = request.files.get('person_img')
    bg_file = request.files.get('bg_img')
    response = requests.post('https://api.remove.bg/v1.0/removebg',
        files={'image_file': main_file, 'bg_image_file': bg_file},
        data={'size': 'auto'}, headers={'X-Api-Key': API_KEY})
    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('merge.html', result_image=img_base64)
    return "Merge Error"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
