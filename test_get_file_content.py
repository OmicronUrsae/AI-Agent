from functions.get_file_content import get_file_content

try:
    get_file_content("calculator", "main.py")
except Exception as e:
    print(e)
try:
    get_file_content("calculator", "pkg/calculator.py")
except Exception as e:
    print(e)
try:
    get_file_content("calculator", "/bin/cat")
except Exception as e:
    print(e)
try:
    get_file_content("calculator", "pkg/does_not_exist.py")
except Exception as e:
    print(e)