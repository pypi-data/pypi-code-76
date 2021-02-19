from gitlab_operations.gitinstance import GitInstance


class UserConfig(GitInstance):
    def __init__(self):
        GitInstance.__init__(self)
        if not self.token == 'False':
            pass
        else:
            print('[x] access token not set')
            self.user_action()

    def user_action(self):
        try:
            print('\n[===============|GitLab User Config|===============]')
            url = input('\nEnter GitLab URL(default is https://gitlab.com/): ')
            access_token = input('Enter AccessToken (default is False): ')
            print('\n[+] setting git url: {}'.format(url))
            print('[+] setting access token: {}'.format(access_token))
            if url:
                self._git_url = url
            else:
                print('[x] setting default gitlab url')
            if access_token:
                self._access_token = access_token
            else:
                print('[x] setting access token "False"')
            self._default_config()
        except KeyboardInterrupt:
            print('\n[x] good bye..\n')
            exit(0)
