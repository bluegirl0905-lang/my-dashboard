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
        # 데이터가 2차원 리스트 형태라고 가정하고 DataFrame 생성
        if len(data) > 1:
            return pd.DataFrame(data[1:], columns=data[0])
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    # 가장 마지막 줄(최신 데이터) 가져오기
    latest = df.iloc[-1]
    
    # 데이터가 제대로 들어왔는지 확인하고 출력
    st.write(f"### 🗓️ 기준일: {latest.iloc[0]}")
    st.metric(label="핵심 경제 지표", value=f"{latest.iloc[1]}")
    
    with st.expander("지난 데이터 흐름 확인하기"):
        st.dataframe(df.tail(7))
else:
    st.warning("데이터를 불러오고 있습니다. 잠시만 기다려 주세요.")
    st.info("구글 시트의 데이터가 비어있거나 API 연결이 확인 중일 수 있습니다.")
