from mxdevtool.data.repositories.repo import DefaultRepository


def init():
    global repo_list
    global default_repo
    repo_list = []
    default_repo = DefaultRepository()

def get_repo():
    try:
        return repo_list[0]
    except:
        return default_repo


def set_repo(repo):
    repo_list.clear()
    repo_list.append(repo)