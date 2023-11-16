FROM python:3.9
RUN pip install streamlit pandas gtts openai pydub imageio-ffmpeg ffprobe

COPY ./ /app
WORKDIR /app
CMD ["streamlit", "run", "app.py", "--server.port", "80", "--server.enableCORS", "false"]
