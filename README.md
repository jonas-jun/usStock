# usStock target price estimator

## build input file

### EPS version
- for in the blacks (plus eps)
- inputs/format_eps.yaml
- eps_growth_0: earnings > earnings estimates
- pe_fwd: earnings > earnings estimates
- peg_peers: peers
- you don't need to fill all growth persentages for three years.
- peg_peers: non-GAAP peg ratio(FWD) for specific peers
    - refer to Seeking Alpha "peers" tab or finviz
- you don't need to fill current price, because *it can be scrapped from yahoo finance* automatically

### Sales version
- for in the reds (minus eps)
- inputs/format_sales.yaml
- sales_growth: earnings > earnings estimates
- ps_fwd: earnings > earnings estimates
- op_margin: fincancials > as a % of revenue, quarterly or profitability > EBIT margin
- op_margin_sector: profitability > EBIT margin median
- ps_sector: valuation > prcies/sales(fwd)
- sales_growth_sector: growth > revenue growth median
- sector_psg_ratio = PSR / (sales_growth * 100)

## run
```bash
python3 main.py -I inputs/format_eps.yaml # not save result case
python3 main.py -I inputs/format_eps.yaml -O result_eps.jsonl # save result case
python3 main.py -I inputs/format_sales.yaml -O result_sales.jsonl
```

## streamlit
- only EPS version
```bash
streamlit run streamlit_app.py
```

# Chart getter
```bash
python3 charter.py -T tsla -P ytd -E chart_tsla.jpg
```
- period: ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

![chart_tsla](/src/chart_tsla.jpg)