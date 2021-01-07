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
@click.argument('template', callback=validate_template_name)
def local(template):
    click.echo('New from template {}'.format(template))


@cli.command()
@click.option('--outputDir', type=click.Path(exists=False), default=None)
@click.argument('template') # callback=validate_template_name
def new(outputdir, template):
    click.echo('New from template {}'.format(template))
    create_new_from_template(template, outputdir)


@cli.command()
def init():
    click.echo('Dropped the database')


if __name__== "__main__":
    cli()