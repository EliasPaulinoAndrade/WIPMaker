from git import Repo

repo_dir = '.'
repo = Repo(repo_dir)
file_list = ["gteste.py"]
commit_message = 'test'
repo.index.add(file_list)
repo.index.commit(commit_message)
origin = repo.remote('origin master')
origin.push()