# When Git is not avalable o the system, switch to old way: 
# wget the repo zip file: http://github.com/[username]/[repo]/archive/master.zip


# This function clones a remote repository to a temporary folder, and return it's path.
def clone_repo_locally(tmpdirname, repository):
    """ """
    try:
        import git
        git.Git(tmpdirname).clone(repository)
    except ImportError :
        download_zip_file()
    return tmpdirname


def download_zip_file(tmpdirname, repository):
    pass
