from json import load
import os
config = load(open(os.path.dirname(os.path.realpath(__file__))+'/config/default.json', 'rb'))