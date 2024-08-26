import subprocess

# Command to run uvicorn
uvicorn_command = "uvicorn main:app --reload --host 172.18.100.240 --port 6969"

# Run the command in the Python terminal
subprocess.run(["python", "-m", "uvicorn", "main:app", "--reload", "--host", "172.18.100.33", "--port", "6969"])
