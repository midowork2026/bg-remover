from flask import Flask, render_template, request, send_file, redirect, url_for
import requests
import base64
import os
import io
from PIL import Image

app = Flask(__name__)

# مفتاح الـ API الخاص بك
API_KEY = os.environ.get("API_KEY", "T8PX6VMNgTofTAD72S4AZZPx")

# --- 1. مسارات الصفحات الأساسية (الواجهات) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # عند تسجيل الدخول، نوجه المستخدم للرئيسية
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # استلام بيانات التسجيل
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # تنفيذ طلبك: بعد التسجيل يتم التحويل فوراً للصفحة الرئيسية
        return redirect(url_for('index'))
    
    return render_template('register.html')

# --- 2. مسارات الأدوات الفرعية (Templates) ---

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

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# --- 3. منطق المعالجة البرمجي (Backend Logic) ---

# مسار أداة إزالة الخلفية
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return render_template('index.html', error="Please choose an image first")
    
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': file},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY}
    )
    
    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('index.html', result_image=img_base64)
    else:
        return render_template('index.html', error="API Error or Connection failed")

# مسار ضغط الصور
@app.route('/process_compress', methods=['POST'])
def process_compress():
    file = request.files.get('file')
    quality = int(request.form.get('quality', 80))
    if file:
        img = Image.open(file)
        img_io = io.BytesIO()
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        img.save(img_io, 'JPEG', quality=quality)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return render_template('compress.html', result_image=img_base64)
    return redirect(url_for('compress_page'))

# مسار تحويل الصيغ
@app.route('/process_convert', methods=['POST'])
def process_convert():
    file = request.files.get('file')
    target_format = request.form.get('format', 'PNG').upper()
    if file:
        img = Image.open(file)
        img_io = io.BytesIO()
        if target_format == "JPG":
            target_format = "JPEG"
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
        img.save(img_io, target_format)
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        return render_template('convert.html', result_image=img_base64, target_format=target_format.lower())
    return redirect(url_for('convert_page'))

# مسار دمج الصور (Background Change)
@app.route('/process_merge', methods=['POST'])
def process_merge():
    main_file = request.files.get('person_img')
    bg_file = request.files.get('bg_img')
    
    if not main_file or not bg_file:
        return render_template('merge.html', error="Please upload both person and background images")

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': main_file, 'bg_image_file': bg_file},
        data={'size': 'auto'},
        headers={'X-Api-Key': API_KEY}
    )
    
    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('merge.html', result_image=img_base64)
    return render_template('merge.html', error="Processing Error")

# تشغيل التطبيق على المنفذ المناسب للاستضافة
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
