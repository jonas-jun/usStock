import requests
from typing import List, Dict
from utils import load_jsonl, export_jsonl, jsonl_to_excel, get_today
import argparse


def jsonl_to_dict(jsonl, key="year"):
    rst = dict()
    for line in jsonl:
        data = line["attributes"]
        assert key in data
        rst[data[key]] = line
    return rst


class estimate_scrapper(object):
    def __init__(self):
        self.url = "https://seeking-alpha.p.rapidapi.com/symbols/get-estimates"
        self.headers = {
            "x-rapidapi-key": "a695c3975dmshaa0c241f4546f74p18540djsn7d1e3f8558cb",
            "x-rapidapi-host": "seeking-alpha.p.rapidapi.com",
        }

    def get_eps_annual(self, ticker: str, years: List[int] = [2024, 2025]):
        self.ticker = ticker.upper()
        query = {"symbol": self.ticker, "data_type": "eps", "period_type": "annual"}
        response = requests.get(url=self.url, headers=self.headers, params=query)
        res_data = response.json()["data"]
        estimates = self._extract_eps(res_data, years)
        return estimates

    def _extract_eps(self, data, years) -> Dict:
        dict_data = jsonl_to_dict(data)
        rst = {"ticker": self.ticker, "date": get_today()}
        for year in years:
            if year in dict_data:
                consensus = dict_data[year]["attributes"]["consensus"]
                rst[str(year)] = round(consensus, 3)
        return rst


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="estimates scrapper")
    parser.add_argument("--ticker", "-T", type=str, default="four")
    parser.add_argument(
        "--years", "-Y", type=int, nargs="+", default=[2024, 2025, 2026]
    )
    parser.add_argument("--jsonl", "-J", type=str, default="eps_estimates.jsonl")
    parser.add_argument("--xlsx", "-X", type=str, default="test.xlsx")
    args = parser.parse_args()

    eps_scrapper = estimate_scrapper()
    rst = eps_scrapper.get_eps_annual(ticker=args.ticker, years=args.years)
    print(rst)

    data = load_jsonl(args.jsonl)

    if rst in data:
        raise ValueError("already done")
    else:
        data.append(rst)
        export_jsonl(data, args.jsonl)
        jsonl_to_excel(data, args.xlsx)
