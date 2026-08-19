import subprocess

diff_msg = subprocess.run(["git", "diff", "--staged" ], capture_output=True, text=True)
print(diff_msg)