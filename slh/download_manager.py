import requests

# When Git is not avalable o the system, switch to old way: 
# wget the repo zip file: http://github.com/[username]/[repo]/archive/master.zip


# This function clones a remote repository to a temporary folder, and return it's path.
def clone_repo_locally(tmpdirname, repository):
    """ """
    try:
        import git
        print("loading git")
        print("clone git repo {}".format(repository))
        print("to temporary directory {}".format(tmpdirname))
        git.Git(tmpdirname).clone(repository)
    except ImportError :
        print("error on import. Downloading zip version")
        # Todo: Handle the case when git is not installed on the system
        download_zip_file()
    return tmpdirname

def download_zip_file(tmpdirname, repository):
    # Todo: to implement
    pass


def download_templates_reference():
    file_url = "https://raw.githubusercontent.com/sharek-org/Silhouette/main/ref/templates.json"
    response = requests.get(file_url)
    return response.json()
