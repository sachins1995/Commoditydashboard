import streamlit as st


LATEST_MODEL_RUN = 'Predicted Mid July'

st.set_page_config(

    layout="wide",
)


pages={"Homepage":[st.Page("apex.py", title="Homepage")],
    "VAAP":[st.Page("dashboard_shrimp.py", title="Aqua"), st.Page("dashboard_coffee.py", title="Coffee"), st.Page("dashboard_chili.py", title="Chili")],
        "OGP":[ 
                    st.Page("dashboard_wheat.py", title="Wheat"),
                    st.Page("dashboard_soya.py", title="Soya"),
                    st.Page("dashboard_chana.py", title="Chana"),
                    st.Page("dashboard_basmati.py", title="Basmati"),
                    st.Page("dashboard_finepaddy.py", title="Fine Paddy"),
                    st.Page("dashboard_maize.py", title="Maize")
                    ]}
pg = st.navigation(pages, position="top", expanded=False)
pg.run()

