import streamlit as st

TITLE = "SHW-M380W 영상 변환기"
SLATE_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/clapper-board_1f3ac.png"

st.set_page_config(page_title=TITLE, page_icon=SLATE_ICON)
st.image(SLATE_ICON, width=100)
st.title(TITLE)