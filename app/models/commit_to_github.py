import subprocess
import sys
import os

def commit_to_github(filename):
    """
    Commits and pushes changes to a file to GitHub.
    
    Args:
        filename (str): The name of the file to commit.
        
    Returns:
        tuple: (success, message) where success is a boolean indicating if the operation was successful,
               and message is a string with details about the operation.
    """
    try:
        # Print current working directory for debugging
        cwd = os.getcwd()
        print(f"Current working directory: {cwd}")
        
        # Check which path exists
        app_data_path = os.path.join(cwd, "app/data", filename)
        data_path = os.path.join(cwd, "data", filename)
        
        file_to_add = "data/" + filename if os.path.exists(data_path) else "app/data/" + filename
        print(f"Using path for git add: {file_to_add}")
        
        # Get the current branch name
        current_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            universal_newlines=True
        ).strip()
        
        # Add the file to git
        add_result = subprocess.run(
            ["git", "add", file_to_add], 
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Git add result: {add_result.stdout}")
        
        # Commit the changes
        commit_result = subprocess.run(
            ["git", "commit", "-m", f"Update translation file: {filename}"], 
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Git commit result: {commit_result.stdout}")
        
        # Push the changes to the current branch
        push_result = subprocess.run(
            ["git", "push", "origin", current_branch], 
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Git push result: {push_result.stdout}")
        
        success_message = "Changes committed and pushed to GitHub successfully."
        print(success_message)
        return True, success_message
    
    except subprocess.CalledProcessError as e:
        error_message = f"An error occurred while committing to GitHub: {e}"
        if hasattr(e, 'output') and e.output:
            error_message += f"\nOutput: {e.output}"
        if hasattr(e, 'stderr') and e.stderr:
            error_message += f"\nError: {e.stderr}"
        
        print(error_message, file=sys.stderr)
        return False, error_message
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message, file=sys.stderr)
        return False, error_message