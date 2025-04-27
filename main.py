from flask import Flask, render_template, request, send_file, session, redirect, url_for
from fpdf import FPDF
from datetime import datetime
import os
import google.generativeai as genai

app = Flask(__name__)
os.makedirs("responses", exist_ok=True)

secret_key = os.urandom(24)  
app.secret_key = secret_key  

# Model setup
genai.configure(api_key="Enter API KEY")
model = genai.GenerativeModel("models/gemini-1.5-flash", generation_config={
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 550
})

# Custom Prompt
system_prompt = '''You are a highly sensitive and expressive language model.
Your task is to analyze the given text and return a detailed breakdown of its emotional and tonal characteristics.
You should not use { in the output}. no use of slash is required either make it professional looking
if the prompt is a paragraph rather than a single line you are not allowed to use any special characters and you have to summarize the paragraph in 4-5 lines
For the provided input, output the following:
1. Primary Emotion: Choose one from (Joyful, Sad, Angry, Fearful, Calm, Nostalgic, Hopeful, Anxious, Lonely, Relieved, Empowered, Indifferent)
2. Tone: Choose one from (Sarcastic, Motivational, Informative, Critical, Defensive, Supportive, Ranting, Curious, Objective, Promotional, Persuasive, Wholesome)
3. Internet Vibe: Choose one from (Petty, Savage, Cringe, Based, Spicy, Dry, Cold, Emotional Damage, Clownish, Galaxy Brain, Diplomatically Toxic)
4. Explanation: 2–3 lines explaining why you chose these sentiments. Mention tone indicators like word choice, punctuation, emojis, or context if applicable.
5. Confidence Score (0-100) for how certain you are about the above classification.
Return everything in structured format like JSON or Markdown.
You are not allowed to use any special characters in the output except :
'''

@app.route('/')
def index():
    return render_template("index.html")

# Store the text
@app.route('/store-text', methods=['POST'])
def store_text():
    session['text'] = request.form['text']
    return '', 204  # 

# Analyze route
@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = session.get('text', '')
    if not user_input:
        return redirect(url_for('index'))

    final_prompt = system_prompt + user_input
    try:
        response = model.generate_content(final_prompt)
        analysis = response.text
    except Exception as e:
        return f"Error during analysis: {str(e)}"

    return generate_pdf("Sentience Analysis", user_input, analysis)

# Convert route
@app.route('/convert', methods=['POST'])
def convert():
    user_input = session.get('text', '')
    conversion_type = request.form.get('conversion_type', 'Ask_AI')
    if not user_input:
        return redirect(url_for('index'))

    prompt = "Convert the following text to " + conversion_type + ": " + user_input
    try:
        response = model.generate_content(prompt)
        result = response.text
    except Exception as e:
        return f"Error during conversion: {str(e)}"

    return generate_pdf("Converted Text", user_input, result)

def clean_text(text):
    return ''.join([char if ord(char) < 128 else ' ' for char in text])

#pdf
def generate_pdf(title, input_text, output_text):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"result_{timestamp}.pdf"
    filepath = os.path.join("responses", filename)

    input_text = clean_text(input_text)
    output_text = clean_text(output_text)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, title, ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "By: Ryder & AI", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Input Text:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, input_text)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Result:", ln=True)
    pdf.set_font("Arial", size=12)
    formatted_output = output_text.replace("{", "").replace("}", "").replace("json", "").replace("```", "")
    pdf.multi_cell(0, 10, formatted_output)

    pdf.output(filepath)
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
