import copy
from sconf import Config
import argparse
from utils import pprint_config
from estimator import getTargetPrice

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="usStock target price estimator")
    parser.add_argument("--input_path", "-I", type=str, default="format.yaml")
    args = parser.parse_args()

    # load format file
    cfg = Config(args.input_path)
    print(">> initialized data")
    pprint_config(cfg)
    data = copy.deepcopy(cfg)
    # build estimator
    data = getTargetPrice(data=data)
    # estimating
    print("\n\n>> Calculating...")
    data.calc_all()
    pprint_config(data.data)
