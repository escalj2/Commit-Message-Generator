
import subprocess
from google import genai
import os
from dotenv import load_dotenv

diff_msg = subprocess.run(["git", "diff", "--staged" ], capture_output=True, text=True)
if diff_msg.stdout == '':
    print("Nothing currently staged")
print(diff_msg)

# Load the .env file and access the key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents=f"Generate a git commit message based on this git-diff --staged output: \n\n{diff_msg}",
)
print(response.text)