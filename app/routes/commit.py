def commit(self):

    import subprocess

    try:
        subprocess.run(["git", "add", "data/" + self.filename], check=True)
        subprocess.run(["git", "commit", "-m", "Autosave commit"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("Changes committed and pushed to GitHub successfully.")
    
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while committing to GitHub: {e}")

    return '', 204
