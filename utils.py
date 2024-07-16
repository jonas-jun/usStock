from sconf import Config
import json
from tqdm import tqdm
import pandas as pd
from datetime import datetime

def build_request_url(base: str, data: dict) -> str:
    for key in data:
        if data[key]:
            base += f"{key}={data[key]}&"
    return base[:-1]


def pprint_config(cfg: Config):
    for key, value in cfg.items():
        print(f"> {key}: {value}")


def append_jsonl(data: Config, path):
    data = _sconf_to_dict(data)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data))
        f.write("\n")


def export_jsonl(data: Config, path):
    data = _sconf_to_dict(data)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(data))
        f.write("\n")


def _sconf_to_dict(data: Config) -> dict:
    rst = dict()
    for key, value in data.items():
        rst[key] = value
    return rst


def load_jsonl(in_f):
    rst = list()
    with open(in_f, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc=f"loading: {in_f}"):
            rst.append(json.loads(line))
    return rst


def export_jsonl(data, out_f):
    with open(out_f, "w", encoding="utf-8") as f:
        for line in tqdm(data, desc=f"exporting: {out_f}"):
            f.write(json.dumps(line, ensure_ascii=False))
            f.write("\n")


def jsonl_to_excel(data, out_f):
    df = pd.DataFrame(data)
    print(f"shape of DataFrame: {df.shape}")
    df.to_excel(out_f, index=False)

weekday_map = {0: "Mon",
            1: "Tue",
            2: "Wed",
            3: "Thu",
            4: "Fri",
            5: "Sat",
            6: "Sun"}

def get_today():
    today = datetime.today()
    rst = f"{today.strftime("%Y-%m-%d")}-{weekday_map[today.weekday()]}"
    return rst
