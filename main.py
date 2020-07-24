from flask import Flask, render_template, request, redirect
from scrapper import total_get_jobs

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
        resultsNumber=len(jobs))

app.run()