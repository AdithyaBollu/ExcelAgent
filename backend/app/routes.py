from flask import request, jsonify
from . import app
from app.agent.agent import chat_with_nutrition_bot


@app.route('/')
def home():
    return "Hello, Flask is running!"

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        history = data.get('history', [])
        
        bot_response = chat_with_nutrition_bot(user_message, history)

        return jsonify({
            'response': bot_response
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500