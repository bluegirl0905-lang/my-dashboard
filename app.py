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
            # 첫 번째 열(날짜) 제외하고 모두 숫자로 변환, 에러는 0으로 처리
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # 날짜 처리
    clean_date = str(latest.iloc[0]).split('T')[0]
    st.write(f"### 🗓️ 기준일: {clean_date}")
    
    groups = {
        "한국 지수": [1, 2],
        "환율": [3, 4],
        "미국지수": [5, 6, 7],
        "금리": [8, 9],
        "원자재": [10, 11, 12],
        "기타": [13, 14]
    }

    for group_name, indices in groups.items():
        st.subheader(group_name)
        cols = st.columns(3)
        for i, idx in enumerate(indices):
            if idx < len(latest):
                label = latest.index[idx]
                curr_val = latest.iloc[idx]
                prev_val = prev.iloc[idx]
                
                # 등락률 계산 (0으로 나누기 방지)
                delta_per = ((curr_val - prev_val) / prev_val * 100) if prev_val != 0 else 0
                
                cols[i % 3].metric(label=label, value=f"{curr_val:,.2f}", delta=f"{delta_per:,.2f}%")
        st.divider()
else:
    st.warning("데이터를 불러오는 중입니다. 구글 시트 배포 설정을 확인해 주세요!")
