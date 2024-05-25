import subprocess
import random
import string

# Function to replace the content of a file with a random string
def replace_with_random_string(file_path):
    try:
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))  # Generating a random string of length 10

        with open(file_path, 'w') as file:
            file.write(random_string)
        
        print("Content replaced with random string successfully.")
    
    except FileNotFoundError:
        print("File not found.")
    except Exception as e:
        print(f"An error occurred while replacing content: {e}")

# Function to create a new branch
def create_git_branch(branch_name):
    try:
        # Check if the branch already exists
        branches = subprocess.run(["git", "branch"], capture_output=True, text=True)
        if branch_name not in branches.stdout:
            # Run the git command to create a new branch
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            print(f"Branch '{branch_name}' created successfully.")
        else:
            print(f"Branch '{branch_name}' already exists.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating branch: {e}")

# Function to create a pull request
def create_pull_request(base_branch, head_branch, title, description):
    try:
        # GitHub CLI command to create a pull request
        command = ["gh", "pr", "create", "--base", base_branch, "--head", head_branch, "--title", title, "--body", description]

        # Run the command
        subprocess.run(command, check=True)
        print("Pull request created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating pull request: {e}")

# Function to merge a pull request
def merge_pull_request(branch_name):
    try:
        # Git command to merge a pull request
        command = ["git", "merge", branch_name]

        # Run the command
        subprocess.run(command, check=True)
        print(f"Pull request '{branch_name}' merged successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while merging pull request: {e}")

# Function to delete a branch
def delete_git_branch(branch_name):
    try:
        # Check if the branch is checked out
        status = subprocess.run(["git", "status"], capture_output=True, text=True)
        if f"On branch {branch_name}" in status.stdout:
            # Switch to another branch before deleting
            subprocess.run(["git", "checkout", "-"], check=True)
        
        # Git command to delete a branch
        subprocess.run(["git", "branch", "-D", branch_name], check=True)
        print(f"Branch '{branch_name}' deleted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while deleting branch: {e}")

# Function to add a remote
def add_git_remote(remote_name, remote_url):
    try:
        # Check if the remote already exists
        remotes = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        if remote_name not in remotes.stdout:
            # Git command to add a remote
            command = ["git", "remote", "add", remote_name, remote_url]

            # Run the command
            subprocess.run(command, check=True)
            print(f"Remote '{remote_name}' added successfully.")
        else:
            print(f"Remote '{remote_name}' already exists.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while adding remote: {e}")

# Function to repeat the process N times
def repeat_process(N):
    for _ in range(N):
        # File path
        file_path = "temp.txt"
        replace_with_random_string(file_path)

        # New branch name
        new_branch_name = "new-branch"
        create_git_branch(new_branch_name)

        # Add remote
        remote_name = "origin"
        remote_url = "git@github.com:JoneTheBuilder/Github-Badges.git"
        add_git_remote(remote_name, remote_url)

        # Base branch, pull request title, and description
        base_branch = "main"
        head_branch = new_branch_name
        title = "Title of your pull request"
        description = "Description of your pull request"

        # Commit changes
        subprocess.run(["git", "add", "."])
        subprocess.run(["git", "commit", "-m", "Commit message"])
        
        # Pull changes from remote repository
        subprocess.run(["git", "pull", "origin", base_branch])
        
        # Push changes to remote repository
        subprocess.run(["git", "push", "origin", new_branch_name])  

        # Create pull request
        create_pull_request(base_branch, head_branch, title, description)

        # Merge pull request
        merge_pull_request(head_branch)

        # Delete branch
        delete_git_branch(head_branch)

# Repeat the process 5 times
repeat_process(10)
