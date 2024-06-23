import copy
from estimator import getTargetPriceRevenue
from sconf import Config
from utils import pprint_config
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="usStock target price estimator using sales"
    )
    parser.add_argument("--input_path", "-I", type=str, default="format_sales.yaml")
    args = parser.parse_args()

    # load format file
    cfg = Config(args.input_path)
    print(">> initialized data")
    pprint_config(cfg)
    data = copy.deepcopy(cfg)
    # build estimator
    data = getTargetPriceRevenue(data=data)
    # estimating
    print("\n\n Calculating...")
    data.calc_all()
    pprint_config(data.data)
