def get_repo_name(url):
    if url.endswith(".git"):
        return url[url.rindex("/")+1:url.rindex(".git")]  
    return url[url.rindex("/")+1:]