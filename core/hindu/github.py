import os
from datetime import date

from dotenv import load_dotenv
from github import Github

load_dotenv()

def update():
    target_date = date.today()
    access_token = os.getenv("GITHUB_ACCESS_TOKEN")
    github_repo = "data"
    git_branch = "main"
    initial_file = f"{target_date}_TechCrunch.json"
    folder_in_git = f"{target_date}_TechCrunch.json"

    g = Github(access_token)
    repo = g.get_user().get_repo(github_repo)
    all_files = []
    contents = repo.get_contents("")
    
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="', '').replace('")', ''))

    with open(initial_file, 'r') as file:
        content = file.read()

    # Upload to GitHub
    if folder_in_git in all_files:
        contents = repo.get_contents(folder_in_git)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch=git_branch)
        print(folder_in_git + ' UPDATED')
    else:
        repo.create_file(folder_in_git, "committing files", content, branch=git_branch)
        print(folder_in_git + ' CREATED')

    # Remove the file from the system after successful upload
    os.remove(initial_file)