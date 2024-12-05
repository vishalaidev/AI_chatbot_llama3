import streamlit as st
import requests


def send_message_to_server(student_id, message):
    url = "http://192.168.x.xx:5011/chatbot"  
    data = {
        "student_id": student_id,
        "message": message
    }
    
    # Sending POST request to Flask server
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            return response.json() 
        else:
            st.error(f"Error: {response.json()['message']}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

# Function for the Streamlit UI
def get_student_input():
    st.title("AI Chatbot for Students")
    
    # Input for student ID
    student_id = st.text_input("Enter your student ID:")
    
    if student_id:
        # Input for the student message
        user_input = st.text_input(f"Message from {student_id}:")
        
        # Button to send the message to the server
        if st.button("Send Message"):
            if user_input:
                response = send_message_to_server(student_id, user_input)
                if response:
                    st.write("AI Bot:", response['response'])
                    st.write("Score:", response['score'])
            else:
                st.warning("Please enter a message.")
                
    # Option to exit the chat
    if st.button("Exit"):
        st.stop()

# Run the Streamlit app
if __name__ == "__main__":
    get_student_input()
