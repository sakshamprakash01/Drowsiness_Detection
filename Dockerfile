FROM python:3.9-slim
ADD . /app
WORKDIR /app
RUN apt-get update -q \
  && apt-get install --no-install-recommends -qy python3-dev g++ gcc inetutils-ping \
  && apt-get update && apt-get install ffmpeg libsm6 libxext6 libxrender-dev -y \
  && pip install --no-cache-dir --progress-bar off gunicorn \
  && pip install --no-cache-dir --progress-bar off -r requirements.txt \
  && apt-get remove -qy python3-dev g++ gcc --purge
ENTRYPOINT ["python"]
CMD ["app.py"]