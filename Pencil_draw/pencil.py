#Importing Libraries
from flask import Flask, render_template, Response 
import os
from flask import flash, redirect, request, url_for
from PIL import ImageTk, Image
import cv2
import numpy as np

app=Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_to_sketch(image_path):
    image=cv2.imread(image_path)

    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    inverted = cv2.bitwise_not(gray)

    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)

    sketch = cv2.bitwise_not(blurred)

    return sketch




@app.route('/', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file attached')
        
        file=request.files['file']

        if file.filename == '' or not allowed_file(file.filename):
            return render_template('index.html', error='No file selected or invalid file type')
            

        filename = file.filename

        file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)

        file.save(file_path)

        sketch=convert_to_sketch(file_path)

        cv2.imwrite(sketch,sketch)

        return render_template('result.html',sketch=sketch)
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
