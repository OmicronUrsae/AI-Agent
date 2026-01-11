import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path

        if not valid_target_file:
            return (f'Cannot execute "{file_path}" as it is outside the permitted working directory')
    
        if not os.path.isfile(target_file):
            return (f'"{file_path}" does not exist or is not a regular file')
        
        extension = target_file.split('.')[-1]
        if extension != 'py':
            return (f'"{file_path}" is not a Python file')
    
        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(
            command,
            cwd=abs_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        str_output = []
        if completed_process.returncode != 0:
            str_output.append(f"Process exited with code {completed_process.returncode}")
    
        if not completed_process.stdout and not completed_process.stderr:
            str_output.append("No output produced")
        else:
            if completed_process.stdout:
                str_output.append(f"STDOUT:\n{completed_process.stdout}")
            if completed_process.stderr:
                str_output.append(f"STDERR:\n{completed_process.stderr}")
            return ("\n".join(str_output))
    except Exception as e:
        return (f"Error: {e}")

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified directory relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional list of arguments to pass to the Python programme",
            ),
        },
        required=["file_path"]
    ),
)