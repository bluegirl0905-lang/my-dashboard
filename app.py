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
        # 1. 여기서 응답이 잘 오는지 확인
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        # 2. 숫자로 변환
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"에러 발생: {e}")
        return None

df = get_data()

if df is not None and not df.empty:
    st.write("✅ 데이터 연결 성공!")
    latest = df.iloc[-1]
    # (이하 출력 로직 동일)
    st.write(f"### 🗓️ 기준일: {str(latest.iloc[0]).split('T')[0]}")
    
    groups = {
        "한국 지수": [1, 2], "환율": [3, 4], "미국지수": [5, 6, 7],
        "금리": [8, 9], "원자재": [10, 11, 12], "기타": [13, 14]
    }
    for group_name, indices in groups.items():
        st.subheader(group_name)
        cols = st.columns(3)
        for i, idx in enumerate(indices):
            if idx < len(latest):
                cols[i % 3].metric(label=latest.index[idx], value=f"{latest.iloc[idx]:,.2f}")
else:
    st.warning("데이터를 불러오지 못했습니다. 구글 시트 연결이나 데이터 구조를 확인해주세요.")
