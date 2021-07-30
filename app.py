import streamlit as st
import streamlit.components.v1 as components
from streamlit_player import st_player
import youtube_dl
import subprocess
import re
import os
from data import *

st.set_page_config(page_title=TITLE, page_icon=SLATE_ICON)
st.image(SLATE_ICON, width=100)
st.title(TITLE)


class ExtensionPP(youtube_dl.postprocessor.common.PostProcessor):
    def __init__(self):
        super(ExtensionPP, self).__init__()

    def run(self, info):
        self.ext = os.path.splitext(info["filepath"])[1]
        return [], info


with open("style.css", "r") as f:
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
        available_res = dict(list(RESOLUTION.items())[: max_res_q + 1])
        rec_res = min(max(available_res.values()), 720)
        res = st.selectbox(
            "", available_res.keys(), index=list(available_res.values()).index(rec_res)
        )
        if RESOLUTION[res] > 720:
            st.warning(
                f"![iconS]({ERROR_ICON}) **1080p 이상의 영상**은 SHW-M380W 기기에서 재생되지 않을 수 있습니다"
            )

        st.markdown(
            f"""#### ![iconS]({TV_ICON}) 비디오 품질 <small>(1=최고, 5=기본, 31=최저)</small>""",
            unsafe_allow_html=True,
        )
        qv = st.slider("", 1, 31, 5, key="qv")

        st.markdown(
            f"""#### ![iconS]({SPEAKER_ICON}) 오디오 품질 <small>(1=최고, 5=기본, 31=최저)</small>""",
            unsafe_allow_html=True,
        )
        qa = st.slider("", 1, 31, 5, key="qa")

        st.markdown(f"### ![iconL]({SLATE_ICON}) 작업 진행 및 결과")

        if st.button("다운로드 및 변환"):

            st.markdown(f"#### ![iconS]({TV_ICON}) 비디오 다운로드")
            vbar = st.progress(0)

            st.markdown(f"#### ![iconS]({SPEAKER_ICON}) 오디오 다운로드")
            abar = st.progress(0)

            st.markdown(
                f"#### ![iconS]({FILM_ICON}) 코덱 변환 <small>(시간이 다소 소요될 수 있음)</small>",
                unsafe_allow_html=True,
            )
            fbar = st.progress(0)

            bar = vbar

            def progress(data):
                global bar, fm

                if data["status"] == "downloading":
                    percent = int(data["downloaded_bytes"] / data["total_bytes"] * 100)
                    bar.progress(percent)

                elif data["status"] == "finished":
                    bar = abar

            ydl_opts = {
                "format": f"bestvideo[ext=mp4][height<={RESOLUTION[res]}]+bestaudio/best[ext=mp4][height<={RESOLUTION[res]}]",
                "quiet": True,
                "no_warnings": True,
                "progress_hooks": [progress],
                "outtmpl": "./cache/%(id)s.%(ext)s",
                "cache-dir": "./cache",
            }

            processor = ExtensionPP()

            ydl = youtube_dl.YoutubeDL(ydl_opts)
            ydl.add_post_processor(processor)

            if not os.path.exists("./cache"):
                os.mkdir("./cache")

            with ydl:
                ydl.download([link])

            ext = processor.ext

            vbar.progress(100)
            abar.progress(100)

            command = [
                "ffprobe",
                "-select_streams",
                "v:0",
                "-count_packets",
                "-show_entries",
                "stream=nb_read_packets",
                "-of",
                "csv=p=0",
                "-i",
                f"./cache/{video.get('id', None)}{ext}",
            ]
            ffprobe = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )
            total = int(ffprobe.stdout)

            command = [
                "ffmpeg",
                "-y",
                "-i",
                f"./cache/{video.get('id', None)}{ext}",
                "-c:v",
                "mpeg4",
                "-vtag",
                "xvid",
                "-q:v",
                str(qv),
                "-q:a",
                str(qa),
                f"./cache/{video.get('id', None)}.avi",
            ]
            ffmpeg = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
            )

            pattern = re.compile(r"(frame)\=\s*(\S+)")

            while True:
                out = ffmpeg.stderr.readline().replace("\n", "")
                if not out:
                    break
                else:
                    frame = pattern.findall(out)
                    if frame:
                        fbar.progress(int(int(frame[0][1]) / total * 100))

            os.remove(f"./cache/{video.get('id', None)}{ext}")

            st.video(f"./cache/{video.get('id', None)}.avi", "video/avi")

            components.html(
                "<script>parent.window.open(parent.document.querySelector('.stVideo').src)</script>",
                height=0,
            )

            st.success(f"![iconS]({CHECK_ICON}) 성공적으로 다운로드했습니다")

            st.balloons()
