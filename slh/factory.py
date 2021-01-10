import os
from os import listdir, mkdir, makedirs
from os.path import isfile, join, isdir, dirname, basename
import tempfile
import shutil
import errno
import stat
import glob
import re
import configparser
import io
from slh.config import ApplicationConfig
from slh.download_manager import clone_repo_locally
from slh.validation import validate_project_structure
from slh.template_engine import TemplateEngine
import click
from slh.utils import FileModifier, TemporaryDirectoryV2
from shutil import copyfile
import requests

def handleRemoveReadonly(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)

def clean_temporary_repo(path):
    repo_main_dir = os.listdir(path)[0]
    shutil.rmtree(join(path, repo_main_dir), ignore_errors=False, onerror=handleRemoveReadonly)

def copy_file(src, dst, template_engine):
    dst_root = dirname(dst)
    if not os.path.exists(dst_root):
        makedirs(dst_root)
    
    original_file = open(src, 'r')
    content = original_file.read()
    rendered_content = template_engine.eval_str(content)
    with open(dst, 'w') as f:
        f.write(rendered_content)

def render_file_paths(src_paths, vars):
    te = TemplateEngine(vars)
    return [ te.eval_str(src)  for src in src_paths ]

def create_new_from_local(name, template_path, output_dir):
    app_config = ApplicationConfig(join(template_path, "default.properties"))
    template_vars = app_config.get_vars()

    for k,v in template_vars.items():
        template_vars[k] = click.prompt(k, default=v)
    template_vars["name"] = name
    
    te = TemplateEngine(template_vars)

    files = [ f for f in glob.glob(join(template_path, "project") + "\\**/*", recursive=True) if isfile(f) ]
    files_to_dst = { f:te.eval_str( f.replace(join(template_path, "project"), "") ) for f in files }

    base_dir = join(output_dir, name)
    mkdir(base_dir)
    
    for src, dst in files_to_dst.items():
        copy_file(src, base_dir + dst, te)

def create_new_from_template(name, template, output_dir):
    """ Creates a new project from remote template. """
    repo_url = "https://github.com/{}.git".format(template)
    repo_user = template.split("/")[0]
    repo_name = template.split("/")[1]

    with TemporaryDirectoryV2(prefix=".", dir=os.getcwd()) as tmpdirname:
        clone_repo_locally(tmpdirname, repo_url)
        local_repo_path = join(tmpdirname, repo_name)
        click.echo("Remote Repository cloned.")
        validate_project_structure(None, None, local_repo_path)
        create_new_from_local(name, local_repo_path, output_dir)

def init_template_layout(output_dir):
    mkdir(output_dir)
    mkdir(join(output_dir, "project"))

    with open(join(output_dir, "default.properties"), "w") as f:
        f.write("[VARS]\nsample=value")

def search_github_for_templates():
    from rich.progress import Progress
    url = "https://api.github.com/search/repositories"
    params = {"q": "slh", "per_page": 50, "page": 0}
    result = requests.get(url, params = params).json()
    if "total_count" not in result:
        raise Exception("Github API Has a rate limitation: {}".format(result["message"]))
    total_count = result["total_count"]
    scanned_items = 0
    _page = 1

    templates = []

    with Progress() as progress:
        search_task = progress.add_task("[red]Scanning repositories...", total=total_count)
        while(True):
            params["per_page"] = 50
            params["page"] = _page
            result = requests.get(url, params = params).json()
            
            if "items" not in result or len(result["items"]) == 0:
                break
            
            for repo in result["items"]:
                if not repo["full_name"].endswith(".slh"):
                    continue

                templates.append(
                    {
                        "name": repo["full_name"], 
                        "author": repo["owner"]["login"], 
                        "description": repo["description"], 
                        "url": repo["html_url"]
                    }
                )
            
            scanned_items += len(result["items"])
            _page += 1
            progress.update(search_task, advance=scanned_items)
    
    return templates