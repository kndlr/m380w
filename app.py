import streamlit as st
from streamlit_player import st_player
import youtube_dl

TITLE = "SHW-M380W 영상 변환기"
SLATE_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/clapper-board_1f3ac.png"
LINK_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/link_1f517.png"
ERROR_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/warning_26a0-fe0f.png"
GEAR_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/gear_2699-fe0f.png"
SCREEN_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/desktop-computer_1f5a5-fe0f.png"
TV_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/television_1f4fa.png"
SPEAKER_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/speaker-low-volume_1f508.png"
RESOLUTION = ("480p (720*480)", "720p HD (1280*720)", "1080p FHD (1920*1080)")

st.set_page_config(page_title=TITLE, page_icon=SLATE_ICON)
st.image(SLATE_ICON, width=100)
st.title(TITLE)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(f"""### ![iconL]({LINK_ICON}) 다운로드할 YouTube 영상 링크""")
link = st.text_input(label="")

if link:
    try:
        with youtube_dl.YoutubeDL() as ydl:
            video = ydl.extract_info(link, download=False)
    except youtube_dl.utils.DownloadError:
        st.error(f"![iconS]({ERROR_ICON}) **올바른 YouTube 영상 링크**를 입력해주세요")
    else:
        st_player(video.get("webpage_url", None))

st.markdown(f"""### ![iconL]({GEAR_ICON}) 영상 다운로드 및 변환 설정""")

st.markdown(f"""#### ![iconS]({SCREEN_ICON}) 해상도 선택""")
option = st.selectbox("", RESOLUTION, index=1)
if option == RESOLUTION[2]:
    st.warning(f"![iconS]({ERROR_ICON}) **1080p 이상의 영상**은 SHW-M380W 기기에서 재생되지 않을 수 있습니다")

st.markdown(f"""#### ![iconS]({TV_ICON}) 비디오 품질 <small>(1=최고, 31=최저)</small>""", unsafe_allow_html=True)
qv = st.slider("", 1, 31, 5, key="qv", help="1=최고,31=최저")

st.markdown(f"""#### ![iconS]({SPEAKER_ICON}) 오디오 품질 <small>(1=최고, 31=최저)</small>""", unsafe_allow_html=True)
qa = st.slider("", 1, 31, 5, key="qa", help="1=최고,31=최저")
