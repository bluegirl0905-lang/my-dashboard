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
        # 숫자 데이터가 아닌 항목은 제외하고 숫자만 남김
        df_numeric = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
        df_final = pd.concat([df.iloc[:, 0], df_numeric], axis=1)
        return df_final
    except:
        return pd.DataFrame()

df = get_data()

if not df.empty:
    st.subheader("📊 최근 주요 자산 흐름")
    st.line_chart(df.set_index(df.columns[0]))
    
    st.subheader("📋 최신 데이터 상세")
    st.dataframe(df.tail(10))
else:
    st.warning("데이터를 가져오는 중입니다. 잠시만 기다리거나 구글 시트 형식을 확인해 주세요.")
