from flask import Flask, render_template, request
from model import ResumeRanker
import csv
import json
from datetime import datetime
import os
app = Flask(__name__)
# Load model
ranker = ResumeRanker("data/G5_Resume.csv")

# ------------------ FILE STORAGE ------------------
def save_to_csv(job_desc, results):
   with open("results.csv", mode='a', newline='', encoding='utf-8') as file:
       writer = csv.writer(file)
       for _, row in results.iterrows():
           writer.writerow([
               datetime.now(),
               job_desc,
               row['ID'],
               row['Category'],
               row['score']
           ])

def save_to_json(job_desc, results):
   with open("results.json", "a", encoding='utf-8') as f:
       for _, row in results.iterrows():
           data = {
               "timestamp": str(datetime.now()),
               "job_description": job_desc,
               "candidate_id": row['ID'],
               "category": row['Category'],
               "score": float(row['score'])
           }
           json.dump(data, f)
           f.write("\n")

# ------------------ ROUTES ------------------
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/rank', methods=['POST'])
def rank():
   job_desc = request.form['job_description']
   # Rank resumes
   results = ranker.rank_resumes(job_desc)
   # Save results (files only)
   save_to_csv(job_desc, results)
   save_to_json(job_desc, results)
   return render_template('results.html', tables=results.to_dict(orient='records'))

# ------------------ MAIN ------------------
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
