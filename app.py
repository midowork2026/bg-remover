from flask import Flask, render_template, request
from rembg import remove
from PIL import Image
import io
import base64
import os

app = Flask(_name_)

# الصفحة الرئيسية
@app.route('/')
def index():
    return render_template('index.html')


# رفع الصورة ومعالجتها
@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files.get('file')

        if not file:
            return render_template('index.html', error="ارفع صورة")

        # 🔥 تقليل حجم الصورة (مهم عشان السيرفر ما يقعش)
        input_image = Image.open(file.stream).convert('RGBA')
        input_image.thumbnail((800, 800))

        output_image = remove(input_image)

        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)

        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')

        return render_template('index.html', result_image=img_base64)

    except Exception as e:
        print("ERROR:", e)
        return render_template('index.html', error="حصل خطأ، جرب صورة أصغر")


if _name_ == '_main_':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
