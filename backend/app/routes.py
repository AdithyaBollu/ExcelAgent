from pathlib import Path
from flask import json, request, jsonify
from . import app
from app.agent.agent import chat_with_nutrition_bot
import openpyxl
import tempfile

import logging

logging.basicConfig(level=logging.INFO)


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
    


@app.route('/chat-with-files', methods=['POST'])
def handle_chat_with_files():
    try:
        user_message = request.form.get('message', '')
        history = request.form.get('history', [])
        file_count = int(request.form.get('file_count', 0))
        history = json.loads(history)
        
        temp_file_paths = dict()

        for i in range(file_count):
            file = request.files.get(f'file_{i}')
                
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                file.save(temp_file.name)
                logging.info(f"File saved to temporary location: {temp_file.name}")
                temp_file_paths[file.filename] = temp_file.name
        

        enhanced_user_message = f"{user_message} Files: "
        for file in temp_file_paths:
            enhanced_user_message += f"{file} at {temp_file_paths[file]}, "
        logging.info(f"Enhanced user message: {enhanced_user_message}")


        bot_response = chat_with_nutrition_bot(enhanced_user_message, history)

        return jsonify({
            "response": bot_response
        })
    except Exception as e:
        logging.error(f"Error in handle_chat_with_files: {e}")
        logging.info(e)
        return jsonify({
            'error': str(e)
        }), 500