import requests
import json
import os
import tempfile

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

    # with open(f"./createdFiles/{file_name}{extension}", "w") as file:
    #     file.write(content)

    path = None
    with tempfile.NamedTemporaryFile(mode="w", suffix=extension, delete=False) as file:
        file.write(content)
        path = file.name

    print(path)
    return path


# if __name__ == "__main__":
#     create_file("Opa", "Hello World", ".txt")