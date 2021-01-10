from os import listdir
from os.path import isfile, join, isdir, exists
import click

# Validates if the template name ends with the silhouette default suffix.
def validate_template_name(ctx, param, value):
    if value.endswith(".slh"):
        return value
    else :
        raise click.BadParameter('template name should ends with slh. Example: helkaroui/sample.slh')

# Should validate if the project contains :
# - default.properties files
# - project            firectory
def validate_project_structure(ctx, param, value):
    files = listdir(value)
    if "project" not in files or not isdir( join(value, "project") ):
        raise click.BadParameter("Project directory is not found")
    if "default.properties" not in files or not isfile( join(value, "default.properties") ):
        raise click.BadParameter("default.properties is not found is root project")
    return value