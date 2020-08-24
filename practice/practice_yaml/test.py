import yaml
import sys


def foo(conf_path):
    with open(conf_path, "rt") as stream:
        raw_yaml = yaml.safe_load(stream)
    return raw_yaml


raw_yaml = foo(sys.argv[1])
print(raw_yaml)
print(yaml.dump(raw_yaml, explicit_start=True))