FROM python:3.10.10

WORKDIR /Frilance_place
COPY main.py .
COPY functions.py .
COPY requirements.txt .
COPY .. templates ./templates/
COPY .. static ./static/

RUN pip install -r requirements.txt

CMD ["python3", "-m", "flask", "--app", "main.py", "run", "--host=0.0.0.0"]
