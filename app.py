from flask import Flask, render_template, request, send_file, redirect, url_for, session
import requests
import base64
import os
import io
from PIL import Image

app = Flask(__name__)
# مفتاح سري لتفعيل خاصية الـ Session (ضروري جداً)
app.secret_key = 'hamouzi_secret_key_2026'

API_KEY = os.environ.get("API_KEY", "T8PX6VMNgTofTAD72S4AZZPx")

@app.route('/')
def index():
    # بنبعت الإيميل للصفحة عشان لو موجود تظهر الأيقونة
    user_email = session.get('user_email')
    return render_template('index.html', user_email=user_email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        # بنخزن الإيميل في السشن عشان الموقع يعرف إنك سجلت
        session['user_email'] = email
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        # بنخزن الإيميل فوراً بعد التسجيل
        session['user_email'] = email
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    # حذف بيانات المستخدم لتسجيل الخروج
    session.pop('user_email', None)
    return redirect(url_for('index'))

# --- باقي المسارات كما هي بدون أي تغيير ---
@app.route('/crop')
def crop_page(): return render_template('crop.html')
@app.route('/compress')
def compress_page(): return render_template('compress.html')
@app.route('/convert')
def convert_page(): return render_template('convert.html')
@app.route('/merge')
def merge_page(): return render_template('merge.html')
@app.route('/privacy')
def privacy(): return render_template('privacy.html')
@app.route('/contact')
def contact(): return render_template('contact.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file: return render_template('index.html', error="Please choose an image first", user_email=session.get('user_email'))
    response = requests.post('https://api.remove.bg/v1.0/removebg', files={'image_file': file}, data={'size': 'auto'}, headers={'X-Api-Key': API_KEY})
    if response.status_code == 200:
        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('index.html', result_image=img_base64, user_email=session.get('user_email'))
    return render_template('index.html', error="API Error", user_email=session.get('user_email'))

# تشغيل التطبيق
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
