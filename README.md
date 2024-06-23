# usStock target price estimator

## build input file
- format.yaml
- eps_growth_0: growth percentage in this year
- you don't need to fill all growth persentages for three years.
- peg_peers: non-GAAP peg ratio(FWD) for specific peers
    - refer to Seeking Alpha "peers" tab or finviz
- you don't need to fill current price, because *it can be scrapped from yahoo finance* automatically

## run
```bash
python3 main.py -I format.yaml
```

## streamlit
```bash
streamlit run streamlit_app.py
```

## using sales version
- use it for minus marginal corporations

```bash
python3 main_sales.py -I format_sales.yaml
```