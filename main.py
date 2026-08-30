import subprocess
from google import genai
import os
from dotenv import load_dotenv
from google.genai import errors
import time

def generate_commit_message(diff_output, max_retries=3):
    prompt = (
        f"Generate 1 conventional commit message based on this git diff --staged output:\n\n"
        f"{diff_output}\n\n"
        f"Return only the commit message text with no special markdown formatting. "
        f"This will be directly committed and pushed."
    )

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt,
            )
            return response.text.strip()

        except errors.ServerError as e:
            print(f"Server busy (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                time.sleep(2 * attempt)
            else:
                print("Gemini is unavailable right now. Try again later.")
                return None

        except errors.ClientError as e:
            print(f"Request error: {e}")
            return None

        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    return None


diff_msg = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True)

if diff_msg.stdout == '':
    print("Nothing currently staged")
else:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    commit_message = generate_commit_message(diff_msg.stdout)

    if commit_message is None:
        print("Couldn't generate a commit message. Exiting.")
    else:
        print(commit_message)
        choice = input("Accept response? (y/n)\n>")

        if choice == 'y':
            subprocess.run(["git", "commit", "-m", commit_message])

            push_option = input("Push? (y/n)\n>")
            if push_option == 'y':
                subprocess.run(["git", "push"])