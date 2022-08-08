import yaml

def read_config_file(config_filename):
    with open(config_filename, "r") as config_file:
        return yaml.load(config_file, yaml.FullLoader)