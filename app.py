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
            df = pd.DataFrame(data[1:], columns=data[0])
            # 숫자가 아닌 열은 모두 제외하고 숫자 데이터만 남기기
            numeric_df = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
            return pd.concat([df.iloc[:, 0], numeric_df], axis=1)
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    latest = df.iloc[-1]
    
    st.write(f"### 🗓️ 기준일: {latest.iloc[0]}")
    
    # 지표가 많으니 가장 최근 데이터에서 숫자 열들만 뽑아서 컬럼별로 보여주기
    cols = st.columns(3) # 3개씩 배치
    data_points = latest.iloc[1:4] # 앞쪽 3개 지표만 뽑음
    
    for i, (label, value) in enumerate(data_points.items()):
        cols[i % 3].metric(label=label, value=f"{value:,.2f}")
    
    with st.expander("지표 상세 보기 (최근 5일)"):
        st.dataframe(df.tail(5))
else:
    st.warning("데이터를 불러오고 있습니다.")
