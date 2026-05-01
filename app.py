from flask import Flask, request, render_template, redirect, session
from rembg import remove
from PIL import Image
import io, base64, os

app = Flask(__name__)
app.secret_key = "secret123"  # مهم للـ session

# بيانات تسجيل دخول ثابتة
USERNAME = "admin"
PASSWORD = "1234"

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect("/")
        else:
            return "بيانات غلط!"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route('/upload', methods=['POST'])
def upload():
    if "user" not in session:
        return redirect("/login")

    file = request.files.get('file')
    if not file:
        return "ارفع صورة!"

    input_image = Image.open(file.stream).convert('RGBA')
    output_image = remove(input_image)

    img_io = io.BytesIO()
    output_image.save(img_io, 'PNG')
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return render_template('index.html', result_image=img_base64)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
