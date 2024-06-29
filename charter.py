import argparse
import yfinance as yf
import matplotlib.pyplot as plt


class makeChart(object):
    def __init__(self, ticker, period, export=False, message=None):
        self.ticker = ticker
        self.data = yf.Ticker(ticker)
        self.period = period
        self.export = export
        self.message = message
        self._get_history()

    def get_chart(self):
        plt.figure(figsize=(12, 8))
        plt.title(f"Stock Chart: {self.ticker}")
        plt.xlabel("date")
        plt.ylabel("price")
        plt.grid(True)
        plt.plot(self.history["Close"], color="black")
        self._get_values()
        cfg_bbox = {"boxstyle": "round,pad=0.3", "fc": "lightsteelblue", "alpha": 0.5}
        cfg_arrowprops = {
            "arrowstyle": "->",
            "color": "salmon",
        }  # ['->', '-|>', '<->', 'fancy', 'simple']
        plt.annotate(
            f'LAST: ${self.values["last"][1]:.2f}',
            xy=(self.values["last"]),
            # xytext=(self.values["last"][0] + timedelta(days=5), self.values["last"][1]),
            xytext=(10, 0),
            textcoords="offset points",
            bbox=cfg_bbox,
            color="darkviolet",
            fontweight="bold",
        )
        plt.annotate(
            f'MIN\nvalue: ${self.values["min"][1]:.2f}\ndate: {self.values["min"][0].date().isoformat()}',
            xy=self.values["min"],
            xytext=(-100, 20),
            textcoords="offset points",
            arrowprops=cfg_arrowprops,
            bbox=cfg_bbox,
        )
        plt.annotate(
            f'MAX\nvalue: ${self.values["max"][1]:.2f}\ndate: {self.values["max"][0].date().isoformat()}',
            xy=self.values["max"],
            xytext=(-100, -20),
            textcoords="offset points",
            arrowprops=cfg_arrowprops,
            bbox=cfg_bbox,
        )
        if self.message:
            plt.figtext(
                0.8,
                0.05,
                self.message,
                ha="center",
                fontsize=12,
                fontweight="bold",
                color="darkred",
            )
        if self.export:
            self._export_image(path=self.export)
        plt.show()

    def _get_history(self):
        self.history = self.data.history(period=self.period)

    def _get_values(self):
        df = self.history
        col = "Close"
        rst = dict()
        rst["max"] = (df[col].idxmax(), df[col].max())  # (date, value)
        rst["min"] = (df[col].idxmin(), df[col].min())
        rst["last"] = (df.index[-1], df[col].iloc[-1])
        self.values = rst

    def _export_image(self, path):
        plt.savefig(path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="stock chart getter")
    parser.add_argument("--ticker", "-T", type=str, default="LLY")
    parser.add_argument(
        "--period",
        "-P",
        type=str,
        default="ytd",
        help="['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']",
    )
    parser.add_argument(
        "--export",
        "-E",
        type=str,
        default=False,
        help="export as *.jpg. False if don't want",
    )
    args = parser.parse_args()
    args.ticker = args.ticker.upper()

    data = makeChart(ticker=args.ticker, period=args.period, export=args.export)
    data.get_chart()
