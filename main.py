from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_stack_overflow_jobs
from exporter import save_to_file
from flask import Flask, render_template, request, redirect, send_file


db = {}
app = Flask("Scraper")

@app.route("/")
def home():
    return render_template("search.html") 

@app.route("/report")
def report():
    word = request.args.get("word")
    if word:
        word = word.lower()
    else:
        return redirect("/")

    if db.get(word):
        jobs = db[word]
    else:
        indeed_jobs = get_indeed_jobs(word)
        stackoverflow_jobs = get_stack_overflow_jobs(word)
        jobs = indeed_jobs + stackoverflow_jobs
        db[word] = jobs

        return render_template("report.html",
            searchingBy=word,
            resultCount=len(jobs),
            jobs=jobs)

@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        if not word:
            raise Exception()

        word = word.lower()

        if not db.get(word):
            raise Exception()
        
        save_to_file(db[word])
        return send_file("jobs.csv")
    except:
        return redirect("/")



app.run(host="0.0.0.0")