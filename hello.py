import base64

from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from modules.fun import is_prime
import time
from PIL import Image, ImageChops
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os, io, base64

app = Flask(__name__)
auth = HTTPBasicAuth()

IMG_FOLDER = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}


@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


@app.route("/")
def hello_world():
    return "<p>Hello</p>"


@app.route("/p")
def p():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'most.jpg')
    return render_template("show.html", image=full_filename)
    # return "<p>Hello</p>"


@app.route("/prime/<int:number>")
def prime(number):
    return {"Is prime": is_prime(number)}



@app.route("/im_size", methods=["POST"])
def process_image():
    file = request.files['image']
    # Read the image via file.stream
    img = Image.open(file.stream)
    return jsonify({'msg': 'success', 'size': [img.width, img.height]})


@app.route('/picture')
def pic():
    return render_template('pic.html')


@app.route('/picture', methods=['POST'])
def submit_file():
    file1 = request.files['file']
    # Read the image via file.stream
    img = Image.open(file1.stream)
    img = ImageChops.invert(img)

    data = io.BytesIO()
    img.save(data, "JPEG")
    encoded_img = base64.b64encode(data.getvalue())
    decoded_img = encoded_img.decode('utf-8')
    img_data = f"data:image/jpeg;base64,{decoded_img}"
    return render_template("show.html", img_data=img_data)

    # return jsonify({'msg': 'success', 'size': [img.width, img.height]})
    # return render_template("show.html", image=file1)
    # return redirect('/picture/invert')
    # return redirect(url_for('inv', file=file1))


@app.route('/picture/invert/<file>')
def inv(file):
    # file = request.files['file']
    # Read the image via file.stream
    # img = Image.open(file.stream)

    return jsonify({'msg': 'success', 'size': 'test'})
    # return jsonify({'msg': 'success', 'size': [img.width, img.height]})


@app.route('/time')
@auth.login_required
def index():
    t = time.localtime()
    return {"time": time.strftime("%H:%M:%S", t)}
