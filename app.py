from flask import Flask, render_template, request, send_file
import requests
import base64
import os
import io
from PIL import Image

app = Flask(__name__)

# 🔥 API KEY الخاص بك
API_KEY = "T8PX6VMNgTofTAD72S4AZZPx"

# 1. الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# 2. صفحة القص (Crop)
@app.route('/crop')
def crop_page():
    return render_template('crop.html')

# 3. صفحة الضغط (Compress)
@app.route('/compress')
def compress_page():
    return render_template('compress.html')

# 4. صفحة التحويل (Convert)
@app.route('/convert')
def convert_page():
    return render_template('convert.html')

# 5. صفحة الدمج (Merge)
@app.route('/merge')
def merge_page():
    return render_template('merge.html')

# 6. صفحة سياسة الخصوصية (Privacy) - اللي كانت ناقصة
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# 7. صفحة اتصل بنا (Contact) - اللي كانت ناقصة
@app.route('/contact')
def contact():
    return render_template('contact.html')

# --- العمليات البرمجية (Logic) ---

# تنفيذ إزالة الخلفية
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file: return render_template('index.html', error="برجاء اختيار صورة")
    response = requests.post('https://api.remove.bg/v1.0/removebg',
        files={'image_file': file}, data={'size': 'auto'}, headers={'X-Api-Key': API_KEY})
    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('index.html', result_image=img_base64)
    return render_template('index.html', error="خطأ في السيرفر")

# تنفيذ الضغط
@app.route('/process_compress', methods=['POST'])
def process_compress():
    file = request.files.get('file')
    quality = int(request.form.get('quality', 80))
    if file:
        img = Image.open(file)
        img_io = io.BytesIO()
        if img.mode in ("RGBA", "P"): img = img.convert("RGB")
        img.save(img_io, 'JPEG', quality=quality)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return render_template('compress.html', result_image=img_base64)
    return "Error"

# تنفيذ التحويل
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
        return render_template('convert.html', result_image=img_base64, target_format=target_format.lower())
    return "Error"

# تنفيذ الدمج
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
