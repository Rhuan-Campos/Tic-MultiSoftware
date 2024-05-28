import streamlit as st

image_logo = "assets/MultiCTe.png"
st.set_page_config(page_title="MultiCTe", page_icon=image_logo, layout="wide")

c1, c2, c3 = st.columns([1,1,1])
with c1:
    st.markdown(" ")
with c2:
    st.image(image_logo)
with c3:
    st.markdown(" ")
col1, col2 = st.columns([1, 1])
with col1:
    data = st.date_input("Selecione o período de visualização")
with col2:
    time = st.time_input("Selecione o horário de visualização")