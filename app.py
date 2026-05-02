from flask import Flask, render_template, request
import requests
import base64
import os

app = Flask(__name__)

# 🔥 API KEY الخاص بك
API_KEY = "T8PX6VMNgTofTAD72S4AZZPx"

@app.route('/')
def index():
    return render_template('index.html')

# --- مسارات الأدوات الجديدة ---

@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/compress')
def compress():
    return render_template('compress.html')

@app.route('/convert')
def convert():
    return render_template('convert.html')

@app.route('/merge')
def merge():
    return render_template('merge.html')

# --- نهاية المسارات الجديدة ---

@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')

        if not file:
            return render_template('index.html', error="برجاء اختيار صورة أولاً")

        # إرسال الصورة لـ remove.bg
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': file},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_code != requests.codes.ok:
            # طباعة الخطأ في الكونسول للمساعدة في الديباجينج
            print("API Error:", response.text)
            return render_template('index.html', error="خطأ في معالجة الصورة من السيرفر")

        # تحويل النتيجة لـ base64 للعرض في المتصفح
        img_base64 = base64.b64encode(response.content).decode('utf-8')

        return render_template('index.html', result_image=img_base64)

    except Exception as e:
        print("SYSTEM ERROR:", e)
        return render_template('index.html', error="حدث خطأ غير متوقع")


if __name__ == '__main__':
    # دعم التشغيل على Heroku أو محلياً
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
