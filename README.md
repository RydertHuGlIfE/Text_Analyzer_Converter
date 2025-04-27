Tone Detection Website

This project is a Flask web application that analyzes user input text and detects:

    Primary Emotion

    Tone

    Internet Vibe

    Explanation

    Confidence Score

It also generates a PDF report based on the analysis.
Features

    Web interface to submit text.

    AI-based sentiment and tone analysis.

    Downloadable PDF report.

    Hosted locally or via Dev Tunnels (port 5000).

Requirements

    Python 3.12+

    Flask

    fpdf2

    OpenAI (or your AI API if used)

    Google generative AI

Install dependencies:

pip install flask fpdf2 google-generativeai

How to Run

Either Clone the REPO or 

Go to project directory:

cd tone-detector-website

Start Flask server:

python main.py

Folder Structure

tone-detector-website/
├── main.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── script.js
└── README.md

Notes

    Avoid non-ASCII characters in PDF unless UTF-8 support is added.
