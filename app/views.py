#views.py

from app import app
import json,os
import time
from random import random
from flask import Flask, render_template, make_response,request, redirect
from werkzeug import secure_filename

UPLOAD_FOLDER = 'app/uploads'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg','pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods = ['GET', "POST"])
def home():
    if request.method == "POST":
        if request.form['query']:
            print request.form['query']
            tweets = getTweets(request.form['query'])
            pol = []
            temp_pol = getPoles()
            for item in temp_pol:
                pol.append({"name":item, "y" : temp_pol[item]})
            print pol
            query = "#"+str(request.form['query']).upper()
            return render_template('tweetsAnalyse.html', tweets = tweets, pol = json.dumps(pol), query = query)
    return render_template('index.html', data='test')


@app.route('/', methods = ['GET','POST'])
def getData():
    result = None
    print 'here'
    if request.method == "POST":
        print 'post'
        if request.form['submit']=="file":
            print 'file'
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print filename
                f=open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'r')
                lines=f.read()
                #result = getTextAnalyse(lines)
                print result
                time.sleep(4)
                return render_template('textAnalysis.html', result = (result[0], result[1]), text = lines, keywords=result[2])
    return render_template('textAnalysis.html', result = result)