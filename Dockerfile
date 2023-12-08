FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY main.py main.py
COPY src/ src/
COPY database/ database/
COPY db_info.ini db_info.ini
CMD ["python", "main.py"]