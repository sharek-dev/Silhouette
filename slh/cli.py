import os
import sys
import click
from os.path import join, isdir
from slh.validation import validate_template_name, validate_project_structure
from slh.factory import create_new_from_local, create_new_from_template, init_template_layout, search_github_for_templates
from slh.download_manager import download_templates_reference
from slh.utils import print_table, print_template_tree

@click.group()
def cli():
    pass

@cli.command(help="Bootstraps a project from local template")
@click.option('--project_name', prompt=True)
@click.argument('template_path', callback=validate_project_structure)
@click.argument('output_dir')
def local(project_name, template_path, output_dir):
    new_dir_name = join(output_dir, project_name)
    if isdir(new_dir_name):
        raise click.BadParameter("Directory {} already exists !".format(new_dir_name))

    click.echo('Create new project from local path {}'.format(template_path))
    create_new_from_local(project_name, template_path, output_dir)
    print_template_tree(new_dir_name)

@cli.command(help="Bootstraps a project from a template published on Github")
@click.option('--project_name', prompt=True)
@click.argument('template', callback=validate_template_name)
@click.argument('output_dir')
def new(project_name, template, output_dir):
    new_dir_name = join(output_dir, project_name)
    if isdir(new_dir_name):
        raise click.BadParameter("Directory {} already exists !".format(new_dir_name))
    
    click.echo('Create new project from remote template {}'.format(template))
    create_new_from_template(project_name, template, output_dir)
    print_template_tree(new_dir_name)

@cli.command(help="Initiate a template directory")
@click.option('--template_name', prompt=True)
@click.argument('output_dir')
def init(template_name, output_dir):
    new_dir_name = join(output_dir, template_name)
    if isdir(new_dir_name):
        raise click.BadParameter("Directory {} already exists !".format(new_dir_name))
    init_template_layout(new_dir_name)
    print_template_tree(new_dir_name)

@cli.command(help="List refrenced templates")
def list():
    click.secho('Listing referenced templates :', fg="yellow")
    templates = download_templates_reference()
    print_table(["name", "description", "url", "author"],templates)


@cli.command(help="List refrenced templates")
def search_github():
    click.echo("Search Github for slh templates")
    templates = search_github_for_templates()
    print_table(["name", "description", "url", "author"],templates)

if __name__== "__main__":
    cli()