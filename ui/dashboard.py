import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

API_URL = "http://fastapi_server:8000/latest"

st.set_page_config(page_title="Market Intelligence", layout="wide")
st.title("🚀 Real-Time Market Intelligence Dashboard")

if "data_history" not in st.session_state:
    st.session_state.data_history = []

placeholder = st.empty()

def fetch_data():
    try:
        response = requests.get(API_URL, timeout=2)
        if response.status_code == 200:
            return response.json()
    except:
        return None

while True:
    data = fetch_data()

    if data:
        st.session_state.data_history.append(data)

    with placeholder.container():

        st.subheader("📊 Live Predictions")

        if len(st.session_state.data_history) > 0:
            df = pd.DataFrame(st.session_state.data_history)

            col1, col2, col3 = st.columns(3)

            col1.metric("Price", df.iloc[-1]["price"])
            col2.metric("Recommendation", df.iloc[-1]["recommendation"])
            col3.metric("Confidence", round(df.iloc[-1]["confidence"], 2))

            st.markdown("---")

            fig = px.line(df, x="timestamp", y="price")
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Waiting for first message...")

    time.sleep(2)