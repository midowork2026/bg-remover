from flask import Flask, render_template, request, send_file, redirect, url_for, session, send_from_directory
import requests
import base64
import os
import io
from PIL import Image

app = Flask(__name__)

# مفتاح سري لتفعيل خاصية الـ Session (ضروري جداً)
app.secret_key = 'hamouzi_secret_key_2026'

# إعدادات الـ API Key الخاص بإزالة الخلفية
# ملحوظة: اتأكد إن الـ API_KEY شغال ومسجل في حسابك
API_KEY = os.environ.get("API_KEY", "T8PX6VNNgTofTAD72S4AZZPx")

# --- المسارات الأساسية للموقع ---

@app.route('/')
def index():
    # بنجيب الإيميل للخدمة عشان لو موجود تظهر الأيقونة
    user_email = session.get('user_email')
    return render_template('index.html', user_email=user_email)

# --- المسارات الخاصة بجوجل والأرشفة (إضافة جديدة) ---

@app.route('/robots.txt')
def robots_txt():
    # بيسمح لجوجل إنه يشوف ملف التعليمات من فولدر static
    return send_from_directory(app.static_folder, 'robots.txt')

@app.route('/sitemap.xml')
def sitemap_xml():
    # بيسمح لجوجل إنه يشوف خريطة الموقع من فولدر static
    return send_from_directory(app.static_folder, 'sitemap.xml')

# --- أضف هنا باقي الـ Routes الخاصة بموقعك (مثل إزالة الخلفية والرفع) ---

# مثال لمسار معالجة الصور (تأكد من وجوده في كودك الأصلي)
@app.route('/remove-bg', methods=['POST'])
def remove_background():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    # كود معالجة الصورة باستخدام الـ API
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': file},
        data={'size': 'auto'},
        headers={'X-API-Key': API_KEY},
    )
    
    if response.status_code == requests.codes.ok:
        return send_file(
            io.BytesIO(response.content),
            mimetype='image/png',
            as_attachment=True,
            download_name='hamouzi_no_bg.png'
        )
    else:
        return "حدث خطأ في معالجة الصورة، حاول مرة أخرى.", 400

if __name__ == '__main__':
    app.run(debug=True)
