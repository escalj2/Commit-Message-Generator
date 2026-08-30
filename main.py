import subprocess
from google import genai
import os
from dotenv import load_dotenv
from google.genai import errors


diff_msg = subprocess.run(["git", "diff", "--staged" ], capture_output=True, text=True)
if diff_msg.stdout == '':
    print("Nothing currently staged")
else:
    try:
        # Load the .env file and access the key
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.7-flash",
            contents=f"Generate 1 conventional commit message based on this git-diff --staged output: \n\n{diff_msg.stdout}. Return only the commit message text with no special markdown text. This will be directly commited and pushed.",
        )
        os.system('cls')
        print(response.text)
    except errors.ServerError as e:
        print(e.message)
    #except Exception as e: print(e)
    else:
        choice = input("Accept response? (y/n)\n>")
        if choice == 'y':
            subprocess.run(["git", "commit", "-m", response.text], capture_output=True, text=True)
            push_option = input("Push? (y/n)\n>")
            if choice == 'y':
                subprocess.run(["git", "push"], capture_output=True, text=True)