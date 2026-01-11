import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key detected.")
 
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Create prompt based on user input

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    client = genai.Client(api_key=api_key)

    final_response_obtained = False
    for step in range(20):
        response = client.models.generate_content(
            model = "gemini-2.5-flash",
            contents = messages,
            config = types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
        )
        if not response.candidates:
            raise Exception("Error: No candidates returned from model.")
        
        for candidate in response.candidates:
            messages.append(candidate.content)

        if response.usage_metadata is None:
            raise RuntimeError("Error: No usage metadata detected.")

        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"User prompt: {args.user_prompt}")

        function_responses = []
        if response.function_calls:
            for call in response.function_calls:
                call_result = call_function(call, verbose=args.verbose)

                if not call_result.parts:
                    raise Exception("Error: No parts returned from function call.")
            
                if call_result.parts[0].function_response is None:
                    raise Exception("Error: No function response returned from function call.")
            
                if call_result.parts[0].function_response.response is None:
                    raise Exception("Error: No response returned from function call.")
            
                if args.verbose:
                    print(f"-> {call_result.parts[0].function_response.response}")
                
                function_responses.append(call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            print(response.text)
            final_response_obtained = True
            break

    if not final_response_obtained:
        sys.exit(f"Error: Iteration limit reached without producing a final response.", 1)

if __name__ == "__main__":
    main()
