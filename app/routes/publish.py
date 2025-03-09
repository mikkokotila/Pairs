def publish(self):

    from utils.get_env_vars import get_env_vars
    from models.publish_to_docs import publish_to_docs

    env_vars = get_env_vars(keys=['service_account_subject', 'service_account_file'],
                            file_name='.env',
                            relative_to_pwd='../../../')

    publish_to_docs(
        '../service-account-file.json',
        env_vars['service_account_subject'],
        self.data.values.tolist(),
        self.selected)

    return '', 204
