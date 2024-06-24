import os
import copy
from datetime import datetime
from sconf import Config
import argparse
from utils import pprint_config, append_jsonl, export_jsonl
from estimator import getTargetPrice, getTargetPriceRevenue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="usStock target price estimator")
    parser.add_argument("--input_path", "-I", type=str, default="format_sales.yaml")
    parser.add_argument("--out_path", "-O", type=str, default=None)
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

    # exporting
    now = datetime.now()
    data.data["date"] = now.strftime("%y%m%d-%a-%H:%M")
    if os.path.exists(args.out_path):
        append_jsonl(data=data.data, path=args.out_path)
    else:
        export_jsonl(data=data.data, path=args.out_path)
