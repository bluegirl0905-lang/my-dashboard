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
        return pd.DataFrame(data[1:], columns=data[0])
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    latest = df.iloc[-1]
    st.write(f"### 🗓️ 기준일: {latest.iloc[0]}")
    
    # 이제 시트의 열 순서(1번부터 시작)와 완벽하게 일치합니다.
    groups = {
        "한국 지수": [1, 2],           # B, C열
        "환율": [3, 4],               # D, E열
        "미국지수": [5, 6, 7],        # F, G, H열
        "금리": [8, 9],               # I, J열
        "원자재": [10, 11, 12],       # K, L, M열
        "기타": [13, 14]              # N, O열
    }

    for group_name, indices in groups.items():
        st.subheader(group_name)
        cols = st.columns(3)
        for i, idx in enumerate(indices):
            if idx < len(latest):
                cols[i % 3].metric(label=latest.index[idx], value=f"{latest.iloc[idx]}")
        st.divider()
