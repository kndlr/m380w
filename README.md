<h1 align="center">:clapper: SHW-M380W 영상 변환기</h1>

> XVID YouTube Downloader for SHW-M380W

### Why?

수명이 얼마 남지 않은 **`SHW-M380W` 태블릿**을 영상 머신으로 활용하고 싶었다

### How?

`SHW-M380W` (은)는 XVID 코덱의 영상을 720p 까지 정상적으로 지원하기에<br>
[`youtube-dl`](https://github.com/ytdl-org/youtube-dl) (을)를 통해 YouTube 영상을 다운로드, [`ffmpeg`](http://ffmpeg.org/) (을)를 통해 XVID 코덱으로 변환 작업을 한다<br>
그래픽 인터페이스 사용은 [`streamlit`](https://streamlit.io/) (으)로 처리한다

### Let's go!

구동하기 전에 [`ffmpeg`](http://ffmpeg.org/download.html) (이)가 설치되었는지 확인해주세요<br>
**(Windows의 경우, 명령이 시스템 환경 변수에 등록되었는지 확인해주세요)**

#### **라이브러리 설치하기**
    pip3 install -r requirements.txt

#### **구동하기**
    streamlit run app.py
