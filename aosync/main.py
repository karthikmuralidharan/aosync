from dataclasses import asdict

import click
import yaml

from aosync.importer import AppOpticsImporter
from aosync.models import Dashboard


@click.command()
@click.option('--config', type=click.Path(exists=True, readable=True))
@click.option('--import_dashboard', type=int)
@click.option('--appoptics_token', envvar='APPOPTICS_TOKEN')
@click.option('--output', type=click.Path())
def main(config, import_dashboard, appoptics_token, output):
    if config:
        with open(config) as file:
            yaml_config = yaml.load(file, Loader=yaml.FullLoader)
            dashboard = Dashboard.from_dict(yaml_config)
            print(f"Dashboard loaded from config: {dashboard}")
    elif import_dashboard and appoptics_token:
        importer = AppOpticsImporter(appoptics_token, import_dashboard)
        dashboard: Dashboard = importer.get_dashboard()
        yaml_dashboard = yaml.dump(asdict(dashboard))
        print(f"Dashboard exported from AppOptics: \n{yaml_dashboard}")
        # Write to the file at the given path
        with open(output, 'w') as file:
            file.write(yaml_dashboard)
    else:
        print("Use --help to retrieve options")


if __name__ == "__main__":
    main()
