import os
from config import char_limit
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_path = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_path, file_path))
    valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path

    if not valid_target_file:
        return (f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    
    if not os.path.isfile(target_file):
        return (f'Error: File not found or is not a regular file: "{file_path}"')
    
    with open(target_file, 'r') as file:
        content = file.read(char_limit)
        if file.read(1):
            content += f'[...File "{target_file}" truncated at {char_limit} characters]'
    return(content)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)