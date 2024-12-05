from flask import Flask, request, jsonify
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from pymongo import MongoClient
import time
import threading

# Initialize Flask App
app = Flask(__name__)

# MongoDB connection
mongo_client = MongoClient("localhost:27017")
db = mongo_client['chatbot_db']
conversations_collection = db['conversations']

# LangChain setup for chatbot
template = """
Answer the question below.

Here is the conversation history : {context}
Question: {question}

Answer:
"""

model = OllamaLLM(model="llama3")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model

# Define scoring function
def calculate_score(question, ai_response):
    """
    Calculate the score for the AI's response based on certain criteria.
    """
    score = 100  # Start with a perfect score
    keywords = ["example", "explanation", "step", "learning", "question"]  # Example keywords to match

    # Check for keyword matches
    keyword_matches = sum(1 for keyword in keywords if keyword.lower() in ai_response.lower())
    if keyword_matches < len(keywords) * 0.5:  # Less than 50% of keywords matched
        score -= 20

    # Check response length
    response_length = len(ai_response.split())
    if response_length < 5:  # Too short
        score -= 30
    elif response_length > 100:  # Excessively long
        score -= 10

  
    if "irrelevant" in ai_response.lower():  
        score -= 40

    # Ensure the score is within 0-100
    score = max(0, min(score, 100))
    return score

# Route to handle user input and get chatbot response
@app.route('/chatbot', methods=['POST'])
def chatbot_response():
    data = request.json
    # Extract the necessary data from the incoming JSON
    student_id = data.get('student_id')
    user_input = data.get('message')

    # Check if the required fields are present
    if not student_id or not user_input:
        return jsonify({"status": "error", "message": "Missing student_id or message"}), 400
    
    # Retrieve conversation history from MongoDB for the given student
    conversation_history = list(conversations_collection.find({"student_id": student_id}).sort("timestamp", -1).limit(1))
    context = ""
    if len(conversation_history) > 0:
        context = conversation_history[0]["context"]

    # Get the AI's response
    result = chain.invoke({"context": context, "question": user_input})
    
    # Calculate the score based on the AI's response
    score = calculate_score(user_input, result)

    # Save the conversation history (user input and AI response)
    new_conversation = {
        "student_id": student_id,
        "user_input": user_input,
        "ai_response": result,
        "score": score,
        "context": context + f"\nUser:{user_input}\nAI: {result}",
        "timestamp": time.time()  # Store the timestamp
    }
    conversations_collection.insert_one(new_conversation)
    
    return jsonify({"status": "success", "response": result, "score": score})

# Function to simulate real-time interaction (CLI)
def handle_cli_input():
    print("Welcome to the AI chatbot! Type 'exit' to quit.")
    student_id = input("Enter your student ID: ")  # Get student ID
    while True:
        user_input = input(f"Student {student_id} : ")  # Get user question
        if user_input.lower() == 'exit':
            break
        # Send input to server via POST request
        data = {
            "student_id": student_id,
            "message": user_input
        }
        response = requests.post("http://192.168.x,xx/chatbot", json=data)
        
        if response.status_code == 200:
            result = response.json()
            print("AI Bot:", result["response"])
            print("Score:", result["score"])
        else:
            print("Error:", response.json()["message"])

if __name__ == "__main__":
    # Start Flask app in the background
    flask_thread = threading.Thread(target=lambda: app.run(host="192.168.x.x", port=5011, use_reloader=False))
    flask_thread.start()

    # Handle real-time CLI input
    handle_cli_input()
