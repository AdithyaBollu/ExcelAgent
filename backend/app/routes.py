from pathlib import Path
from flask import json, request, jsonify, send_file, url_for
from . import app
from app.agent.agent import chat_with_nutrition_bot
import openpyxl
import tempfile
import os
import uuid
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

temp_files_store = {}

@app.route('/')
def home():
    return "Hello, Flask is running!"

@app.route('/chat', methods=['POST'])
def handle_chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        history = data.get('history', [])
        
        bot_response, file_info = chat_with_nutrition_bot(user_message, history)

        response = {"response": bot_response}


        logging.info(f"FILENAME {file_info}")

        if file_info:
            file_id = store_temp_file(file_info["path"], file_info.get("name"))
            response["download_url"] = url_for("download_file", file_id=file_id, _external=True)
            response["filename"] = file_info.get("name", "download")

        return jsonify(response)
    except Exception as e:
        logging.info("ERROR: ", e)
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
            logging.info(f"Processing file: {file.filename if file else 'None'}")
            extension = Path(file.filename).suffix.lower() if file else ''
                
            with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as temp_file:
                file.save(temp_file.name)
                logging.info(f"File saved to temporary location: {temp_file.name}")
                temp_file_paths[file.filename] = temp_file.name
        

        enhanced_user_message = f"{user_message} Files: "
        for file in temp_file_paths:
            enhanced_user_message += f"{file} at {temp_file_paths[file]}, "
        logging.info(f"Enhanced user message: {enhanced_user_message}")


        bot_response, file_info = chat_with_nutrition_bot(enhanced_user_message, history)

        response = {"response": bot_response}

        if file_info:
            file_id = store_temp_file(file_info["path"], file_info.get("name"))
            response["download_url"] = url_for("download_file", file_id=file_id, _external=True)
            response["filename"] = file_info.get("name", "download")


        return jsonify(response)
    except Exception as e:
        logging.error(f"Error in handle_chat_with_files: {e}")
        logging.info(e)
        return jsonify({
            'error': str(e)
        }), 500


@app.route("/download/<file_id>")
def download_file(file_id):
    clean_up_expired_files()

    if file_id not in temp_files_store:
        return jsonify({"Error": "File not found or expired"}), 404
    
    file_info = temp_files_store[file_id]

    if not os.path.exists(file_info["path"]):
        del temp_files_store[file_id]

        return jsonify({"Error": "File not found"}), 404

    try:
        return send_file(
            file_info['path'],
            as_attachment=True,
            download_name=file_info["original_name"]
        )
    except Exception as e:
        logging.warning(f"Error Serving file, {file_info["original_name"]} at path {file_info["path"]}")
        return jsonify({"Error": "File serving file"}), 500 

def generate_file_id():
    '''Generates a unique file ID using UUID4.'''
    return str(uuid.uuid4())


def store_temp_file(file_path, original_name):
    file_id = generate_file_id()
    temp_files_store[file_id] = {
        "path" : file_path,
        "original_name": original_name or os.path.basename(file_path),
        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(hours=24)  # Expires in 1 day
    }

    return file_id

def clean_up_expired_files():
    '''Remove Expired Temp Files'''

    now = datetime.now()

    expired_ids = [file_id for file_id in temp_files_store 
                   if temp_files_store[file_id]["expires_at"] < now]
    
    for id in expired_ids:
        file_info = temp_files_store[id]
        try:
            if os.path.exists(file_info["path"]):
                os.unlink(file_info["path"])
            
        except Exception as e:
            logging.warning(f"Failed to elminate expiring temp file {file_info['path']}")
        
        del temp_files_store[id]

    