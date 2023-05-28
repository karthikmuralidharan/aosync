from dataclasses import asdict

import click
import yaml
from aosync.api import AppOpticsAPI
from aosync.importer import AppOpticsImporter
from aosync.models import Dashboard
from aosync.syncer import AppOpticsSyncer
from aosync.yamlutil import to_yaml


@click.group()
def cli():
    pass


@click.command()
@click.argument('dashboard_id', type=int)
@click.argument('output', type=click.Path())
@click.option('--appoptics_token', envvar='APPOPTICS_TOKEN')
def pull(dashboard_id, output, appoptics_token):
    if dashboard_id and appoptics_token:
        api = AppOpticsAPI(appoptics_token)
        importer = AppOpticsImporter(api)
        dashboard = asdict(importer.import_dashboard(dashboard_id))
        yaml_dashboard = to_yaml(dashboard)
        print(f"Dashboard exported from AppOptics: \n{yaml_dashboard}")
        # Write to the file at the given path
        with open(output, 'w') as file:
            file.write(yaml_dashboard)
    else:
        print("Use --help to retrieve options")


@cli.command()
@click.argument('input', type=click.Path(exists=True))
@click.option('--appoptics_token', envvar='APPOPTICS_TOKEN')
def sync(input, appoptics_token):
    if input:
        with open(input, 'r') as input_file:
            dashboard_data = yaml.safe_load(input_file)
            dashboard = Dashboard.from_dict(dashboard_data)
            api = AppOpticsAPI(appoptics_token)
            syncer = AppOpticsSyncer(api)
            out = asdict(syncer.sync(dashboard))
            yaml_dict = to_yaml(out)
            print(f"Dashboard exported from AppOptics: \n{yaml_dict}")
            # Write to the file at the given path
            with open(input, 'w') as file:
                file.write(yaml_dict)
    else:
        click.echo('Please provide an input file for sync operation')


cli.add_command(sync)
cli.add_command(pull)

if __name__ == "__main__":
    cli()
