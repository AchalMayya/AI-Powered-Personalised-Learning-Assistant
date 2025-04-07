from flask import Flask, request, render_template, jsonify, session
from prompt_engineering import create_student_recommendation_prompt
from advanced_prompting import create_few_shot_prompt
import requests
import os
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management
app.config['SESSION_TYPE'] = 'filesystem'

# Store conversation history per session
conversation_histories = {}

def get_llama_response(prompt, history=""):
    """Send a prompt to Llama2 and get a response while maintaining conversation context"""
    full_prompt = f"Conversation history:\n{history}\n\nUser: {prompt}\nAssistant: "
    
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': 'llama2',
            'prompt': full_prompt,
            'stream': False,
            'temperature': 0.7,
            'top_p': 0.9,
            'max_tokens': 2048
        }
    )
    return response.json()['response']

@app.route('/')
def index():
    # Create a unique session ID if not exists
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        conversation_histories[session['session_id']] = ""
    
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def recommend():
    session_id = session.get('session_id', str(uuid.uuid4()))
    student_data = request.json

    # Generate recommendation prompt
    prompt = create_few_shot_prompt(student_data)

    try:
        recommendation = get_llama_response(prompt)
        
        # Store recommendation in conversation history for this session
        conversation_histories[session_id] = f"STUDENT PROFILE:\n"
        for key, value in student_data.items():
            if isinstance(value, list):
                value_str = ", ".join(value) if value else "None"
            else:
                value_str = value if value else "None"
            conversation_histories[session_id] += f"- {key}: {value_str}\n"
        
        conversation_histories[session_id] += f"\nAI RECOMMENDATION:\n{recommendation}\n"
        
        return jsonify({'success': True, 'recommendation': recommendation})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/chat', methods=['POST'])
def chat():
    session_id = session.get('session_id')
    if not session_id or session_id not in conversation_histories:
        return jsonify({'success': False, 'error': 'Session expired. Please refresh the page.'})
    
    user_message = request.json.get("message", "").strip()

    if not user_message:
        return jsonify({'success': False, 'error': 'Empty message'})

    try:
        # Create a context-aware prompt for the follow-up question
        history = conversation_histories[session_id]
        
        # Add instructions to focus on educational advice in context
        enhanced_prompt = f"""
The user is asking a follow-up question about the educational recommendations provided.
Respond with helpful, specific educational advice related to their question.
Focus on practical, actionable guidance that builds on the previous recommendations.

The user asks: {user_message}
"""
        
        response = get_llama_response(enhanced_prompt, history)
        
        # Append to conversation history for this session
        conversation_histories[session_id] += f"User: {user_message}\nAssistant: {response}\n"
        
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/clear-chat', methods=['POST'])
def clear_chat():
    """Clear the chat history but keep the recommendation"""
    session_id = session.get('session_id')
    if not session_id or session_id not in conversation_histories:
        return jsonify({'success': False, 'error': 'Session not found'})
    
    try:
        # Keep only the recommendation part of the conversation
        history = conversation_histories[session_id]
        recommendation_end = history.find("AI RECOMMENDATION:") + len("AI RECOMMENDATION:")
        recommendation_section = history[:recommendation_end]
        if recommendation_section:
            conversation_histories[session_id] = recommendation_section
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    # Ensure the templates directory exists
    os.makedirs('templates', exist_ok=True)
    
    # No longer trying to write the HTML file here
    # This was erasing your file before
    
    print("Server is starting. Access the application at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)