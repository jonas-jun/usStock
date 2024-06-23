import copy
from sconf import Config
import argparse
from utils import pprint_config
from estimator import getTargetPrice, getTargetPriceRevenue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="usStock target price estimator")
    parser.add_argument("--input_path", "-I", type=str, default="format_sales.yaml")
    args = parser.parse_args()

    # load format file
    cfg = Config(args.input_path)
    print(">> initialized data")
    pprint_config(cfg)
    data = copy.deepcopy(cfg)

    # build estimator
    task = data.task.lower()
    assert task in {"eps", "sales"}
    if task == "eps":
        data = getTargetPrice(data=data)
    else:
        data = getTargetPriceRevenue(data=data)

    # estimating
    print("\n\n>> Calculating...")
    data.calc_all()
    pprint_config(data.data)
