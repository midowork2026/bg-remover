from flask import Flask, render_template, request
import requests
import base64
import os

app = Flask(_name_)

# 🔥 حط API KEY هنا
API_KEY = "T8PX6VMNgTofTAD72S4AZZPx"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')

        if not file:
            return render_template('index.html', error="ارفع صورة")

        response = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': file},
            data={'size': 'auto'},
            headers={'X-Api-Key': API_KEY},
        )

        if response.status_code != requests.codes.ok:
            return render_template('index.html', error="خطأ في المعالجة")

        img_base64 = base64.b64encode(response.content).decode('utf-8')

        return render_template('index.html', result_image=img_base64)

    except Exception as e:
        print("ERROR:", e)
        return render_template('index.html', error="حصل خطأ")


if _name_ == '_main_':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
