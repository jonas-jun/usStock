from sconf import Config
import json


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
