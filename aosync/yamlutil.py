from typing import Dict

import yaml


def remove_none_values(data):
    if isinstance(data, dict):
        return {k: remove_none_values(v) for k, v in data.items() if v is not None}
    elif isinstance(data, list):
        return [remove_none_values(i) for i in data if i is not None]
    else:
        return data


def to_yaml(d: Dict):
    cleaned = remove_none_values(d)
    yaml_dashboard = yaml.dump(cleaned)
    return yaml_dashboard
