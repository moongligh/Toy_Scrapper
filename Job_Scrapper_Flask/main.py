from flask import Flask, render_template, request, redirect, send_file
from scrapper import total_get_jobs
from exporter import save_to_csv

app = Flask('SuperScrapper')

db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/report')
def report():
    word = request.args.get('word')
    if word:
        word = word.lower()
        fromDB = db.get(word)
        
        if fromDB:
            jobs = fromDB
        else:
            jobs = total_get_jobs(word)
            db[word] = jobs
    else:
        return redirect('/')
    return render_template('report.html',
        SearchingBy=word,
        resultsNumber=len(jobs),
        jobs = jobs)

@app.route('/export')
def export():
    try:
        word = request.args.get('word')
        if not word:
            raise Exception()
        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            raise Exception()
        save_to_csv(jobs)
        return send_file('jobs.csv')
        
    except:
        return redirect('/')

app.run()