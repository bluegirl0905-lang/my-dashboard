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
        # 구글 시트에서 데이터를 그대로 리스트 형태의 데이터프레임으로 받습니다.
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    except Exception as e:
        return None

df = get_data()

if df is not None:
    # [디버깅] 일단 데이터가 어떻게 생겼는지 화면에 보여줍니다.
    st.write("데이터 로드 성공!")
    st.dataframe(df.tail(1)) # 최근 데이터 1줄만 출력
    
    # 여기서부터는 나중에 숫자가 확인되면 다시 그룹화 코드를 넣으면 됩니다.
    st.info("데이터가 위처럼 보인다면, 각 항목이 몇 번째 열(0부터 시작)에 있는지 확인해서 인덱스를 맞춰야 합니다.")
else:
    st.error("데이터를 가져오는 데 실패했습니다. 구글 시트 URL을 다시 확인해주세요.")
