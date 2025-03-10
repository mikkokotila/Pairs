def commit(self):

    import subprocess
    import os

    try:
        # Get correct filename without .csv extension
        filename = self.filename.replace('.csv', '') + '.json'
        db_file_path = os.path.join(self.db_path, filename)
        
        subprocess.run(["git", "add", db_file_path], check=True)
        subprocess.run(["git", "commit", "-m", "Autosave commit"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("Changes committed and pushed to GitHub successfully.")
    
    except subprocess.CalledProcessError as e:
        
        print(f"An error occurred while committing to GitHub: {e}")

    return '', 204
