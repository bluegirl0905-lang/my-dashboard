import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="오늘의 경제지표 요약", layout="centered")
st.title("📊 오늘의 경제지표 요약")

URL = "https://script.google.com/macros/s/AKfycbzrUvcNuPARln8UlCDjUomg9NrLQKRD4kuVH3pAxx7wCYr94uOusy0eO_R3QUK9Lujl/exec"

@st.cache_data(ttl=600)
def get_data():
    try:
        response = requests.get(URL)
        data = response.json()
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    latest = df.iloc[-1]
    st.write(f"### 🗓️ 기준일: {latest.iloc[0]}")
    
    # 그룹별로 나누어 출력 (지표가 10개면 3~4개씩 묶어서)
    groups = {
        "국내 증시/환율": [1, 2, 3], # KOSPI, KOSDAQ, 환율
        "미국 및 금리": [4, 5, 6],   # 미국지수, 금리1, 금리2
        "원자재 및 기타": [7, 8, 9, 10] # 금, 원유, 구리, 비트코인, VIX
    }

    for group_name, indices in groups.items():
        st.subheader(group_name)
        cols = st.columns(3)
        for i, idx in enumerate(indices):
            if idx < len(latest):
                label = latest.index[idx]
                value = latest.iloc[idx]
                cols[i % 3].metric(label=label, value=f"{value}")
        st.divider()

else:
    st.warning("데이터를 불러오고 있습니다.")
