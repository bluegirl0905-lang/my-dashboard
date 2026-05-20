import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="오늘의 경제지표", layout="centered")
st.title("📊 오늘의 경제지표")

URL = "https://script.google.com/macros/s/AKfycbzrUvcNuPARln8UlCDjUomg9NrLQKRD4kuVH3pAxx7wCYr94uOusy0eO_R3QUK9Lujl/exec"

@st.cache_data(ttl=60)
def get_data():
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # [수정] 각 열을 하나씩 안전하게 숫자 처리
        for col in df.columns[1:]:
            # 데이터를 먼저 문자열로 바꾸고, 콤마 제거 후 숫자로 강제 변환
            # errors='coerce'를 써서 글자(휴장 등)는 NaN으로 변함
            df[col] = pd.to_numeric(pd.Series(df[col]).astype(str).str.replace(',', ''), errors='coerce')
        
        # NaN(휴장 등)이 된 부분만 0으로 채움
        df = df.fillna(0)
        return df
    except Exception as e:
        st.error(f"데이터 처리 에러: {e}")
        return pd.DataFrame()

df = get_data()

if not df.empty:
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    clean_date = str(latest.iloc[0]).split('T')[0]
    st.write(f"### 🗓️ 기준일: {clean_date}")
    
    groups = {
        "한국 지수": [1, 2], "환율": [3, 4], "미국지수": [5, 6, 7],
        "금리": [8, 9], "원자재": [10, 11, 12], "기타": [13, 14]
    }
    
    for group_name, indices in groups.items():
        st.subheader(group_name)
        cols = st.columns(3)
        for i, idx in enumerate(indices):
            # 인덱스 범위 초과 방지
            if idx < len(latest):
                curr_val = latest.iloc[idx]
                prev_val = prev.iloc[idx]
                # 등락률 계산
                delta_per = ((curr_val - prev_val) / prev_val * 100) if prev_val != 0 else 0
                cols[i % 3].metric(label=latest.index[idx], value=f"{curr_val:,.2f}", delta=f"{delta_per:,.2f}%")
else:
    st.warning("데이터를 불러오지 못했습니다. 시트 데이터가 15열까지 정상적으로 존재하는지 확인해주세요.")
