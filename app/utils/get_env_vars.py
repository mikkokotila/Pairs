def get_env_vars(keys: list,
                 file_name: str,
                 relative_to_pwd: str) -> dict:

    out = {}

    import os
    from dotenv import load_dotenv

    path_to_file = os.path.join(os.getcwd(), relative_to_pwd)
    parent_path = os.path.abspath(path_to_file)

    load_dotenv(parent_path + '/' + file_name)

    for key in keys:

        out[key] = os.getenv(key)

    return out
