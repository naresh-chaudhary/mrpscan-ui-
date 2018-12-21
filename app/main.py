import json,os
from app import app
from time import time
from random import random
from flask import Flask, render_template, make_response,request, redirect,session
import requests
from werkzeug import secure_filename


UPLOAD_FOLDER = '/Users/nareshkumar.v/learning/personalGitRepos/mrpscan-ui/app/uploads'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg','pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ENDPOINT_URL="http://172.29.162.39:2505/upload"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/')
def hello_world():
    return render_template('textAnalysis.html', data='test')



@app.route('/', methods = ['GET','POST'])
def getData():
    result = None
    print 'here'
    print os.pardir
    if request.method == "POST":
        print 'post'
        if request.form['submit']=="file":
            print 'file'
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print filename
                print os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f=open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'rb')
                lines=f.read()

                files = {'datafile': (filename, f, 'multipart/form-data')}

                r = requests.post(ENDPOINT_URL, files=files)
                print r.content
                result=r.content
                return render_template('textAnalysis.html', result = (result), text = lines)
    return render_template('textAnalysis.html', result = result)



