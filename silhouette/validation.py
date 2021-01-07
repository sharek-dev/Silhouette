import click

def validate_template_name(ctx, param, value):
    if value.endswith("slh3"):
        return value
    else :
        raise click.BadParameter('template name should ends with slh3. Example: helkaroui/sample.slh3')