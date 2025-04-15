🚀 DEPLOYMENT.md - Deployment Guide for News Aggregator

This guide explains how to deploy the News Aggregator project locally.

✅ Step 1: Clone the Repository

git clone <your-repo-url>
cd Course-Project

✅ Step 2: Create and Activate Virtual Environment (Optional but Recommended)

python3 -m venv .venv
source .venv/bin/activate

✅ Step 3: Install Requirements

You can use pip freeze to recreate the environment or run:

pip install -r requirements.txt

If requirements.txt is not present, install manually using pip freeze output (already shared above).

✅ Step 4: Set Environment Variables

If needed, set:

export FLASK_APP=run.py
export FLASK_ENV=development

(Windows PowerShell: $env:FLASK_APP = "run.py")

✅ Step 5: Initialize the Database

Make sure database exists, then run migrations if needed:

flask db init
flask db migrate -m "initial"
flask db upgrade

Or use pre-existing database.db.

✅ Step 6: Run the Application

flask run

Visit the app in your browser: http://localhost:5002

✅ Step 7 (Optional): Seed Test Data

To insert sample articles:

python seed_articles.py

✅ Step 8 (Optional): Reset Database

To delete all articles:

python reset-db.py