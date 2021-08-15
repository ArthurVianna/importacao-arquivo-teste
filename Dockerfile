FROM python:3.9.2

COPY ./ /

RUN pip install -r /_requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]