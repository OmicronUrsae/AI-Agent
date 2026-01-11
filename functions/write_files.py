import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:    
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path

        if not valid_target_file:
            return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)
        if os.path.isdir(target_file):
            return (f'Error: Cannot write to "{target_file}" as it is a directory')

        with open(target_file, 'w') as file:
            file.write(content)
        return (f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return (f"Error: writing to file: {e}")

schema_write_files = types.FunctionDeclaration(
    name="write_files",
    description="Writes content (user input) to a file in the specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write into the file",
            ),
        },
        required=["file_path", "content"]
    ),
)