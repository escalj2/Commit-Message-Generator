

"""diff_msg = subprocess.run(["git", "diff", "--staged" ], capture_output=True, text=True)
if diff_msg.stdout == '':
    print("Nothing currently staged")
print(diff_msg)"""

from google import genai
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the key using os.getenv()
api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="Explain how AI works in a few words"
)
print(interaction.output_text)
