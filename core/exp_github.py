from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

def update():

     access_tocken = os.getenv("GITHUB_ACCESS_TOKEN")
     github_repo = "data"
     git_branch = "main"
     initial_file = "TechCrunch.json"
     folder_empl_in_git = "TechCrunch.json"

     g = Github(access_tocken)
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
     # Upload to github
     if folder_empl_in_git in all_files:
         contents = repo.get_contents(folder_empl_in_git)
         repo.update_file(contents.path, "committing files", content, contents.sha, branch=git_branch)
         return folder_empl_in_git + ' UPDATED'
     else:
         repo.create_file(folder_empl_in_git, "committing files", content, branch=git_branch)
         return folder_empl_in_git + ' CREATED'