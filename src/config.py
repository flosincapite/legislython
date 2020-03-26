import os
import yaml


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


ROLL_XML_DIR = os.path.join(PROJECT_ROOT, 'data', 'roll_xmls')
VOTE_XML_DIR = os.path.join(PROJECT_ROOT, 'data', 'vote_xmls')


print('Loading config ...')
with open(os.path.join(PROJECT_ROOT, 'config.yml')) as inp:
  yaml_dict = yaml.load(inp)
  AGENT = yaml_dict.get('Agent')
