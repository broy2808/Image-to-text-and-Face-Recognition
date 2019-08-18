from flask import Flask, render_template, request,url_for,flash
from werkzeug import secure_filename
import os
import Face_recog
import pytesseract
from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from PIL import Image

app=Flask(__name__)
PEOPLE_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
FOLDER = os.path.join('static', 'uploaded_image')
app.config['UPLOAD_PIC'] = FOLDER
pytesseract.pytesseract.tesseract_cmd = r"C:\Python37\Lib\site-packages\Tesseract-OCR\tesseract.exe"
ALLOWED_EXTENSIONS = { 'png', 'jpg', 'jpeg', 'gif'}
app.secret_key = os.urandom(16)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
         
          if request.method == 'POST' :
                  print(request.form.get('val'))
                  if request.form.get('val')=='Handwriting':
                         clear()
                         f = request.files['file']
                         if 'file' not in request.files:
                                flash('No file part')
                                return redirect(request.url)
                         if  allowed_file(f.filename):
                             print(f.filename)
                             img= request.files['file']
                             #f.save(secure_filename(f.filename))
                             print(f.filename)
                             filename_img = secure_filename(img.filename)
                             img.save(os.path.join(app.config['UPLOAD_PIC'],filename_img))
                             words=grab_text(os.path.join(app.config['UPLOAD_PIC'],filename_img))
                             print(words)
                             upd_filename = os.path.join(app.config['UPLOAD_PIC'],filename_img)
                             
                             return render_template("show_entries.html", data=words,img1=upd_filename,txt="Text extracted from image=>")
                         else:
                             flash('No file part')
                             return render_template('index.html')
                  else:
                         clear()
                         f = request.files['file']
                         img= request.files['file']
                         print(f.filename)
                         filename_img = secure_filename(img.filename)
                         img.save(os.path.join(app.config['UPLOAD_PIC'],filename_img))
                         images=[]
                         fixed_image_url=[]
                         images=Face_recog.collect_dataset(os.path.join(app.config['UPLOAD_PIC'],filename_img))
                         
                         for img in images:
                             print(img)
                             full_filename = os.path.join(app.config['UPLOAD_FOLDER'], img)
                             fixed_image_url.append(full_filename)
                             
                         upd_filename = os.path.join(app.config['UPLOAD_PIC'], filename_img)
                         return render_template("show_entries.html",image=fixed_image_url,img1=upd_filename,txt1="Faces from uploaded image=>")
  
@app.route('/about', methods =['GET'])
def about():
    return render_template("about.html")

def grab_text(image_file):
    text = pytesseract.image_to_string(image_file)
    return text

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clear():
    for file in os.scandir(app.config['UPLOAD_PIC']):
            os.unlink(file.path)
if __name__ == "__main__":
    app.run(debug = True)
