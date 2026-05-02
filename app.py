from flask import Flask, render_template, request
import requests
import base64
import os

app = Flask(__name__)

# 🔥 API KEY الخاص بك (تأكد أنه شغال وله رصيد)
API_KEY = "T8PX6VMNgTofTAD72S4AZZPx"

# 1. الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')

# 2. مسارات الأدوات (تفتح الصفحات الجديدة)
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

# 3. منطق إزالة الخلفية (الزر الرئيسي في الـ Index)
@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')
        if not file:
            return render_template('index.html', error="برجاء اختيار صورة أولاً")

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': file},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_code != requests.codes.ok:
            return render_template('index.html', error="خطأ من سيرفر إزالة الخلفية")

        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('index.html', result_image=img_base64)

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return render_template('index.html', error="حدث خطأ في الرفع")

# 4. منطق دمج الصور بالذكاء الاصطناعي (ميزة Merge)
@app.route('/process_merge', methods=['POST'])
def process_merge():
    try:
        main_file = request.files.get('person_img')
        bg_file = request.files.get('bg_img')

        if not main_file or not bg_file:
            return render_template('merge.html', error="برجاء رفع الصورتين")

        # إرسال الصورتين معاً لـ remove.bg ليتم دمجهم ذكياً
        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={
                'image_file': main_file,
                'bg_image_file': bg_file
            },
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_code != requests.codes.ok:
            return render_template('merge.html', error="فشلت عملية الدمج")

        img_base64 = base64.b64encode(response.content).decode('utf-8')
        return render_template('merge.html', result_image=img_base64)

    except Exception as e:
        print("MERGE ERROR:", e)
        return render_template('merge.html', error="حدث خطأ أثناء المعالجة")

# 5. تشغيل التطبيق
if __name__ == '__main__':
    # البورت 8080 للتشغيل المتوافق مع معظم السيرفرات
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
