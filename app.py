import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="오늘의 경제지표 요약", layout="centered")
st.title("📊 오늘의 경제지표 요약")

URL = "https://script.google.com/macros/s/AKfycbzrUvcNuPARln8UlCDjUomg9NrLQKRD4kuVH3pAxx7wCYr94uOusy0eO_R3QUK9Lujl/exec"

@st.cache_data(ttl=60)
def get_data():
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()
        df = pd.DataFrame(data[1:])
        df.columns = [f"col_{i}" for i in range(df.shape[1])]
        
        # 각 col을 숫자로 변환 (에러 발생 시 0으로)
        for col in df.columns[1:]:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # col_0이 날짜입니다.
    st.write(f"### 🗓️ 데이터 기준: {str(latest['col_0']).split('T')[0]} (미국 마감일 기준)")
    
    # col_1부터 확인된 순서대로 매칭 (표 보고 설정한 위치)
    # col_1: 코스피, col_2: 코스닥, col_3: 환율, col_4: 달러인덱스
    # col_5: S&P500, col_6: 나스닥, col_7: 다우, col_8: 2Y금리, col_9: 10Y금리
    # col_10: 구리, col_11: 금, col_12: WTI, col_13: BTC, col_14: VIX
    
    groups = {
        "한국 지수": ["col_1", "col_2"],
        "환율": ["col_3", "col_4"],
        "미국지수": ["col_5", "col_6", "col_7"],
        "금리": ["col_8", "col_9"],
        "원자재": ["col_10", "col_11", "col_12"],
        "기타": ["col_13", "col_14"]
    }
    
    # 보여줄 이름 매칭
    names = {
        "col_1": "코스피", "col_2": "코스닥", "col_3": "환율", "col_4": "달러인덱스",
        "col_5": "S&P500", "col_6": "나스닥", "col_7": "다우", "col_8": "2Y금리", "col_9": "10Y금리",
        "col_10": "구리", "col_11": "금", "col_12": "WTI", "col_13": "BTC", "col_14": "VIX"
    }

    for group_name, cols in groups.items():
        st.subheader(group_name)
        c = st.columns(3)
        for i, col_name in enumerate(cols):
            curr_val = latest[col_name]
            prev_val = prev[col_name]
            delta = ((curr_val - prev_val) / prev_val * 100) if prev_val != 0 else 0
            c[i % 3].metric(label=names[col_name], value=f"{curr_val:,.2f}", delta=f"{delta:,.2f}%")
        st.divider()
else:
    st.warning("데이터를 불러오는 중입니다.")
