import streamlit as st
import pandas as pd

image_logo = "assets/LOGO.png"
st.set_page_config(page_title="home", page_icon=image_logo, layout="wide")
st.sidebar.markdown("---")
st.sidebar.image(image_logo, width=175)

if 'data' not in st.session_state:
    dataFrame = pd.read_csv("datasets/Dados.csv", index_col=0)
    st.session_state['data'] = dataFrame

st.write(dataFrame)