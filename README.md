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
python3 main.py
```
