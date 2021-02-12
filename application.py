import os

from flask import Flask, session, render_template, redirect, request, url_for, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

jobfinder= Flask(__name__)


# CHECK FOR ENVIRONMENT VARIABLES
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# CONFIGURE SESSION TO USE FILESYSTEM
jobfinder.config["SESSION_PERMANENT"] = False
jobfinder.config["SESSION_TYPE"] = "filesystem"
Session(jobfinder)

# SET UP DATABASE
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


#HOME PAGE
@jobfinder.route("/")
def index():
    category = db.execute("SELECT * FROM categories")
    recent = db.execute("SELECT * FROM jobs ORDER BY job_id DESC LIMIT 5")
    return render_template("index.html",category=category,recent=recent)

#FIND JOB
@jobfinder.route("/findjob/<category>")
def findjob(category):
    jobs = db.execute("SELECT * FROM jobs WHERE job_category = :category",{'category': str(category)}).fetchall()
    count_category = len(jobs)
    return render_template("findjob.html",jobs=jobs,category=category,count_category=count_category)

#POST JOB
@jobfinder.route("/postjob",methods=['GET','POST'])
def postjob():
    session.clear()
    message = ""
    if request.method == "POST":
        key = db.execute("INSERT INTO jobs (job_name,company_name,job_category,ctc,city,country,description,phone) VALUES (:job_name,:company_name,:job_category,:ctc,:city,:country,:description,:phone)",
        {'job_name':request.form.get("jobname") , 'company_name':request.form.get("companyname") , 'job_category':request.form.get("category") , 'ctc':request.form.get("ctc") ,'city':request.form.get("city") ,'country':request.form.get("country") , 'description':request.form.get("description"),'phone':request.form.get("phone")  })
        db.commit()
        message = "Job Posted successfully"

    category = db.execute("SELECT * FROM categories")
    return render_template("post_job.html",category=category,message=message)


#MAIN FUNCTION
if __name__=='__main__':
    jobfinder.run(debug=True)
