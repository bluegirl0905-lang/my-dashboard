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
            # 숫자로 변환 가능한 열들은 모두 숫자로 변환 (등락률 계산을 위해)
            for col in df.columns[1:]:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            return df
        return pd.DataFrame()
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    # 1. 날짜만 깔끔하게 표시 (시간 제거)
    latest = df.iloc[-1]
    raw_date = str(latest.iloc[0])
    clean_date = raw_date.split('T')[0] # '2026-05-19T...'에서 앞부분만 추출
    
    st.write(f"### 🗓️ 기준일: {clean_date}")
    
    # 2. 등락률 계산을 위해 이전 날 데이터 가져오기
    # 데이터가 2개 이상일 때만 비교, 아니면 0으로 표시
    has_previous = len(df) > 1
    previous = df.iloc[-2] if has_previous else latest

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
        cols = st.columns(3)
        for i, idx in enumerate(indices):
            if idx < len(latest):
                label = latest.index[idx]
                curr_val = latest.iloc[idx]
                prev_val = previous.iloc[idx]
                
                # 등락률 계산: ((오늘 - 어제) / 어제) * 100
                if has_previous and prev_val != 0 and not pd.isna(curr_val) and not pd.isna(prev_val):
                    delta_per = ((curr_val - prev_val) / prev_val) * 100
                    delta_str = f"{delta_per:,.2f}%"
                else:
                    delta_str = "0.00%"

                # 지수 값 표시 (소수점 2자리까지)
                val_str = f"{curr_val:,.2f}" if isinstance(curr_val, (int, float)) else str(curr_val)
                
                cols[i % 3].metric(label=label, value=val_str, delta=delta_str)
        st.divider()

else:
    st.warning("데이터를 불러오는 중입니다.")
