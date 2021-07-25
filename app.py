import streamlit as st
import youtube_dl

TITLE = "SHW-M380W 영상 변환기"
SLATE_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/clapper-board_1f3ac.png"
LINK_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/link_1f517.png"
ERROR_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/warning_26a0-fe0f.png"

st.set_page_config(page_title=TITLE, page_icon=SLATE_ICON)
st.image(SLATE_ICON, width=100)
st.title(TITLE)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(f"""### ![iconL]({LINK_ICON}) 다운로드할 YouTube 영상 링크""")
link = st.text_input(label="")

try:
    with youtube_dl.YoutubeDL() as ydl:
        video = ydl.extract_info(link, download=False)
except youtube_dl.utils.DownloadError:
    st.error(f"![iconS]({ERROR_ICON}) **올바른 YouTube 영상 링크**를 입력해주세요")
