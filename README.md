# AI_chatbot_llama3

https://github.com/user-attachments/assets/7b83b6c0-29c9-42d4-b45c-bd24a9300117

AI Chatbot with Flask, LangChain, MongoDB, and Scoring
=====================================================

This project is a chatbot application built using Flask as the backend framework, LangChain with an Ollama model (Llama3), and MongoDB for storing conversation history. It also includes a scoring mechanism to evaluate AI responses based on predefined criteria. The chatbot can handle real-time interaction via a Command Line Interface (CLI) and supports multiple users through unique `student_id`s.

-----------------------------------------------------

Features:
---------
1. Chatbot with Contextual Memory:
   - The chatbot leverages LangChain to process user questions based on the context from previous conversations stored in MongoDB.

2. Response Scoring:
   - AI responses are scored based on specific criteria like keyword presence, response length, and relevance.

3. Conversation Storage:
   - MongoDB stores user inputs, AI responses, scores, and context for future reference.

4. Real-Time CLI Interaction:
   - Users can interact with the chatbot in real-time through the CLI.

5. Threaded Flask Server:
   - The Flask server runs in the background, while the CLI operates in the foreground.

-----------------------------------------------------

Installation and Setup:
------------------------

1. Prerequisites:
   - Python 3.8 or higher
   - MongoDB installed and running on `localhost:27017`
   - `pip` for Python package management

2. Install Python Dependencies:
   ```bash
   install flask pymongo langchain safetensors llama 
   ```
3. Configure MongoDB:
   - Ensure MongoDB is running locally and has the database `chatbot_db` with a collection named `conversations`.

4. Configure LangChain with Ollama:
   - Install and set up Ollama to use the `Llama3` model. Follow the instructions provided in the LangChain Ollama Documentation.

5. Start the Flask Application:
   - Run the Flask server with the following command:
     ```bash
     python ai_bot_server.py.py
     ```

   - This will start the Flask server on `http://**********:5011`.


-----------------------------------------------------

How It Works:
-------------

1. **User Input**:
   - Users send input to the Flask server through CLI or API POST requests.

2. **Retrieve Context**:
   - The server fetches the conversation history for the given `student_id` from MongoDB.

3. **Generate Response**:
   - LangChain processes the input and generates a response using the `Llama3` model.

4. **Score the Response**:
   - The `calculate_score` function evaluates the response based on:
     - Keyword presence
     - Response length
     - Relevance

5. **Save Conversation**:
   - The server saves the conversation history, including the score, in MongoDB.

6. **Respond to User**:
   - The AI's response and score are sent back to the user.

-----------------------------------------------------

API Endpoints:
--------------

POST `/chatbot`
- **Description**: Processes user input and returns AI's response along with a score.
- **Request Body**:
  ```json
  {
      "student_id": "12345",
      "message": "What is LangChain?"
  }
  ```
- **Response**:
  ```json
  {
      "status": "success",
      "response": "LangChain is a framework for building applications using large language models.",
      "score": 95
  }
  ```

-----------------------------------------------------




