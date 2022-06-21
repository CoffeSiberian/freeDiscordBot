from pathlib import Path
import json

def getDirt():
    return str(Path(__file__).parents[1])

def getConf():
    return json.load(open(getDirt()+'/config.json'))