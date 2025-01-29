import openai
from flask import Flask, render_template, request, jsonify
import os
from fuzzywuzzy import process

app = Flask(__name__)


openai.api_key = os.getenv("OPENAI_API_KEY")


FAQ_FILE = "faq_data.txt"

def load_faq_data():
    """Load FAQ data from a text file."""
    faq_data = []
    try:
        with open(FAQ_FILE, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                question, answer = line.strip().split("|", 1)  
                faq_data.append({"question": question, "answer": answer})
    except FileNotFoundError:
        print("FAQ file not found. Creating a new one...")
        open(FAQ_FILE, "w").close()  
    return faq_data

def log_query(question, answer):
    """Logs user queries and answers in a text file."""
    with open("user_queries.txt", "a", encoding="utf-8") as file:
        file.write(f"Q: {question}\nA: {answer}\n\n")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question')
    faq_data = load_faq_data()

    
    faq_questions = [faq['question'] for faq in faq_data]
    
    
    best_match = process.extractOne(question, faq_questions)
    
    
    if best_match and best_match[1] > 70:  
        matched_question = best_match[0]
        answer = next(faq['answer'] for faq in faq_data if faq['question'] == matched_question)
        log_query(question, answer)
        return jsonify({'answer': answer})

    
    answer = generate_answer(question, faq_data)
    
   
    if not answer or "I'm sorry" in answer:
        answer = "I'm not sure about that. Please visit our website or contact customer support."
    
    log_query(question, answer)
    return jsonify({'answer': answer})

def generate_answer(question, faq_data):
    """Generates an AI response using OpenAI API based on the FAQ data."""
    try:
        faq_text = "\n".join([f"{faq['question']} - {faq['answer']}" for faq in faq_data])
        prompt = (f"The following is a list of questions and answers for a bank:\n\n"
                  f"{faq_text}\n\n"
                  f"Answer this question based on the above information: {question}")
        
        response = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.RateLimitError:
        return "I'm sorry, but our AI service has reached its limit. Please try again later."
    except openai.error.OpenAIError as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
