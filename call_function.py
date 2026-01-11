from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.write_files import write_file, schema_write_files
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.run_python_file import run_python_file, schema_run_python_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_write_files,
        schema_get_file_content,
        schema_run_python_file,
    ]
)

function_mapping = {
    "get_files_info": get_files_info,
    "write_files": write_file,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
}

def call_function(function_call: types.FunctionCall, verbose=False):
    function_name = function_call.name or ""
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"
    
    if function_name not in function_mapping:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    function_result = function_mapping[function_name](**args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )
    