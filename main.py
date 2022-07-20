import json, pathlib, utils
from multitools import multitools

def run():
    config = json.load(open(pathlib.Path(__file__).parent / "config.json"))
    args = utils.build_args(config)
    tool = multitools(args)
    tool.run()

if __name__ == "__main__":
    run()
