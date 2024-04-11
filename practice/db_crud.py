import streamlit as st
from st_pages import show_pages_from_config
from sqlalchemy.sql import text
from datetime import datetime
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(
    page_title="DB CRUD",
    page_icon="./images/monsterball.png"
)
show_pages_from_config()
st.markdown("""
<style>
img { 
    max-height: 300px;
}
.streamlit-expanderContent div {
    display: flex;
    justify-content: center;
    font-size: 20px;
}
[data-testid="stExpanderToggleIcon"] {
    visibility: hidden;
}
.streamlit-expanderHeader {
    pointer-events: none;
}
[data-testid="StyledFullScreenButton"] {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# conn sqlite
conn = st.connection('mysqlite_db', type='sql')
with conn.session as s:
    s.execute(text('CREATE TABLE IF NOT EXISTS long_term_inaction_notice (notice TEXT, updated_at TEXT);'))
    s.execute(text('CREATE TABLE IF NOT EXISTS long_term_inaction_total (category TEXT, east_gwangju TEXT, west_gwangju TEXT, mokpo TEXT, suncheon TEXT, jeju TEXT, total TEXT, updated_at TEXT);'))
    s.commit()

st.title("DB CRUD")
st.markdown("H/W **performance**")


df = conn.query('select * from long_term_inaction_notice')
st.data_editor(df)

with st.form(key="form"):
    notice = st.text_input(
        label="장기 미조치 현황 추가"
    )
    submit = st.form_submit_button(label="Submit")
    if submit:
        if not notice or len(notice.strip()) == 0:
            st.error("장기 미조치 현황 안내를 작성해주세요.")
        else:
            with conn.session as s:                
                s.execute(text('INSERT INTO long_term_inaction_notice (notice, updated_at) VALUES (:notice, :updated_at);'), params=dict(notice=notice, updated_at=datetime.now()))
                s.commit()
            st.success("장기 미조치 현황 안내를 추가하였습니다.")
            # https://discuss.streamlit.io/t/database-updates/49371/6
            st.cache_data.clear()
            streamlit_js_eval(js_expressions="parent.window.location.reload()")