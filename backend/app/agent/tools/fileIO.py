import requests
import json


def read_file(file_path):
    if not file_path:
        return "No file uploaded."
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"





def create_file(file_name, content, extension):

    with open(f"./createdFiles/{file_name}{extension}", "w") as file:
        file.write(content)
    
    return os.path.abspath(f"./createdFiles/{file_name}{extension}")