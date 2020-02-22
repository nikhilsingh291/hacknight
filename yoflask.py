# from flask import Flask

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "Hello, World!"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0',port=5698)

import os
from flask import Flask, flash, request, redirect, url_for, render_template

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        print(request.form)
        name=request.form['full_name']

        phone_no=request.form['phone']
        vehicle_no=request.form['vehicle_no']
        policy_no=request.form['policy_no']
        print('yo')
        return redirect('/upload')
    return render_template('index.html')
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print(request.method)
    print("hua?")
    if request.method == 'POST':
        print(request.files)
        # check if the post request has the file part
        # if len(request.files)==0:
        #     print('No files uploaded')
        #     return redirect(request.url)
        print(request.files)
        for i in request.files.keys():
            file=request.files[i]
            print(file)
        # file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                #filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename ))
                return 'Done'
    return render_template('page2.html')


    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <label>DL :</label><input type=file name=file> <br>
    #  <label>rc :</label><input type=file name=file2><br>
    #   <label>image :</label><input type=file name=file3> <comment>img</comment>
    #
    #   <input type=submit value=Upload>
    # </form>
    # '''



if __name__ == "__main__":
    app.secret_key = 'SECRET KEY'
    app.run(host='0.0.0.0',port=5698)
