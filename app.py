import streamlit as st
import pandas as pd
import requests

# (상단 설정은 동일)
# ...

@st.cache_data(ttl=300)
def get_data():
    try:
        response = requests.get(URL, timeout=15)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        
        # [핵심 수정] 숫자가 아닌 글자(휴장 등)는 강제로 0으로 변환하는 로직 강화
        for col in df.columns[1:]:
            # 1. 콤마 제거 2. 숫자로 강제 변환 3. 에러(휴장 등)는 NaN으로 4. NaN을 0으로 채움
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return df
    except:
        return pd.DataFrame()

# (하단 출력 부분 동일)
# ...
