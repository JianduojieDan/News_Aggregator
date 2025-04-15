📘 README - Course Project: News Aggregator Website

Welcome to the News Aggregator Website, a Flask-based application designed to collect, display, and manage news articles from various sources.

🎯 Project Overview

This project allows users to:

Browse recent articles by source

View article details (including images)

Search for articles by keyword

Save favorite articles

Receive recommendations (based on preferences)

Add new articles manually (with image upload)

📁 Project Structure

Course-Project/
├── app/                    # Main application code
│   ├── models/            # SQLAlchemy models
│   ├── routes/            # Flask Blueprints and views
│   ├── templates/         # HTML templates
│   └── static/            # Static files (CSS, images)
├── .venv/                 # Python virtual environment
├── database.db            # SQLite database file
├── run.py                 # Entry point to run the app
├── config.py              # Flask configuration file
├── seed_articles.py       # Script to insert test articles
├── reset-db.py            # Script to clear all article data
├── README.txt             # (This file)
└── DEPLOYMENT.md          # Deployment instructions

🛠 Technologies Used

Python 3.9+

Flask / Flask-SQLAlchemy / Flask-Login / Flask-WTF

SQLite (as database)

Jinja2 (template rendering)

🚀 How to Use the App

Visit homepage to see recent news.

Click on "Sources" to filter by specific news source.

Use "Read More" to view article details.

If logged in:

Save articles to favorites.

Set source preferences.

Get article recommendations.

Add new articles via /add_article.

👤 Author

Project by Jianduojie Dan



