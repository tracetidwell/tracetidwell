import datetime as dt
from flask import Flask, request, render_template, redirect, url_for
from utils import predict_race
    
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/triathlon')
def triathlon():
    return render_template('triathlon.html')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/race_time_form')
def race_time_form():
    return render_template('race_time_form.html')

@app.route('/race_time_prediction', methods=['GET', 'POST'])
def race_time_prediction():
    if request.method == 'POST':
        inputs = request.form.copy()
        print(inputs)
        results = predict_race(inputs)
        print(results)
        return render_template('race_time_prediction.html', results=results)
    return render_template('race_time_prediction.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0', port=5000, debug=True)