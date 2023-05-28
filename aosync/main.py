from dataclasses import asdict

import click
import yaml

from aosync.api import AppOpticsAPI
from aosync.importer import AppOpticsImporter
from aosync.models import Dashboard
from aosync.syncer import AppOpticsSyncer


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
        dashboard: Dashboard = importer.import_dashboard(dashboard_id)
        yaml_dashboard = yaml.dump(asdict(dashboard))
        print(f"Dashboard exported from AppOptics: \n{yaml_dashboard}")
        # Write to the file at the given path
        with open(output, 'w') as file:
            file.write(yaml_dashboard)
    else:
        print("Use --help to retrieve options")


@cli.command()
@click.option('--token', prompt='AppOptics API token', help='Your AppOptics API token.')
@click.option('--input', type=click.Path(exists=True), help='Input YAML file for syncing.')
def sync(token, input):
    if input:
        with open(input, 'r') as input_file:
            dashboard_data = yaml.safe_load(input_file)

            dashboard = Dashboard(**dashboard_data)
            syncer = AppOpticsSyncer(token)
            syncer.sync(dashboard)
    else:
        click.echo('Please provide an input file for sync operation')


cli.add_command(sync)
cli.add_command(pull)

if __name__ == "__main__":
    cli()
