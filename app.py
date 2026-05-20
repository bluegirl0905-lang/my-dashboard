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
    
    # 요청하신 그룹별 분류 (인덱스는 구글 시트의 열 순서와 일치해야 합니다)
    # 만약 데이터가 안 나오면, 시트의 열 순서에 맞춰 [1, 2] 등의 숫자를 조정하세요.
    groups = {
        "한국 지수": [1, 2],           # 코스피, 코스닥
        "환율": [3, 4],               # 환율, 달러인덱스
        "미국지수": [5, 6, 7],        # S&P500, 나스닥, 다우
        "금리": [8, 9],               # 2Y, 10Y
        "원자재": [10, 11, 12],       # 구리, 금, WTI
        "기타": [13, 14]              # BTC, VIX
    }

    for group_name, indices in groups.items():
        st.subheader(group_name)
        cols = st.columns(3) # 3개씩 배치
        for i, idx in enumerate(indices):
            if idx < len(latest):
                label = latest.index[idx]
                value = latest.iloc[idx]
                cols[i % 3].metric(label=label, value=f"{value}")
        st.divider()

else:
    st.warning("데이터를 불러오고 있습니다. 시트의 데이터 열 순서를 확인해 주세요!")
