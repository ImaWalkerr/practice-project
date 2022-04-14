FROM python:3.9.8
ENV PYTHONBUFFERED=1
WORKDIR /usr/src/games
COPY requirements_windows.txt ./
RUN pip install -r requirements_windows.txt
COPY . ./