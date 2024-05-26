from tqdm import tqdm
import subprocess
import sys
import json
import time

def run_command(command):
    """Run a shell command and return the output."""
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    if result.returncode != 0:
        print(f"Error running command: {command}")
        print(result.stderr)
        return None
    return result.stdout

def branch_exists(branch_name):
    """Check if a branch already exists."""
    branches = run_command("git branch --list")
    if branches:
        return branch_name in branches.split()
    return False

def delete_branch(branch_name):
    """Delete a branch if it exists locally and remotely."""
    if branch_exists(branch_name):
        run_command("git checkout main")  # Switch to main branch
        run_command(f"git branch -D {branch_name}")
        run_command(f"git push origin --delete {branch_name}")

def create_branch(branch_name):
    """Create a new git branch."""
    run_command(f"git checkout -b {branch_name}")

def make_changes(branch_name):
    """Make some changes and commit them."""
    with open("change.txt", "a") as f:
        f.write(f"Changes in branch {branch_name}\n")
    run_command("git add change.txt")
    run_command(f"git commit -m 'Changes in branch {branch_name}'")

def push_branch(branch_name):
    """Push the branch to the remote repository."""
    run_command(f"git push origin {branch_name}")

def create_pull_request(branch_name):
    """Create a pull request using GitHub CLI."""
    for attempt in range(3):  # Retry up to 3 times
        result = run_command(f"gh pr create --base main --head {branch_name} --title 'PR from {branch_name}' --body 'This is an automated PR from {branch_name}'")
        if result is not None:
            return
        print(f"Retrying PR creation for {branch_name}...")
        time.sleep(5 * (attempt + 1))  # Exponential backoff

def merge_pull_request(pr_number):
    """Merge the pull request using GitHub CLI."""
    result = run_command(f"gh pr merge {pr_number} --squash --delete-branch")
    if result is None:
        print(f"Skipping PR #{pr_number} due to merge conflicts or other issues.")

def main(n):
    for i in tqdm(range(1, n + 1), leave=False, desc="Pull requests:"):
        branch_name = f"feature-branch-{i}"
        delete_branch(branch_name)  # Ensure the branch does not exist
        create_branch(branch_name)
        make_changes(branch_name)
        push_branch(branch_name)
        create_pull_request(branch_name)
        time.sleep(2)  # Delay to avoid hitting rate limit
    
    prs = run_command("gh pr list --state open --json number")
    if prs:
        pr_numbers = [pr["number"] for pr in json.loads(prs)]
        
        for pr_number in pr_numbers:
            merge_pull_request(pr_number)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_and_merge_prs.py <number_of_prs>")
        sys.exit(1)

    num_of_prs = int(sys.argv[1])
    main(num_of_prs)
