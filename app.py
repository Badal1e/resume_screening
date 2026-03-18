from flask import Flask, render_template, request
from model import ResumeRanker
from database import get_connection
import pymysql
import csv
from _datetime import datetime
import os

app = Flask(__name__)

ranker = ResumeRanker("data/G5_Resume.csv")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/rank', methods=['POST'])
def rank():
    job_desc = request.form['job_description']
    results = ranker.rank_resumes(job_desc)

    # Save to DB
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in results.iterrows():
        cursor.execute("""
            INSERT INTO results (job_description, candidate_id, category, score)
            VALUES (%s, %s, %s, %s)
        """, (job_desc, str(row['ID']), row['Category'], float(row['score'])))

    conn.commit()
    conn.close()

    save_to_csv(job_desc, results)

    return render_template('results.html', tables=results.to_dict(orient='records'))


@app.route('/history')
def history():
    # conn = get_connection()
    # cursor = conn.cursor(pymysql.cursors.DictCursor)

    cursor.execute("SELECT * FROM results ORDER BY created_at DESC LIMIT 20")
    data = cursor.fetchall()

    conn.close()

    return render_template('history.html', data=data)


def save_to_csv(job_desc, results):
    file_name = "results.csv"
    
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        for _, row in results.iterrows():
            writer.writerow([
                datetime.now(),
                job_desc,
                row['ID'],
                row['Category'],
                row['score']
            ])

import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))