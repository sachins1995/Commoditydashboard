
import streamlit as st


st.set_page_config(

    layout="wide",
)

st.header("ASTRA Price Prognosis Dashboard")

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
col7, col8, col9 = st.columns(3)

col_crop_pair = {col1:'wheat',
                 col2:'finepaddy',
                 col3:'shrimp',
                 col4:'soya',
                 col5:'basmati',
                 col6:'chana',
                 col7:'coffee',
                 col8:'maize',
                 col9:'chili'}

for key, val in col_crop_pair.items():
    
    with key.container(border=1):
        st.subheader(val.upper())
        st.image(f'images/{val}.png')

