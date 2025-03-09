def commit(self):
    import subprocess
    from flask import flash, redirect, url_for
    import os
    import sys

    # Print current working directory for debugging
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    # Print the full path to the file
    file_path = os.path.join(cwd, "app/data", self.filename)
    print(f"Full file path: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    
    # Print the full path without app prefix
    alt_file_path = os.path.join(cwd, "data", self.filename)
    print(f"Alternative file path: {alt_file_path}")
    print(f"Alternative file exists: {os.path.exists(alt_file_path)}")

    try:
        # Get the current branch name
        current_branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            universal_newlines=True
        ).strip()
        
        # Add the file to git - try with the correct path
        file_to_add = "data/" + self.filename if os.path.exists(alt_file_path) else "app/data/" + self.filename
        print(f"Using path for git add: {file_to_add}")
        
        add_result = subprocess.run(
            ["git", "add", file_to_add], 
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Git add result: {add_result.stdout}")
        
        # Commit the changes
        commit_result = subprocess.run(
            ["git", "commit", "-m", f"Update translation file: {self.filename}"], 
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
        
        # Success message
        flash("Changes committed and pushed to GitHub successfully.", "success")
        print("Changes committed and pushed to GitHub successfully.")
    
    except subprocess.CalledProcessError as e:
        error_message = f"An error occurred while committing to GitHub: {e}"
        if e.output:
            error_message += f"\nOutput: {e.output}"
        if e.stderr:
            error_message += f"\nError: {e.stderr}"
        
        flash(error_message, "error")
        print(error_message, file=sys.stderr)
    
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        flash(error_message, "error")
        print(error_message, file=sys.stderr)

    return redirect(url_for('index'))
