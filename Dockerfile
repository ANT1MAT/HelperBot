FROM python:3.8
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY app /code/
CMD [ "python", "/code/bot_start.py"]
WORKDIR /code
