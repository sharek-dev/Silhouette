import os
from os import listdir
from os.path import isfile, join, isdir
import git
import tempfile
import shutil
import errno
import stat
import glob
import re

# This function clones a remote repository to a temporary folder, and return it's path.
def clone_repo_locally(tmpdirname, repository):
    """ """
    git.Git(tmpdirname).clone(repository)
    return tmpdirname

def handleRemoveReadonly(func, path, exc):
        os.chmod(path, stat.S_IWRITE)
        func(path)

def clean_temporary_repo(path):
        repo_main_dir = os.listdir(path)[0]
        shutil.rmtree(join(path, repo_main_dir), ignore_errors=False, onerror=handleRemoveReadonly)

def create_new_from_template(template, outputDir):
    """ Creates a new project from remote template. """
    repo_url = "https://github.com/{}.git".format(template)
    repo_user = template.split("/")[0]
    repo_name = template.split("/")[1]

    with tempfile.TemporaryDirectory(prefix=".", dir=os.getcwd()) as tmpdirname:
        clone_repo_locally(tmpdirname, repo_url)
        local_repo_path = join(tmpdirname, repo_name)
        print(local_repo_path)
        files = [f.replace(local_repo_path, "") for f in glob.glob(local_repo_path + "\\**/*", recursive=True) if isfile(f) ]
        
        print(files)
        
        clean_temporary_repo(tmpdirname)





class Template():
    def __init__(self, template):
        self.template = template
    def __enter__(self):
        self.fd = open(self.dev, MODE)
        return self.fd
    def __exit__(self, type, value, traceback):
        close(self.fd)