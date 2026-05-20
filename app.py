import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="나의 갓생 경제 대시보드", layout="wide")
st.title("📈 나의 실시간 경제 자산 대시보드")

URL = "https://script.google.com/macros/s/AKfycbzrUvcNuPARln8UlCDjUomg9NrLQKRD4kuVH3pAxx7wCYr94uOusy0eO_R3QUK9Lujl/exec"

@st.cache_data(ttl=600)
def get_data():
    try:
        response = requests.get(URL)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # 첫 번째 열을 제외한 나머지 열들을 강제로 숫자로 변환
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    st.subheader("📊 최근 주요 자산 흐름")
    # 인덱스를 날짜 열로 설정하여 차트 표시
    st.line_chart(df.set_index(df.columns[0]))
    
    st.subheader("📋 최신 데이터 상세")
    st.dataframe(df.tail(10))
else:
    st.warning("데이터를 가져오는 중입니다. 잠시만 기다려 주세요.")
