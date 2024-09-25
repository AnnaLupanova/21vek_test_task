FROM python:3.8
WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN pip install fastapi uvicorn
COPY /api .
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]