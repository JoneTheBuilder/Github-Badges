import os
import time

# Function to execute shell commands
def execute_command(command):
    return os.system(command)

# Function to create a file
def create_file(filename, content):
    with open(filename, 'w') as f:
        f.write(content)

# Number of times to repeat the process
N = 5

# Main loop
for i in range(N):
    # Create a branch
    branch_name = f"branch_{i}"
    execute_command(f"git checkout -b {branch_name}")
    
    # Create a file
    filename = f"file_{i}.txt"
    file_content = f"This is file {i}."
    create_file(filename, file_content)
    
    # Add and commit changes
    execute_command("git add .")
    execute_command(f"git commit -m 'Add {filename}'")
    
    # Push changes to remote
    execute_command(f"git push origin {branch_name}")
    
    # Create a pull request
    pull_request_title = f"Pull request {i}"
    pull_request_body = f"This pull request adds file {filename}."
    execute_command(f"gh pr create --title '{pull_request_title}' --body '{pull_request_body}' --base main --head {branch_name}")
    
    # Wait for a few seconds before creating another pull request
    time.sleep(5)

# Merge pull requests
execute_command("gh pr merge --auto")

# Delete merged branches
for i in range(N):
    branch_name = f"branch_{i}"
    execute_command(f"git branch -d {branch_name}")

# Prune remote branches
execute_command("git fetch -p")
