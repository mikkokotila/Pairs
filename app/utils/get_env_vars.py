def get_env_vars(keys: list,
                 file_name: str,
                 relative_to_pwd: str) -> dict:

    out = {}

    import os
    from dotenv import load_dotenv

    path_to_file = os.path.join(os.getcwd(), relative_to_pwd)
    parent_path = os.path.abspath(path_to_file)
    env_file_path = parent_path + '/' + file_name

    # Check if the .env file exists
    if os.path.exists(env_file_path):
        load_dotenv(env_file_path)
    else:
        print(f"Warning: Environment file {env_file_path} not found.")
        return {key: None for key in keys}

    for key in keys:
        out[key] = os.getenv(key)

    return out
