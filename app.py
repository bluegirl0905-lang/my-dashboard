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
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    # 가장 최신 데이터 가져오기
    latest = df.iloc[-1]
    
    st.write(f"### 🗓️ 기준일: {latest[0]}")
    
    # 주요 지표를 눈에 띄게 배치
    st.metric(label="핵심 경제 지표", value=f"{latest[1]}")
    
    with st.expander("지난 데이터 흐름 확인하기"):
        st.dataframe(df.tail(7)) # 최근 일주일 데이터
else:
    st.warning("데이터를 불러오고 있습니다. 잠시만 기다려 주세요.")
