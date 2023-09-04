import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
import openai

# Set up OpenAI API key
openai.api_key = "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"

# Load dataset from csv file
dataset = pd.read_csv("dataset.csv")

# Define function to prompt user and get response
def ask_question(prompt):
    response = input(prompt + " ")
    return response.lower()

# Define function to generate advice based on user input
def generate_advice(specs):
    prompt = f"List me some Indian model Gadget  with the following {specs}, Also provide a comparison between the products you suggest. "

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7
    )

    advice = response.choices[0].text.strip()
    # advice = response
    return advice

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/advice', methods=['POST'])
def advice():
    prod = (request.form['prod'])
    return redirect(url_for('show_questions', prod=prod))

@app.route('/questions/<prod>', methods=['GET', 'POST'])
def show_questions(prod):
    prod = str(prod)  
    
    if request.method == 'GET':
        if prod == "mobile" :
            questions = dataset["Mobile Qns"].tolist()
        elif prod == "Laptop":
            questions = dataset["Laptop Qns"].tolist()
        elif prod == "TV":
            questions = dataset["TV Qns"].tolist()
        else:
            questions = dataset["No questions"].tolist()
        
        return render_template('questions.html', prod=prod, questions=questions)
    
    elif request.method == 'POST':
        answers = []
        for i in range(6):
            answer = request.form.get(f'answer{i+1}')
            answers.append(answer)
        advice = generate_advice(answers)
        return render_template('advice.html', advice=advice)

if __name__ == '__main__':
    app.run(debug=True)
