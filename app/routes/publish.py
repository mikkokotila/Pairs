def publish(self):

    from utils.get_env_vars import get_env_vars
    from models.publish_to_docs import publish_to_docs

    env_vars = get_env_vars(keys=['google_service_account_subject',
                                  'google_service_account_file'],
                            file_name='.env',
                            relative_to_pwd='../../../')
    
    # Convert DataFrame to list format expected by publish_to_docs
    data_list = self.data[['source_string', 'target_string', 'style']].values.tolist()

    publish_to_docs(
        '../service-account-file.json',
        env_vars['service_account_subject'],
        data_list,
        self.selected)

    return '', 204
