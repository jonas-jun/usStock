import json
import streamlit as st
from sconf import Config
from estimator import getTargetPrice
import time

st.title("US Stock Target Price Estimator")
msg_welcome = """
---
미국 주식의 적정 주가를 계산해보는 페이지입니다.\n
<미주부: 미국 주식으로 부자되기>를 참고했습니다.\n
다음 항목들을 찾아 입력해주세요.
"""
# st.markdown(msg_welcome)
st.divider()

ticker = st.text_input("Ticker: ", "FOUR")
ticker = ticker.upper()

st.divider()
price_current = st.number_input("현재 주가(USD): 입력하지 않으시면 자동으로 가져옵니다.")

st.divider()
st.write("EPS 성장률 예측치: D+2부터는 비워두어도 괜찮습니다.")

eps_growth_0 = st.number_input("EPS 성장률(%) D+0: ")
eps_growth_1 = st.number_input("EPS 성장률(%) D+1: ")
eps_growth_2 = st.number_input("EPS 성장률(%) D+2: ")
eps_growth_3 = st.number_input("EPS 성장률(%) D+3: ")

st.divider()
pe_fwd = st.number_input("P/E ratio (FWD): ", 0)
pe_fwd = float(pe_fwd)

st.divider()
peg_peers = st.text_input(
    "Peer그룹의 PEG ratio를 쉼표로 구분하여 입력해주세요: ",
    "0.88, 0.97, 1.77, 0.45",
)
peg_peers = list(map(float, peg_peers.split(",")))

data_dic = dict()
data_dic["ticker"] = ticker
data_dic["price_current"] = price_current
data_dic["eps_growth_0"] = eps_growth_0
data_dic["eps_growth_1"] = eps_growth_1
data_dic["eps_growth_2"] = eps_growth_2
data_dic["eps_growth_3"] = eps_growth_3
data_dic["pe_fwd"] = pe_fwd
data_dic["peg_peers"] = peg_peers
print(data_dic)

st.divider()

data_cfg = Config(data_dic)

st.write("입력된 데이터입니다.")
st.json(json.dumps(data_dic), expanded=True)

with st.spinner("계산 중입니다..."):
    data = getTargetPrice(data=data_cfg)
    st.write("계산된 데이터입니다.")
    data.calc_all()
    time.sleep(2)

rst = {
    "Current price": data.data.price_current,
    "Average EPS growth": round(data.data.eps_growth_avg, 2),
    "PEG ratio": round(data.data.peg_ratio, 2),
    "Growth value": round(data.data.growth_value, 2),
    "Reasonable price": round(data.data.price_reasonable, 1),
    "Target price D+1": round(data.data.price_target_1, 1),
}
if data.data.get("price_target_2"):
    rst["Target price D+2"] = round(data.data.price_target_2, 1)
if data.data.get("price_target_3"):
    rst["Target price D+3"] = round(data.data.price_target_3, 1)

st.json(rst)

st.divider()

box = st.success if rst["Target price D+1"] > rst["Current price"] else st.error


box(f"Target price fwd 1yr: {rst["Target price D+1"]} USD", icon=":material/attach_money:")
