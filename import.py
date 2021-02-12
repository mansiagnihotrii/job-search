import os
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    # Create table to import data into
    #TABLE TO STORE REGISTERED USER INFORMATION
    db.execute("CREATE TABLE users (user_id SERIAL PRIMARY KEY, firstname VARCHAR NOT NULL, lastname VARCHAR NOT NULL, username VARCHAR NOT NULL, password VARCHAR NOT NULL)")
    #TABLE TO STORE JOB CATEGORIES
    db.execute("CREATE TABLE categories (job_category VARCHAR PRIMARY KEY,logo_location VARCHAR)")
    #TABLE TO STORE JOBS
    db.execute("CREATE TABLE jobs (job_id SERIAL PRIMARY KEY, job_name VARCHAR NOT NULL, company_name VARCHAR NOT NULL,job_category VARCHAR NOT NULL REFERENCES categories(job_category), ctc VARCHAR ,city VARCHAR NOT NULL, country VARCHAR NOT NULL,description VARCHAR NOT NULL,phone VARCHAR NOT NULL)")
    #INSERTING DUMMY DATA
    insert_query = "INSERT INTO categories (job_category,logo_location) VALUES (:job_category,:logo_location)"
    with open('job_category.csv','r') as f:
        csv_reader = csv.reader(f,delimiter=',')
        db.execute(insert_query,[{"job_category":row[0],"logo_location":row[1]} for row in csv_reader])
    f.close()
    db.commit()

if __name__ == "__main__":
    main()
