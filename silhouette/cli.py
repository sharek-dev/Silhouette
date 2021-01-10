import os
import sys
import click
from silhouette.validation import validate_template_name, validate_project_structure
from silhouette.factory import create_new_from_local, create_new_from_template
from silhouette.download_manager import download_templates_reference
from silhouette.utils import print_table, print_template_tree

@click.group()
def cli():
    """
    Author: Hamza EL KAROUI
    """
    pass

@cli.command()
@click.option('--name', prompt=True)
@click.argument('template_path', callback=validate_project_structure)
@click.argument('output_dir')
def local(name, template_path, output_dir):
    click.echo('New from local path {}'.format(template_path))
    create_new_from_local(name, template_path, output_dir)
    print_template_tree(output_dir)

@cli.command()
@click.option('--name', prompt=True)
@click.argument('template', callback=validate_template_name)
@click.argument('output_dir')
def new(name, template, output_dir):
    click.echo('New from template {}'.format(template))
    create_new_from_template(name, template, output_dir)
    print_template_tree(output_dir)

@cli.command()
def init():
    click.echo('Dropped the database')

@cli.command()
def list():
    click.secho('Listing referenced templates :', fg="yellow")
    templates = download_templates_reference()
    print_table(["name", "description", "url", "author"],templates)

if __name__== "__main__":
    cli()