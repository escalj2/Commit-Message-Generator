from git import Repo

repo = Repo(r'C:\Users\escal\Projects\Commit Message Generator')
diff_output = repo.git.diff('--staged')
print(diff_output)