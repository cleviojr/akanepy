import yaml

file = open('variables.yaml', 'r')
CONFIG = yaml.load(file)
file.close()
