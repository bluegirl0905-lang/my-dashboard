import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="경제지표 요약", layout="centered")
st.title("📊 오늘의 경제지표")

URL = "https://script.google.com/macros/s/AKfycbzrUvcNuPARln8UlCDjUomg9NrLQKRD4kuVH3pAxx7wCYr94uOusy0eO_R3QUK9Lujl/exec"

@st.cache_data(ttl=60)
def get_data():
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()
        
        # 1. 데이터가 리스트 형태인지 확인
        if not data or len(data) < 2:
            return None
        
        # 2. 열 이름을 강제로 0, 1, 2... 순서로 지정 (중복 이름 에러 방지)
        df = pd.DataFrame(data[1:])
        df.columns = [f"col_{i}" for i in range(df.shape[1])]
        return df
    except Exception as e:
        return None

df = get_data()

if df is not None:
    st.write("✅ 데이터 연결 성공! 아래 표를 보고 어떤 열이 어떤 데이터인지 번호를 확인하세요.")
    st.dataframe(df.tail(3)) 
    
    st.write("### 열 번호 확인 가이드")
    st.write("위 표에서 보고, 원하는 데이터가 몇 번째 'col_X'에 있는지 알려주세요!")
    st.write("예: col_0은 날짜, col_1은 코스피, col_2는 코스닥...")
else:
    st.error("데이터를 가져오는 데 실패했습니다.")
