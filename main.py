import os
import copy
from datetime import datetime
from sconf import Config
import argparse
import yfinance as yf
from utils import pprint_config, append_jsonl, export_jsonl
from estimator import getTargetPrice, getTargetPriceRevenue
from charter import makeChart

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="usStock target price estimator")
    parser.add_argument(
        "--input_path", "-I", type=str, default="inputs/format_eps.yaml"
    )
    parser.add_argument("--out_path", "-O", type=str, default=None)
    parser.add_argument("--out_img", "-IMG", type=str, default=None)
    args = parser.parse_args()

    # load format file
    cfg = Config(args.input_path)
    print(">> initialized data")
    pprint_config(cfg)
    data = copy.deepcopy(cfg)

    # yfinance 데이터 한 번만 로드
    yf_ticker = yf.Ticker(cfg.ticker)

    # build estimator
    task = data.task.lower()
    assert task in {"eps", "sales"}
    if task == "eps":
        data = getTargetPrice(data=data, yf_ticker=yf_ticker)
    else:
        data = getTargetPriceRevenue(data=data, yf_ticker=yf_ticker)

    # estimating
    print("\n\n>> Calculating...")
    data.calc_all()
    pprint_config(data.data)

    # exporting
    now = datetime.now()
    data.data["date"] = now.strftime("%y%m%d-%a-%H:%M")
    if args.out_path:
        if os.path.exists(args.out_path):
            append_jsonl(data=data.data, path=args.out_path)
        else:
            export_jsonl(data=data.data, path=args.out_path)

    # make chart
    chart = makeChart(
        ticker=cfg.ticker,
        period="1y",
        export=args.out_img,
        message="target price 1yr: ${:.2f}".format(data.data.price_target),
        yf_ticker=yf_ticker,
    )
    chart.get_chart()
