import json,os
from time import time
from random import random
from flask import Flask, render_template, make_response,request, redirect,session
import requests
from werkzeug import secure_filename
app = Flask(__name__)


UPLOAD_FOLDER = '/Users/nareshkumar.v/learning/personalGitRepos/mrpscan-ui/app/uploads'
ALLOWED_EXTENSIONS = set(['txt','png','jpg','jpeg','pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ENDPOINT_URL="10.85.x.y"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



@app.route('/')
def hello_world():
    return render_template('textAnalysis.html', data='test')

@app.route('/live-data')
def live_data():
    print Info.tweets
    data = [time() * 1000, random() * 100, "Nishant"]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


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
                f=open(os.path.join(app.config['UPLOAD_FOLDER'], filename),'rb')
                lines=f.read()
                #result = getTextAnalyse(lines)
                print result
                #time.sleep(4)
                files = {'upload_file': f}
                values = {'DB': 'photcat', 'OUT': 'csv', 'SHORT': 'short'}

                #r = requests.post(ENDPOINT_URL, files=files, data=values)
                result=98#r.content
                return render_template('textAnalysis.html', result = (result), text = lines)
    return render_template('textAnalysis.html', result = result)



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
