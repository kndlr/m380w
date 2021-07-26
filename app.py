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
CAPTION_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/page-with-curl_1f4c3.png"
MOVIE_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/movie-camera_1f3a5.png"
FILM_ICON = "https://emojipedia-us.s3.dualstack.us-west-1.amazonaws.com/thumbs/120/apple/285/film-frames_1f39e-fe0f.png"
RESOLUTION = {"144p" : 144, "240p" : 240, "360p" : 360, "480p" : 480, "720p HD" : 720, "1080p FHD" : 1080, "1440p QHD" : 1440, "2160p UHD" : 2160, "4320p QUHD" : 4320}

st.set_page_config(page_title=TITLE, page_icon=SLATE_ICON)
st.image(SLATE_ICON, width=100)
st.title(TITLE)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(f"### ![iconL]({LINK_ICON}) 다운로드할 YouTube 영상 링크")
link = st.text_input(label="")

if link:
    try:
        with youtube_dl.YoutubeDL() as ydl:
            video = ydl.extract_info(link, download=False)
    except youtube_dl.utils.DownloadError:
        st.error(f"![iconS]({ERROR_ICON}) **올바른 YouTube 영상 링크**를 입력해주세요")
    else:
        st_player(video.get("webpage_url", None))

        st.markdown(f"### ![iconL]({GEAR_ICON}) 영상 다운로드 및 변환 설정")

        st.markdown(f"#### ![iconS]({SCREEN_ICON}) 해상도 선택")
        max_res_q = max([i.get("quality", 0) for i in video["formats"]])
        available_res = dict(list(RESOLUTION.items())[:max_res_q+1])
        rec_res = min(max(available_res.values()), 720)
        res = st.selectbox("", available_res.keys(), index=list(available_res.values()).index(rec_res))
        if RESOLUTION[res] >= 1080:
            st.warning(f"![iconS]({ERROR_ICON}) **1080p 이상의 영상**은 SHW-M380W 기기에서 재생되지 않을 수 있습니다")

        st.markdown(f"""#### ![iconS]({TV_ICON}) 비디오 품질 <small>(1=최고, 5=기본, 31=최저)</small>""", unsafe_allow_html=True)
        qv = st.slider("", 1, 31, 5, key="qv")

        st.markdown(f"""#### ![iconS]({SPEAKER_ICON}) 오디오 품질 <small>(1=최고, 5=기본, 31=최저)</small>""", unsafe_allow_html=True)
        qa = st.slider("", 1, 31, 5, key="qa")

        st.json(video)

        st.markdown(f"### ![iconL]({SLATE_ICON}) 작업 진행 및 결과")

        if st.button("다운로드 및 변환"):
            
            st.markdown(f"#### ![iconS]({TV_ICON}) 비디오 다운로드")
            vbar = st.progress(0)

            st.markdown(f"#### ![iconS]({SPEAKER_ICON}) 오디오 다운로드")
            abar = st.progress(0)

            st.markdown(f"#### ![iconS]({MOVIE_ICON}) 비디오 및 오디오 결합")
            mbar = st.progress(0)

            st.markdown(f"#### ![iconS]({FILM_ICON}) 코덱 변환")
            fbar = st.progress(0)

            bar = vbar

            def progress(data):
                global bar, total_duration

                if data["status"] == "downloading":
                    percent = int(data["downloaded_bytes"] / data["total_bytes"] * 100)
                    bar.progress(percent)
                    
                    if percent == 100:
                        bar = abar
            
            ydl_opts = {
                "format" : f"bestvideo[height<={RESOLUTION[res]}]+bestaudio/best[height<={RESOLUTION[res]}]",
                "quiet" : True,
                "no_warnings" : True,
                "progress_hooks" : [progress],
                "outtmpl" : "./cache/%(id)s.%(ext)s",
                "cache-dir" : "./cache",
                "merge_output_format" : "mp4",
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            vbar.progress(100)
            abar.progress(100)
            mbar.progress(100)
