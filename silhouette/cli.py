import os
import sys
import click
from silhouette.validation import validate_template_name
from silhouette.factory import *

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

@cli.command()
@click.option('--name', prompt=True)
@click.argument('template') # callback=validate_template_name
@click.argument('output_dir')
def new(name, template, output_dir):
    click.echo('New from template {}'.format(template))
    create_new_from_template(name, template, output_dir)

@cli.command()
def init():
    click.echo('Dropped the database')

@cli.command()
def list():
    click.echo('Listing referenced templates')
    

if __name__== "__main__":
    cli()