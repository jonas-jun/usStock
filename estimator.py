import yfinance as yf
import numpy as np


class getTargetPrice(object):
    def __init__(self, data):
        self.data = data
        self.yf_data = yf.Ticker(self.data.ticker)
        if not data.price_current:
            self._get_current_price()
        self._get_52high()

    def calc_all(self):
        self._calc_peg_peers()
        self._calc_eps_avg()
        self._calc_peg_ratio()
        self._calc_growth_value()
        self._calc_dec_from_52high()
        self._calc_reasonable_price()
        self._calc_target_prices()

    def _get_current_price(self):
        self.data.price_current = self.yf_data.info["regularMarketPreviousClose"]

    def _get_52high(self):
        self.data.price_52high = self.yf_data.info["fiftyTwoWeekHigh"]

    def _calc_peg_peers(self):
        if type(self.data.peg_peers) not in {float, int}:
            self.data.peg_peers = np.mean(self.data.peg_peers).item()

    def _calc_eps_avg(self):
        val_eps_growth = list()
        for key, value in self.data.items():
            if "eps" in key and "avg" not in key and value:
                val_eps_growth.append(value)
        self.data.eps_growth_avg = np.mean(val_eps_growth)

    def _calc_peg_ratio(self):
        self.data.peg_ratio = self.data.pe_fwd / self.data.eps_growth_avg

    def _calc_growth_value(self):
        if self.data.eps_growth_avg > 0:
            self.data.growth_value = self.data.eps_growth_avg * self.data.peg_peers
        else:
            self.data.growth_value = (
                self.data.pe_fwd + (self.data.pe_fwd * self.data.eps_growth_avg)
            ) / 100

    def _calc_dec_from_52high(self):
        self.data.dec_from_52high = (
            self.data.price_current / self.data.price_52high
        ) - 1

    def _calc_reasonable_price(self):
        self.data.price_reasonable = self.data.price_current * (
            self.data.growth_value / self.data.pe_fwd
        )

    def _calc_target_prices(self):
        if self.data.eps_growth_1:
            self.data.price_target = self.data.price_reasonable * (
                1 + self.data.eps_growth_1 / 100
            )
        if self.data.eps_growth_1 and self.data.eps_growth_2:
            self.data.price_target_2 = self.data.price_reasonable * (
                1 + self.data.eps_growth_1 / 100 + self.data.eps_growth_2 / 100
            )
        if self.data.eps_growth_1 and self.data.eps_growth_2 and self.data.eps_growth_3:
            self.data.price_target_3 = self.data.price_reasonable * (
                1
                + self.data.eps_growth_1 / 100
                + self.data.eps_growth_2 / 100
                + self.data.eps_growth_3 / 100
            )


class getTargetPriceRevenue(getTargetPrice):
    def calc_all(self):
        self._calc_sales_avg()
        self._calc_psg_ratio()
        self._calc_psg_ratio_sector()
        self._calc_growth_value()
        self._calc_discount_rate()
        self._calc_growth_margin_value()
        self._calc_dec_from_52high()
        self._calc_target_price_growth()
        self._calc_target_price()

    def _calc_sales_avg(self):
        val_sales_growth = list()
        for key, value in self.data.items():
            if "sales" in key and "avg" not in key and "sector" not in key and value:
                val_sales_growth.append(value)
        self.data.sales_growth_avg = np.mean(val_sales_growth)

    def _calc_psg_ratio(self):
        self.data.psg_ratio = self.data.ps_fwd / (self.data.sales_growth_avg)

    def _calc_psg_ratio_sector(self):
        self.data.psg_ratio_sector = self.data.ps_sector / self.data.sales_growth_sector

    def _calc_growth_value(self):
        if self.data.sales_growth_avg < 0:
            self.data.growth_value = self.data.ps_fwd + (
                self.data.ps_fwd * self.data.sales_growth_avg
            )
        else:
            self.data.growth_value = (
                100 * self.data.sales_growth_avg
            ) * self.data.psg_ratio_sector
        self.data.growth_value /= 100

    def _calc_discount_rate(self):
        if self.data.op_margin < self.data.op_margin_sector:
            if self.data.op_margin < 0:
                self.data.discount_rate = (
                    self.data.op_margin + self.data.op_margin_sector
                ) / 2
            else:
                self.data.discount_rate = (
                    self.data.op_margin - self.data.op_margin_sector
                ) / 2
        else:
            self.data.discount_rate = (
                self.data.op_margin - self.data.op_margin_sector
            ) / 2
        self.data.discount_rate /= 100

    def _calc_growth_margin_value(self):
        self.data.growth_margin_value = self.data.growth_value + (
            self.data.growth_value * self.data.discount_rate
        )

    def _calc_target_price_growth(self):
        self.data.price_target_growth = (
            self.data.price_current * self.data.growth_value / self.data.ps_fwd
        )

    def _calc_target_price(self):
        self.data.price_target = (
            self.data.price_current * self.data.growth_margin_value / self.data.ps_fwd
        )
