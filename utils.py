from sconf import Config


def build_request_url(base: str, data: dict) -> str:
    for key in data:
        if data[key]:
            base += f"{key}={data[key]}&"
    return base[:-1]


def pprint_config(cfg: Config):
    for key, value in cfg.items():
        print(f"> {key}: {value}")


def pprint_config_text(cfg: Config):
    rst = str()
    for key, value in cfg.items():
        tmp = f"{key}: {value}\n"
        rst += tmp
    return rst
